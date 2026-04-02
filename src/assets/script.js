  const days = Object.keys(timetable);
  let currentDayIndex = new Date().getDay() - 1;
  // Handle weekends (Saturday=5, Sunday=-1) and out of range days
  if (currentDayIndex < 0 || currentDayIndex >= days.length) currentDayIndex = 0;

  // Load custom timetable from localStorage if it exists
  function loadTimetable() {
    const saved = localStorage.getItem('customTimetable');
    if (saved) {
      try {
        return JSON.parse(saved);
      } catch (e) {
        console.log('Failed to parse saved timetable, using default');
        return timetable;
      }
    }
    return timetable;
  }

  // Get current timetable (custom or default)
  let currentTimetable = loadTimetable();

  function saveTimetable() {
    localStorage.setItem('customTimetable', JSON.stringify(currentTimetable));
  }

  function resetTimetable() {
    if (confirm('Are you sure you want to reset the timetable to default?')) {
      localStorage.removeItem('customTimetable');
      currentTimetable = JSON.parse(JSON.stringify(timetable));
      updateEditForm();
      renderDay();
    }
  }

  function toggleEditMode() {
    document.getElementById('editModal').classList.remove('hidden');
    document.getElementById('editDay').value = days[currentDayIndex];
    updateEditForm();
  }

  function closeEditModal() {
    document.getElementById('editModal').classList.add('hidden');
  }

  function showAboutInfo() {
    document.getElementById('aboutModal').classList.remove('hidden');
  }

  function closeAboutModal() {
    document.getElementById('aboutModal').classList.add('hidden');
  }

  // Close modal when clicking outside
  window.addEventListener('click', function(event) {
    const editModal = document.getElementById('editModal');
    const aboutModal = document.getElementById('aboutModal');

    if (event.target === editModal) {
      closeEditModal();
    }

    if (event.target === aboutModal) {
      closeAboutModal();
    }
  });

  function updateEditForm() {
    const selectedDay = document.getElementById('editDay').value;
    const periods = currentTimetable[selectedDay];
    const periodsList = document.getElementById('periodsList');
    periodsList.innerHTML = '';

    periods.forEach((period, index) => {
      const editor = document.createElement('div');
      editor.className = 'period-editor';
      editor.innerHTML = `
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px;">
          <strong style="font-size: 14px;">Period ${index + 1}</strong>
          <button style="background: #ff6b6b; color: white; border: none; padding: 4px 8px; border-radius: 4px; cursor: pointer;" 
                  onclick="deletePeriod('${selectedDay}', ${index})">Delete</button>
        </div>
        <div class="period-editor-row">
          <div>
            <label>Start Time:</label>
            <input type="time" value="${period.start}" onchange="updatePeriodField('${selectedDay}', ${index}, 'start', this.value)">
          </div>
          <div>
            <label>End Time:</label>
            <input type="time" value="${period.end}" onchange="updatePeriodField('${selectedDay}', ${index}, 'end', this.value)">
          </div>
        </div>
        <label>Subject:</label>
        <input type="text" value="${period.subject}" onchange="updatePeriodField('${selectedDay}', ${index}, 'subject', this.value)">
        <label>Type:</label>
        <select onchange="updatePeriodField('${selectedDay}', ${index}, 'type', this.value)">
          <option value="theory" ${period.type === 'theory' ? 'selected' : ''}>Theory</option>
          <option value="lab" ${period.type === 'lab' ? 'selected' : ''}>Lab</option>
          <option value="elective" ${period.type === 'elective' ? 'selected' : ''}>Elective</option>
          <option value="project" ${period.type === 'project' ? 'selected' : ''}>Project</option>
          <option value="break" ${period.type === 'break' ? 'selected' : ''}>Break</option>
          <option value="sp" ${period.type === 'sp' ? 'selected' : ''}>Special</option>
          <option value="free" ${period.type === 'free' ? 'selected' : ''}>Free</option>
          <option value="seminar" ${period.type === 'seminar' ? 'selected' : ''}>Seminar</option>
          <option value="workshop" ${period.type === 'workshop' ? 'selected' : ''}>Workshop</option>
          <option value="other" ${period.type === 'other' ? 'selected' : ''}>Other</option>
        </select>
      `;
      periodsList.appendChild(editor);
    });

    // Add new period button
    const addBtn = document.createElement('button');
    addBtn.className = 'btn-save';
    addBtn.style.width = '100%';
    addBtn.textContent = '+ Add Period';
    addBtn.onclick = () => addNewPeriod(selectedDay);
    periodsList.appendChild(addBtn);

    // Save button
    const saveBtn = document.createElement('button');
    saveBtn.className = 'btn-save';
    saveBtn.style.width = '100%';
    saveBtn.style.marginTop = '10px';
    saveBtn.textContent = 'Save Changes';
    saveBtn.onclick = () => {
      saveTimetable();
      renderDay();
      alert('Timetable updated successfully!');
    };
    periodsList.appendChild(saveBtn);
  }

  function updatePeriodField(day, index, field, value) {
    if (currentTimetable[day] && currentTimetable[day][index]) {
      currentTimetable[day][index][field] = value;
    }
  }

  function deletePeriod(day, index) {
    if (confirm('Delete this period?')) {
      currentTimetable[day].splice(index, 1);
      updateEditForm();
    }
  }

  function addNewPeriod(day) {
    const newPeriod = {
      start: '09:00',
      end: '10:00',
      subject: 'New Subject',
      type: 'theory'
    };
    currentTimetable[day].push(newPeriod);
    updateEditForm();
  }

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

    currentTimetable[day].forEach(p => {
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

  /* ================= SLIDER & BASIC NAVIGATION ================= */
  function changeDay(direction){
    const container = document.getElementById('timetable');
    // Apply Slide Out Animation
    const outClass= direction === 'next' ? 'slide-out-left':'slide-out-right';
    container.classList.add(outClass);

    setTimeout(()=> {
      if (direction==='next'){ currentDayIndex=(currentDayIndex + 1) % days.length; }
      else{ currentDayIndex = (currentDayIndex - 1 + days.length) % days.length; }
      
      renderDay();

      container.classList.remove(outClass);
      const inClass = direction==='next' ? 'slide-in-right':'slide-in-left';
      container.classList.add(inClass);

      // Cleanup th animation class after it finishes
      setTimeout(()=>{
        container.classList.remove(inClass);
            // Scroll to active period ONLY after animation finishes
            scrollToActive();
      },300)
    },300)
  }

  function prevDay() { changeDay('prev') }
  function nextDay() { changeDay('next') }

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

  /* ================= KEYBOARD NAVIGATION ================= */
  document.addEventListener('keydown', e => {
    if (e.key === 'ArrowLeft') {
      prevDay();
    } else if (e.key === 'ArrowRight') {
      nextDay();
    }
  });

  /* ================= LIVE TRACKING ================= */
  setInterval(renderDay, 60000);

  renderDay();
  // 1. Find the first element with the 'active' class and scroll it into view
  function scrollToActivePeriod() {
    const activeElement = document.querySelector('.period.active');
    if (activeElement) {
      activeElement.scrollIntoView({ behavior: 'smooth', block: 'center' });
    }
  }