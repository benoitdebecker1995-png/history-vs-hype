/**
 * Frontend JavaScript for History Clip Tool
 * Handles API communication and UI updates
 */

const API_BASE = 'http://localhost:8000';
let selectedProjectId = null;

// Utility: Show status message
function showStatus(elementId, message, type) {
    const el = document.getElementById(elementId);
    el.textContent = message;
    el.className = `status ${type}`;
}

// Utility: Hide status message
function hideStatus(elementId) {
    const el = document.getElementById(elementId);
    el.className = 'status';
}

// ============================================================================
// STEP 1: Create Project
// ============================================================================

document.getElementById('createProjectForm').addEventListener('submit', async (e) => {
    e.preventDefault();

    const name = document.getElementById('projectName').value;
    const videoFile = document.getElementById('videoFile').files[0];

    if (!videoFile) {
        showStatus('createStatus', 'Please select a video file', 'error');
        return;
    }

    showStatus('createStatus', 'Uploading video and creating project...', 'info');

    const formData = new FormData();
    formData.append('video', videoFile);

    try {
        const response = await fetch(`${API_BASE}/projects/?name=${encodeURIComponent(name)}`, {
            method: 'POST',
            body: formData
        });

        if (!response.ok) {
            throw new Error('Failed to create project');
        }

        const project = await response.json();
        showStatus('createStatus', `✓ Project created: ${project.name} (ID: ${project.id})`, 'success');

        // Reset form
        document.getElementById('createProjectForm').reset();

        // Auto-load projects
        loadProjects();

    } catch (error) {
        showStatus('createStatus', `Error: ${error.message}`, 'error');
    }
});

// ============================================================================
// STEP 2: Load Projects & Transcribe
// ============================================================================

document.getElementById('loadProjectsBtn').addEventListener('click', loadProjects);

async function loadProjects() {
    try {
        const response = await fetch(`${API_BASE}/projects/`);
        const projects = await response.json();

        const list = document.getElementById('projectList');
        list.innerHTML = '';

        if (projects.length === 0) {
            list.innerHTML = '<li style="padding: 15px; color: #999;">No projects yet. Create one above.</li>';
            return;
        }

        projects.forEach(project => {
            const li = document.createElement('li');
            li.className = 'project-item';
            li.innerHTML = `
                <strong>${project.name}</strong><br>
                <small>
                    Duration: ${project.duration?.toFixed(1) || 'N/A'}s |
                    Transcribed: ${project.transcribed ? '✓' : '✗'} |
                    Clips Detected: ${project.clips_detected ? '✓' : '✗'}
                </small>
            `;

            li.addEventListener('click', () => selectProject(project.id, li));
            list.appendChild(li);
        });

    } catch (error) {
        console.error('Error loading projects:', error);
    }
}

function selectProject(projectId, element) {
    selectedProjectId = projectId;

    // Visual feedback
    document.querySelectorAll('.project-item').forEach(el => el.classList.remove('selected'));
    element.classList.add('selected');

    // Show transcribe section
    document.getElementById('transcribeSection').classList.remove('hidden');
}

document.getElementById('transcribeBtn').addEventListener('click', async () => {
    if (!selectedProjectId) {
        alert('Please select a project first');
        return;
    }

    const modelSize = document.getElementById('modelSize').value;

    showStatus('transcribeStatus', 'Starting transcription... This may take several minutes.', 'info');

    try {
        const response = await fetch(`${API_BASE}/transcribe/${selectedProjectId}?model_size=${modelSize}`, {
            method: 'POST'
        });

        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.detail || 'Transcription failed');
        }

        const result = await response.json();
        showStatus('transcribeStatus', '✓ Transcription started. Check project status by refreshing the project list.', 'success');

    } catch (error) {
        showStatus('transcribeStatus', `Error: ${error.message}`, 'error');
    }
});

// ============================================================================
// STEP 3: Detect Clips
// ============================================================================

document.getElementById('detectBtn').addEventListener('click', async () => {
    if (!selectedProjectId) {
        alert('Please select a project first');
        return;
    }

    const minScore = document.getElementById('minScore').value;
    const maxClips = document.getElementById('maxClips').value;

    showStatus('detectStatus', 'Analyzing transcript and detecting clips...', 'info');

    try {
        const response = await fetch(
            `${API_BASE}/clips/${selectedProjectId}/detect?min_score=${minScore}&max_clips=${maxClips}`,
            { method: 'POST' }
        );

        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.detail || 'Clip detection failed');
        }

        const clips = await response.json();
        showStatus('detectStatus', `✓ Detected ${clips.length} high-value clips`, 'success');

        // Auto-load clips
        loadClips();

    } catch (error) {
        showStatus('detectStatus', `Error: ${error.message}`, 'error');
    }
});

// ============================================================================
// STEP 4: Load & Export Clips
// ============================================================================

document.getElementById('loadClipsBtn').addEventListener('click', loadClips);

async function loadClips() {
    if (!selectedProjectId) {
        alert('Please select a project first');
        return;
    }

    try {
        const response = await fetch(`${API_BASE}/clips/${selectedProjectId}`);
        const clips = await response.json();

        const container = document.getElementById('clipList');
        container.innerHTML = '';

        if (clips.length === 0) {
            container.innerHTML = '<p style="color: #999; padding: 15px;">No clips detected yet. Run detection first.</p>';
            return;
        }

        clips.forEach((clip, index) => {
            const reasons = JSON.parse(clip.score_reasons || '[]');

            const div = document.createElement('div');
            div.className = 'clip-item';
            div.innerHTML = `
                <div class="clip-header">
                    <div>
                        <strong>Clip #${index + 1}</strong>
                        <span class="clip-time">${clip.start_time.toFixed(1)}s - ${clip.end_time.toFixed(1)}s (${clip.duration.toFixed(1)}s)</span>
                    </div>
                    <div class="clip-score">Score: ${clip.score.toFixed(1)}</div>
                </div>
                <div class="clip-text">${clip.transcript_text}</div>
                <div class="clip-reasons">
                    <strong>Scoring Reasons:</strong>
                    <ul>
                        ${reasons.map(r => `<li>${r}</li>`).join('')}
                    </ul>
                </div>
                <div class="clip-actions">
                    <button onclick="exportClip(${clip.id}, 'academic')">Export (Academic)</button>
                    <button onclick="exportClip(${clip.id}, 'shorts_friendly')">Export (Shorts)</button>
                    ${clip.exported ? `<span style="color: green; margin-left: 10px;">✓ Exported</span>` : ''}
                </div>
            `;
            container.appendChild(div);
        });

    } catch (error) {
        console.error('Error loading clips:', error);
    }
}

async function exportClip(clipId, preset) {
    try {
        const button = event.target;
        button.disabled = true;
        button.textContent = 'Exporting...';

        const response = await fetch(`${API_BASE}/export/clip/${clipId}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                caption_preset: preset,
                crop_mode: 'center'
            })
        });

        if (!response.ok) {
            throw new Error('Export failed');
        }

        const result = await response.json();

        button.textContent = '✓ Exported';
        button.style.background = '#27ae60';

        alert(`Clip exported successfully!\n\nLocation: ${result.output_path}`);

        // Reload clips to show updated status
        setTimeout(() => loadClips(), 1000);

    } catch (error) {
        alert(`Error exporting clip: ${error.message}`);
        event.target.disabled = false;
        event.target.textContent = 'Export';
    }
}

// Auto-load projects on page load
window.addEventListener('load', () => {
    loadProjects();
});
