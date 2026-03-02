# Class Timetable v2.4.0

A responsive, Progressive Web App (PWA) for managing and viewing class schedules with real-time period tracking.
![Screenshot of TimeTable PWA](assets/screenshot_360.jpg)


## Features

- **Real-time Tracking**: Automatically highlights the current class period
- **Responsive Design**: Works seamlessly on desktop, tablet, and mobile devices
- **Touch Gestures**: Swipe left/right to navigate between days
- **PWA Support**: Install as a standalone app on mobile devices
- **Offline Capable**: Service worker enables offline functionality
- **Customizable Schedule**: Easy-to-edit timetable data structure

## Project Structure

```
class-timetable/
├── index.html          # Main HTML file
├── time-table.js       # Timetable data configuration
├── serve.py            # Local development server with python (if needed)
├── LICENSE             # License file
├── sw.js               # Service worker for PWA
├── assets/
│   ├── main.css        # Main stylesheet
│   ├── portrait.css    # Portrait orientation styles (optional)
│   ├── landscape.css   # Landscape orientation styles (optional)
│   ├── script.js       # Main application logic
│   └── site.webmanifest # PWA manifest file
```

## Getting Started

### Prerequisites

- Python 3.x (if you wanna run the development server)
- A modern web browser with service worker support

### Installation

1. Clone or download this repository:
   ```bash
   git clone https://github.com/amalbenny/class-timetable.git
   cd class-timetable
   ```

2. Run the local development server:
   ```bash
   python3 serve.py
   ```

3. The application will automatically open in your default browser at `http://localhost:1342`

### Alternative Setup

You can also serve the files using any HTTP server of your choice:

```bash
# Using Python's built-in server
python3 -m http.server 8000

# Using Node.js http-server
npx http-server

# Using PHP
php -S localhost:8000
```

## Customizing Your Timetable

Edit the [time-table.js](time-table.js) file to customize your schedule:

```javascript
const timetable = {
  Monday: [
    { 
      start: "09:00", 
      end: "09:50", 
      subject: "Mathematics", 
      type: "theory" 
    },
    // Add more periods...
  ],
  // Add more days...
};
```

### Period Types

The application supports different period types with color-coded badges:

- `theory` - Regular theory classes
- `elective` - Elective courses
- `project` - Project work
- `lab` - Laboratory sessions
- `break` - Break times
- `sp` - Special periods
- `seminar` - Seminar sessions
- `workshop` - Workshop sessions
- `free` - Free periods
- `other` - Other activities

## Usage
Head to https://amalbenny.github.io/class-timetable/ to view a sample timtable hosted in [GitHub Pages](https://pages.github.com/)
### Navigation

- **Desktop**: Use the arrow buttons (◁ ▷) in the header to switch between days
- **Mobile/Touch**: Swipe left or right to navigate between days
- **Current Period**: The currently active period is automatically highlighted

### Installing as PWA

**On Mobile (Android/iOS):**
1. Open the app in your browser
2. Tap the browser menu
3. Select "Add to Home Screen" or "Install App"
4. The app will be installed on your device and can be launched like a native app

**On Desktop (Chrome/Edge):**
1. Look for the install icon in the address bar
2. Click it and confirm the installation
3. The app will be available in your applications menu

## Configuration

### Changing the Server Port

Edit [serve.py](serve.py) to change the default port:

```python
PORT = 1342  # Change to your preferred port
```

### Orientation-Specific Styles

To enable different styles for portrait and landscape orientations:

1. Uncomment the orientation-specific stylesheet links in [index.html](index.html)
2. Edit [assets/portrait.css](assets/portrait.css) and [assets/landscape.css](assets/landscape.css) as needed

## Browser Compatibility

- Chrome/Edge: Full support
- Firefox: Full support
- Safari: Full support (iOS 11.3+)
- Opera: Full support

## Development

### File Descriptions

- **index.html**: Main entry point, contains the app structure
- **time-table.js**: Timetable data configuration
- **assets/script.js**: Core application logic (rendering, navigation, gesture handling)
- **assets/main.css**: Main styles and theme
- **assets/sw.js**: Service worker for offline caching
- **assets/site.webmanifest**: PWA manifest configuration
- **serve.py**: Simple Python HTTP server with auto-browser launch

### Adding New Features

The modular structure makes it easy to extend:
- Add new period types by updating the CSS in `main.css`
- Modify the layout by editing `index.html` and `main.css`
- Extend functionality by adding code to `script.js`

## License

See the [LICENSE](LICENSE) file for details.

## Support

For issues or questions, please open an [Issue](https://github.com/amalbenny/class-timetable/issues) or communicate through [Discussions Tab](https://github.com/amalbenny/class-timetable/discussions) in the repository.

---

**Version**: 2.4.1
**Last Updated**: February 2026
