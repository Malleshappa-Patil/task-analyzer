let stagedTasks = [];
let analyzedResults = []; // Store API results here

// 1. Handle Tab Switching
function switchTab(tab) {
    document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
    event.target.classList.add('active');
    
    if (tab === 'form') {
        document.getElementById('taskForm').classList.remove('hidden-tab');
        document.getElementById('jsonInput').classList.add('hidden-tab');
    } else {
        document.getElementById('taskForm').classList.add('hidden-tab');
        document.getElementById('jsonInput').classList.remove('hidden-tab');
    }
}

// 2. Add Task Manually
document.getElementById('taskForm').addEventListener('submit', (e) => {
    e.preventDefault();
    const task = {
        title: document.getElementById('title').value,
        due_date: document.getElementById('dueDate').value || null,
        estimated_hours: parseFloat(document.getElementById('hours').value),
        importance: parseInt(document.getElementById('importance').value),
        dependencies: [] // Simple version for MVP
    };
    addTaskToList(task);
    e.target.reset();
});

// 3. Add via JSON
function parseJson() {
    try {
        const data = JSON.parse(document.getElementById('jsonText').value);
        if (Array.isArray(data)) {
            data.forEach(task => addTaskToList(task));
            document.getElementById('jsonText').value = '';
        } else {
            alert("JSON must be an array of objects.");
        }
    } catch (err) {
        alert("Invalid JSON format.");
    }
}

function addTaskToList(task) {
    stagedTasks.push(task);
    updateUI();
}

function updateUI() {
    const list = document.getElementById('taskList');
    document.getElementById('count').innerText = stagedTasks.length;
    document.getElementById('analyzeBtn').disabled = stagedTasks.length === 0;
    
    list.innerHTML = stagedTasks.map((t, i) => `
        <li>
            <span>${t.title}</span>
            <small>Imp: ${t.importance}</small>
        </li>
    `).join('');
}

// 4. CALL THE API
document.getElementById('analyzeBtn').addEventListener('click', async () => {
    const resultsArea = document.getElementById('resultsArea');
    resultsArea.innerHTML = '<p>Analyzing with Python Logic...</p>';

    try {
        const response = await fetch('http://127.0.0.1:8000/api/tasks/analyze/', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(stagedTasks)
        });

        if (!response.ok) throw new Error('API Error');

        analyzedResults = await response.json(); // Store for re-sorting
        applySorting(); // Render results

    } catch (error) {
        resultsArea.innerHTML = `<p style="color:red">Error: ${error.message}. Is Django running?</p>`;
    }
});

// 5. CLIENT-SIDE SORTING (The "Toggle" Requirement)
function applySorting() {
    const strategy = document.getElementById('sortStrategy').value;
    let data = [...analyzedResults]; // Copy array

    // Sort Logic
    if (strategy === 'smart') {
        // Already sorted by API, but good to be safe
        data.sort((a, b) => b.priority_score - a.priority_score);
    } else if (strategy === 'urgent') {
        data.sort((a, b) => {
            // Handle null dates (put them last)
            if (!a.due_date) return 1;
            if (!b.due_date) return -1;
            return new Date(a.due_date) - new Date(b.due_date);
        });
    } else if (strategy === 'important') {
        data.sort((a, b) => b.importance - a.importance);
    } else if (strategy === 'quick') {
        data.sort((a, b) => a.estimated_hours - b.estimated_hours);
    }

    renderResults(data);
}

function renderResults(tasks) {
    const container = document.getElementById('resultsArea');
    container.innerHTML = tasks.map(task => {
        // Determine Color Class
        let priorityClass = 'priority-low';
        if (task.priority_score > 80) priorityClass = 'priority-high';
        else if (task.priority_score > 40) priorityClass = 'priority-medium';

        return `
            <div class="task-card ${priorityClass}">
                <div class="score-badge">${task.priority_score.toFixed(1)}</div>
                <h3>${task.title}</h3>
                <div class="meta">
                    <span>📅 Due: ${task.due_date || 'None'}</span>
                    <span>⭐ Imp: ${task.importance}</span>
                    <span>⏱️ ${task.estimated_hours}h</span>
                </div>
            </div>
        `;
    }).join('');
}