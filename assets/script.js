  const days = Object.keys(timetable);
  let currentDayIndex = new Date().getDay() - 1;
  // Handle weekends (Saturday=5, Sunday=-1) and out of range days
  if (currentDayIndex < 0 || currentDayIndex >= days.length) currentDayIndex = 0;

  function timeToMinutes(t) {
    const [h, m] = t.split(":").map(Number);
    return h * 60 + m;
  }

  function renderDay() {
    const day = days[currentDayIndex];
    document.getElementById("dayinfo").innerText = day;

    // Update variable now with live tracker
    const now = new Date();
    const nowMin = now.getHours() * 60 + now.getMinutes();

    const container = document.getElementById("timetable");
    container.innerHTML = "";

    timetable[day].forEach(p => {
      const active = now.getDay() - 1 === currentDayIndex &&
        nowMin >= timeToMinutes(p.start) && nowMin <= timeToMinutes(p.end);

      const div = document.createElement("div");
      div.className = `period ${active ? "active" : ""}`;

      div.innerHTML = `
        <div class="info">
          <div class="time">${p.start} – ${p.end}</div>
          <div class="subject">${p.subject}</div>
        </div>
        <div class="type ${p.type}">${p.type.toUpperCase()}</div>
      `;

      container.appendChild(div);
    });
  }

  function prevDay() { currentDayIndex = (currentDayIndex - 1 + days.length) % days.length; renderDay(); }
  function nextDay() { currentDayIndex = (currentDayIndex + 1) % days.length; renderDay(); }

  /* ================= GESTURE NAVIGATION ================= */
  let startX = 0, startY = 0;

  document.addEventListener("touchstart", e => {
    startX = e.touches[0].clientX;
    startY = e.touches[0].clientY;
  });

  document.addEventListener("touchend", e => {
    const diffX = e.changedTouches[0].clientX - startX;
    const diffY = e.changedTouches[0].clientY - startY;
    
    // Only trigger swipe if horizontal movement is dominant
    if (Math.abs(diffX) > Math.abs(diffY) && Math.abs(diffX) > 80) {
      if (diffX > 0) prevDay();
      else nextDay();
    }
  });

  /* ================= LIVE TRACKING ================= */
  setInterval(renderDay, 60000);

  renderDay();
  // 1. Find the first element with the 'active' class and scroll it into view
  const activeElement = document.querySelector('.period.active');
  if (activeElement) {
    activeElement.scrollIntoView({ behavior: 'smooth', block: 'center' });
  }

  /* ================= NOTIFICATION SYSTEM ================= */
  
  // Request notification permission on load
  function requestNotificationPermission() {
    if ('Notification' in window && Notification.permission === 'default') {
      Notification.requestPermission();
    }
  }

  // Get next period details
  function getNextPeriod() {
    const now = new Date();
    const currentDay = now.getDay() - 1;
    const nowMin = now.getHours() * 60 + now.getMinutes();

    // Check today's remaining periods
    if (currentDay >= 0 && currentDay < days.length) {
      const todaysPeriods = timetable[days[currentDay]];
      for (let period of todaysPeriods) {
        if (timeToMinutes(period.start) > nowMin) {
          return {
            day: days[currentDay],
            period: period,
            minutesUntilStart: timeToMinutes(period.start) - nowMin
          };
        }
      }
    }

    // If no remaining periods today, get first period of next week day
    let nextDayIndex = (currentDay + 1) % days.length;
    if (nextDayIndex > currentDay || nextDayIndex === 0) {
      return {
        day: days[nextDayIndex],
        period: timetable[days[nextDayIndex]][0],
        minutesUntilStart: Infinity // Next day
      };
    }

    return null;
  }

  // Notification tracking to avoid duplicates
  let notificationShown = false;
  let notificationStartTime = null;

  // Check and send notifications
  function checkAndNotify() {
    const next = getNextPeriod();
    
    if (!next) return;

    const minutesUntil = next.minutesUntilStart;

    // Send notification when exactly 5 minutes before period starts
    if (minutesUntil <= 5 && minutesUntil > 4.5 && !notificationShown) {
      if ('Notification' in window && Notification.permission === 'granted') {
        notificationShown = true;
        notificationStartTime = Date.now();
        
        const notification = new Notification('Next Period Starting Soon! ⏰', {
          body: `${next.period.subject} starts at ${next.period.start}`,
          icon: 'assets/favicon-96x96.png',
          badge: 'assets/favicon-96x96.png',
          tag: 'period-notification',
          requireInteraction: true,
          data: {
            period: next.period,
            day: next.day
          }
        });

        // Handle notification clicks
        notification.onclick = () => {
          window.focus();
          notification.close();
        };

        // Start countdown timer every second
        const countdownInterval = setInterval(() => {
          const elapsed = (Date.now() - notificationStartTime) / 1000;
          const remaining = Math.max(0, 300 - Math.floor(elapsed)); // 300 seconds = 5 minutes

          if (remaining > 0) {
            const mins = Math.floor(remaining / 60);
            const secs = remaining % 60;
            const timeStr = `${mins}:${secs < 10 ? '0' : ''}${secs}`;
            
            // Update notification title with countdown
            notification.close();
            new Notification('Next Period Starting Soon! ⏰', {
              body: `${next.period.subject} starts at ${next.period.start}\n⏱️ ${timeStr} remaining`,
              icon: 'assets/favicon-96x96.png',
              badge: 'assets/favicon-96x96.png',
              tag: 'period-notification',
              requireInteraction: true,
              data: {
                period: next.period,
                day: next.day
              }
            });
          } else {
            clearInterval(countdownInterval);
            notificationShown = false;
          }
        }, 1000);
      }
    }

    // Reset flag when period starts
    if (minutesUntil <= 0) {
      notificationShown = false;
    }
  }

  // Check for notifications every 10 seconds
  setInterval(checkAndNotify, 10000);
  
  // Initial check on page load
  requestNotificationPermission();
  checkAndNotify();
