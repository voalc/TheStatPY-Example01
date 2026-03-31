import os
import re
import sys
import ctypes

class Colors:
    ANSI_CODES = {
        "red": "\033[91m", "green": "\033[92m", "yellow": "\033[93m", "blue": "\033[94m", 
        "magenta": "\033[95m", "cyan": "\033[96m", "white": "\033[97m", "black": "\033[30m",
        
        "bg_red": "\033[41m", "bg_green": "\033[42m", "bg_yellow": "\033[43m", 
        "bg_blue": "\033[44m", "bg_magenta": "\033[45m", "bg_cyan": "\033[46m", 
        "bg_white": "\033[107m", "bg_black": "\033[40m",

        "bold": "\033[1m", "underline": "\033[4m", "dim": "\033[2m",
        "italic": "\033[3m", "strike": "\033[9m", "reset": "\033[0m",
    }

    def __init__(self):
        self.enabled = self._check_support()
        self._all_codes = {**self.ANSI_CODES}

    def _check_support(self):
        if "NO_COLOR" in os.environ or not sys.stdout.isatty(): return False
        if sys.platform == "win32":
            try:
                h = ctypes.windll.kernel32.GetStdHandle(-11)
                m = ctypes.c_ulong()
                ctypes.windll.kernel32.GetConsoleMode(h, ctypes.byref(m))
                return bool(ctypes.windll.kernel32.SetConsoleMode(h, m.value | 0x0004))
            except (AttributeError, OSError):
                return False
        return os.environ.get("TERM") != "dumb"

    def __getattr__(self, name):
        # This still handles standard named colors like 'red' or 'bold'
        return self._all_codes.get(name.lower(), "") if self.enabled else ""

    def ext(self, n: int, background=False) -> str:
        """Returns 256-color sequence (n from 0-255)."""
        if not self.enabled: return ""
        try:
            n = int(n)
        except (TypeError, ValueError):
            return ""
        if not 0 <= n <= 255:
            return ""
        code = 48 if background else 38
        return f"\033[{code};5;{n}m"

    def hex(self, hex_code: str, background=False) -> str:
        """Returns TrueColor (24-bit) sequence from hex string."""
        if not self.enabled: return ""
        if not isinstance(hex_code, str):
            return ""
        normalized = hex_code.lstrip('#')
        if not re.fullmatch(r"[0-9a-fA-F]{6}", normalized):
            return ""
        r, g, b = tuple(int(normalized[i:i+2], 16) for i in (0, 2, 4))
        code = 48 if background else 38
        return f"\033[{code};2;{r};{g};{b}m"

    def paint(self, text: str, *styles: str) -> str:
        if not self.enabled: return text
        # Ignore unknown/non-string styles so user-facing output remains resilient.
        resolved_styles = []
        for s in styles:
            if isinstance(s, str):
                resolved_styles.append(s if s.startswith("\033") else getattr(self, s))
        prefix = "".join(resolved_styles)
        return f"{prefix}{text}{self.reset}"
    
    def _get_visual_len(self, text: str) -> int:
        """Helper to calculate the length of text without ANSI codes."""
        # This regex removes all \033[...m sequences
        ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
        return len(ansi_escape.sub('', str(text)))

    def align(self, text: str, width: int, align: str = 'left', *styles: str) -> str:
        """
        Aligns text within a specific width and then applies styles.
        - align: 'left' (<), 'center' (^), or 'right' (>)
        """
        directions = {'left': '<', 'center': '^', 'right': '>'}
        dir_char = directions.get(align.lower(), '<')
        
        # Format the plain text first so spaces get the background color after checking visual length
        vis_len = self._get_visual_len(text)
        adjusted_width = width + (len(str(text)) - vis_len)
        formatted_text = f"{str(text):{dir_char}{adjusted_width}}"
        return self.paint(formatted_text, *styles)
    
    def list_defaults(self):
        """Prints all named colors and effects."""
        print(self.paint("\n --- Default Named Styles --- ", "white", "bg_blue", "bold"))
        for name in self.ANSI_CODES:
            if not name.startswith("bg_") and name != "reset":
                print(f"{name:10} : {self.paint('Example Text', name)}")

    def list_256(self):
        """Prints a formatted grid of the 256-color palette."""
        print(self.paint("\n --- 256-Color Chart --- ", "white", "bg_blue", "bold"))
        for i in range(256):
            # Print the number with its color as background
            # We use black text for light colors and white for dark to keep it readable
            fg = "black" if (i > 10 and i < 52) or (i > 69 and i < 123) or i > 190 else "white"
            sys.stdout.write(self.paint(f" {i:3} ", fg, self.ext(i, background=True)))
            if (i + 1) % 16 == 0:
                sys.stdout.write("\n")
        print(self.reset)

    def box(self, content, width: int = 40, align: str = 'center', color: str = 'cyan'):
        """
        Draws a box around text. Supports multi-line strings or lists of strings.
        """
        # Box characters
        tl, tr, bl, br, hz, vt = "┌", "┐", "└", "┘", "─", "│"

        # Split content into lines if it's a string, or treat as list
        lines = content.split('\n') if isinstance(content, str) else content

        print(self.paint(f"{tl}{hz * (width + 2)}{tr}", color))
        side = self.paint(vt, color)
        for line in lines:
            print(f"{side} {self.align(line, width, align)} {side}")
        print(self.paint(f"{bl}{hz * (width + 2)}{br}", color))

    def table(self, data: list, header_color: str = "cyan", border_color: str = "dim"):
        """
        Generates a colored table from a list of dictionaries.
        """
        if not data: return
        headers = list(data[0].keys())
        
        # 1. Calculate max width for each column (checking headers and all rows)
        col_widths = {h: self._get_visual_len(h) for h in headers}
        for row in data:
            for h in headers:
                value = row.get(h, "")
                col_widths[h] = max(col_widths[h], self._get_visual_len(value))

        # 2. Build Border Helpers
        vt = self.paint("│", border_color)
        hz = self.paint("─", border_color)
        
        def get_divider():
            parts = [hz * (col_widths[h] + 2) for h in headers]
            return self.paint("┼", border_color).join(parts)

        # 3. Print Headers
        header_row = f" {vt} ".join([self.align(h.upper(), col_widths[h], 'center', header_color, 'bold') for h in headers])
        print(f"\n {header_row} ")
        print(get_divider())

        # 4. Print Rows
        for row in data:
            row_str = f" {vt} ".join([self.align(row.get(h, ""), col_widths[h], 'left') for h in headers])
            print(f" {row_str} ")

cl = Colors()