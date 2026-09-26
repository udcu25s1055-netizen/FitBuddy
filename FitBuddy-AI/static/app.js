const form = document.getElementById('planForm');
const result = document.getElementById('result');

form.addEventListener('submit', async (event) => {
  event.preventDefault();

  const payload = {
    goal: document.getElementById('goal').value,
    experience: document.getElementById('experience').value,
    days_per_week: Number(document.getElementById('days_per_week').value),
    minutes_per_session: Number(document.getElementById('minutes_per_session').value),
    equipment: document.getElementById('equipment').value,
    focus_areas: document.getElementById('focus_areas').value,
    notes: document.getElementById('notes').value,
  };

  result.innerHTML = '<p class="empty-state">Generating your workout plan...</p>';

  try {
    const response = await fetch('/api/generate-plan', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload),
    });

    if (!response.ok) {
      throw new Error('Request failed');
    }

    const data = await response.json();

    result.innerHTML = `
      <h3 class="plan-title">${data.title}</h3>
      <p class="plan-overview">${data.overview}</p>
      ${data.weekly_schedule.map(item => `
        <div class="schedule-item">
          <h3>${item.day} — ${item.focus}</h3>
          <ul>
            ${item.workout.map(step => `<li>${step}</li>`).join('')}
          </ul>
          <div class="recovery">Recovery: ${item.recovery}</div>
        </div>
      `).join('')}
    `;
  } catch (error) {
    result.innerHTML = '<p class="empty-state">Unable to generate a plan right now. Please try again.</p>';
  }
});
