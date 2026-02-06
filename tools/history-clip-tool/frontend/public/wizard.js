/**
 * History Clip Tool - Wizard UI Controller
 *
 * Manages the 4-step wizard flow:
 * 1. Upload video
 * 2. Transcribe
 * 3. Review clips
 * 4. Export
 */

const API_BASE = 'http://localhost:8000';

// ============================================================================
// State Management
// ============================================================================

class WizardState {
    constructor() {
        this.currentStep = 1;
        this.projectId = null;
        this.projectName = null;
        this.projectDuration = null;
        this.uploadedFile = null;
        this.selectedModel = 'base';
        this.selectivity = 'medium';  // low, medium, high
        this.clips = [];  // Clips from backend (includes database IDs)
        this.keptClipIndices = new Set();  // Tracks which clips user wants to keep
        this.exportedPaths = [];  // Paths to exported clips
    }

    reset() {
        this.currentStep = 1;
        this.projectId = null;
        this.projectName = null;
        this.projectDuration = null;
        this.uploadedFile = null;
        this.selectedModel = 'base';
        this.selectivity = 'medium';
        this.clips = [];
        this.keptClipIndices.clear();
        this.exportedPaths = [];
    }
}

const state = new WizardState();

// ============================================================================
// Error Handling
// ============================================================================

function showError(message) {
    alert(`Error: ${message}\n\nPlease check the console for details.`);
    console.error(message);
}

// ============================================================================
// Wizard Navigation
// ============================================================================

function goToStep(step) {
    // Hide all steps
    for (let i = 1; i <= 4; i++) {
        document.getElementById(`step-${i}`).style.display = 'none';
        const indicator = document.getElementById(`step-indicator-${i}`);
        indicator.classList.remove('active', 'completed');
    }

    // Show current step
    document.getElementById(`step-${step}`).style.display = 'block';
    document.getElementById(`step-indicator-${step}`).classList.add('active');

    // Mark completed steps
    for (let i = 1; i < step; i++) {
        document.getElementById(`step-indicator-${i}`).classList.add('completed');
    }

    state.currentStep = step;

    // Initialize step-specific UI when entering step 4
    if (step === 4) {
        updateExportStepUI();
    }
}

// ============================================================================
// Step 1: Upload
// ============================================================================

function initUploadStep() {
    const uploadZone = document.getElementById('upload-zone');
    const fileInput = document.getElementById('video-file-input');
    const continueBtn = document.getElementById('btn-continue-upload');

    // Click to browse
    uploadZone.addEventListener('click', () => {
        fileInput.click();
    });

    // File selected
    fileInput.addEventListener('change', async (e) => {
        const file = e.target.files[0];
        if (file) {
            await handleFileUpload(file);
        }
    });

    // Drag and drop
    uploadZone.addEventListener('dragover', (e) => {
        e.preventDefault();
        uploadZone.classList.add('dragover');
    });

    uploadZone.addEventListener('dragleave', () => {
        uploadZone.classList.remove('dragover');
    });

    uploadZone.addEventListener('drop', async (e) => {
        e.preventDefault();
        uploadZone.classList.remove('dragover');

        const file = e.dataTransfer.files[0];
        if (file && file.type.startsWith('video/')) {
            await handleFileUpload(file);
        } else {
            showError('Please drop a video file (MP4, MOV, MKV)');
        }
    });

    // Continue button
    continueBtn.addEventListener('click', () => {
        goToStep(2);
    });
}

async function handleFileUpload(file) {
    try {
        console.log('Uploading file:', file.name);

        // Show uploading state
        document.getElementById('upload-zone').innerHTML = '<div style="padding: 40px;">Uploading...</div>';

        // Create FormData
        const formData = new FormData();
        formData.append('video', file);

        // Upload to backend
        const response = await fetch(`${API_BASE}/projects/?name=${encodeURIComponent(file.name)}`, {
            method: 'POST',
            body: formData
        });

        if (!response.ok) {
            throw new Error(`Upload failed: ${response.statusText}`);
        }

        const project = await response.json();

        // Store project info
        state.projectId = project.id;
        state.projectName = project.name;
        state.projectDuration = project.duration;
        state.uploadedFile = file;

        console.log('Project created:', project);

        // Show success state
        document.getElementById('upload-zone').style.display = 'none';
        document.getElementById('upload-success').style.display = 'flex';
        document.getElementById('uploaded-filename').textContent = file.name;

        // Format duration
        const minutes = Math.floor(project.duration / 60);
        const seconds = Math.floor(project.duration % 60);
        document.getElementById('uploaded-meta').textContent =
            `Duration: ${minutes}:${seconds.toString().padStart(2, '0')} | Size: ${(file.size / 1024 / 1024).toFixed(1)} MB`;

        // Enable continue button
        document.getElementById('btn-continue-upload').disabled = false;

    } catch (error) {
        console.error('Upload error:', error);
        showError(`Failed to upload video: ${error.message}`);

        // Reset upload zone
        document.getElementById('upload-zone').innerHTML = `
            <div class="upload-icon">📁</div>
            <div class="upload-text">Drop your video here or click to browse</div>
            <div class="upload-formats">Supports MP4, MOV, MKV</div>
        `;
    }
}

// ============================================================================
// Step 2: Transcribe
// ============================================================================

function initTranscribeStep() {
    const backBtn = document.getElementById('btn-back-transcribe');
    const startBtn = document.getElementById('btn-start-transcribe');
    const modelRadios = document.querySelectorAll('input[name="model"]');

    // Back button
    backBtn.addEventListener('click', () => {
        goToStep(1);
    });

    // Model selection
    modelRadios.forEach(radio => {
        radio.addEventListener('change', (e) => {
            state.selectedModel = e.target.value;
        });
    });

    // Start transcription
    startBtn.addEventListener('click', async () => {
        await startTranscription();
    });
}

async function startTranscription() {
    try {
        console.log('Starting transcription with model:', state.selectedModel);

        // Hide options
        document.querySelector('.transcribe-options').style.display = 'none';
        document.querySelector('#step-2 .wizard-actions').style.display = 'none';

        // Show progress
        const progressDiv = document.getElementById('transcribe-progress');
        progressDiv.style.display = 'block';

        // Start transcription
        const response = await fetch(
            `${API_BASE}/transcribe/${state.projectId}?model_size=${state.selectedModel}`,
            { method: 'POST' }
        );

        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.detail || 'Transcription failed to start');
        }

        console.log('Transcription started, polling for progress...');

        // Poll for progress
        await pollTranscriptionProgress();

    } catch (error) {
        console.error('Transcription error:', error);
        showError(`Transcription failed: ${error.message}`);

        // Reset UI
        document.querySelector('.transcribe-options').style.display = 'block';
        document.querySelector('#step-2 .wizard-actions').style.display = 'flex';
        document.getElementById('transcribe-progress').style.display = 'none';
    }
}

async function pollTranscriptionProgress() {
    const pollInterval = 2000; // Poll every 2 seconds
    const maxAttempts = 1800; // 60 minutes max (1800 * 2s)
    let attempts = 0;

    return new Promise((resolve, reject) => {
        const interval = setInterval(async () => {
            attempts++;

            try {
                const response = await fetch(`${API_BASE}/ui/transcription-status/${state.projectId}`);

                if (!response.ok) {
                    throw new Error('Failed to check transcription status');
                }

                const status = await response.json();

                // Update progress bar
                const progressPercent = Math.round(status.progress * 100);
                document.getElementById('transcribe-progress-fill').style.width = `${progressPercent}%`;

                console.log(`Transcription progress: ${progressPercent}%`);

                // Check if complete
                if (status.status === 'complete') {
                    clearInterval(interval);
                    console.log('Transcription complete!');

                    // Small delay for visual feedback
                    setTimeout(() => {
                        loadClipsAndGoToReview();
                        resolve();
                    }, 500);
                }

                // Timeout check
                if (attempts >= maxAttempts) {
                    clearInterval(interval);
                    reject(new Error('Transcription timeout - this is taking too long'));
                }

            } catch (error) {
                clearInterval(interval);
                reject(error);
            }
        }, pollInterval);
    });
}

async function loadClipsAndGoToReview() {
    try {
        console.log('Loading clips with selectivity:', state.selectivity);

        const response = await fetch(
            `${API_BASE}/ui/clips/${state.projectId}?selectivity=${state.selectivity}`
        );

        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.detail || 'Failed to load clips');
        }

        const data = await response.json();
        state.clips = data.clips;

        console.log(`Loaded ${state.clips.length} clips`);

        // Go to review step
        goToStep(3);
        renderClipCards();

    } catch (error) {
        console.error('Error loading clips:', error);
        showError(`Failed to load clips: ${error.message}`);
    }
}

// ============================================================================
// Step 3: Review Clips
// ============================================================================

function initReviewStep() {
    const backBtn = document.getElementById('btn-back-review');
    const exportBtn = document.getElementById('btn-export-selected');
    const slider = document.getElementById('selectivity-slider');

    // Back button
    backBtn.addEventListener('click', () => {
        if (confirm('Going back will re-run transcription. Continue?')) {
            goToStep(2);
        }
    });

    // Selectivity slider
    slider.addEventListener('change', async (e) => {
        const value = parseInt(e.target.value);
        const mapping = {1: 'low', 2: 'medium', 3: 'high'};
        state.selectivity = mapping[value];

        console.log('Selectivity changed to:', state.selectivity);
        await reloadClips();
    });

    // Export button
    exportBtn.addEventListener('click', () => {
        if (state.keptClipIndices.size > 0) {
            goToStep(4);
        }
    });
}

async function reloadClips() {
    try {
        // Show loading state
        document.getElementById('clips-grid').innerHTML =
            '<p style="text-align: center; color: #666;">Loading clips...</p>';

        const response = await fetch(
            `${API_BASE}/ui/clips/${state.projectId}?selectivity=${state.selectivity}`
        );

        if (!response.ok) {
            throw new Error('Failed to reload clips');
        }

        const data = await response.json();
        state.clips = data.clips;

        // Clear kept indices (clips may have changed)
        state.keptClipIndices.clear();

        console.log(`Reloaded ${state.clips.length} clips`);

        renderClipCards();

    } catch (error) {
        console.error('Error reloading clips:', error);
        showError(`Failed to reload clips: ${error.message}`);
    }
}

function renderClipCards() {
    const grid = document.getElementById('clips-grid');
    grid.innerHTML = '';

    if (state.clips.length === 0) {
        grid.innerHTML = '<p style="text-align: center; color: #666; padding: 40px;">No clips found. Try moving the selectivity slider to "Keep more".</p>';
        document.getElementById('clips-found-message').textContent = 'No clips found';
        document.getElementById('btn-export-selected').disabled = true;
        return;
    }

    document.getElementById('clips-found-message').textContent = `Found ${state.clips.length} potential clips`;

    state.clips.forEach((clip, index) => {
        const card = createClipCard(clip, index);
        grid.appendChild(card);
    });

    updateExportButton();
}

function createClipCard(clip, index) {
    const card = document.createElement('div');
    card.className = 'clip-card';
    card.id = `clip-card-${index}`;

    if (state.keptClipIndices.has(index)) {
        card.classList.add('kept');
    }

    // Format time
    const formatTime = (seconds) => {
        const mins = Math.floor(seconds / 60);
        const secs = Math.floor(seconds % 60);
        return `${mins}:${secs.toString().padStart(2, '0')}`;
    };

    // Video preview (using time fragment)
    const videoSrc = `${API_BASE}/projects/${state.projectId}/source`;
    const videoFragment = `#t=${clip.start},${clip.end}`;

    card.innerHTML = `
        <div class="clip-header">
            <div class="clip-time">
                ${formatTime(clip.start)} - ${formatTime(clip.end)} (${clip.duration}s)
            </div>
        </div>

        <div class="clip-text">"${clip.preview_text}"</div>

        <div class="clip-reasons">
            <strong>Why this was selected:</strong>
            <ul>
                ${clip.reasons.length > 0
                    ? clip.reasons.map(r => `<li>${r}</li>`).join('')
                    : '<li>Good clip candidate</li>'
                }
            </ul>
        </div>

        <div class="clip-actions">
            <button class="btn-small btn-success" data-index="${index}" data-action="keep">Keep</button>
            <button class="btn-small btn-danger" data-index="${index}" data-action="discard">Discard</button>
        </div>
    `;

    // Add event listeners to buttons
    const keepBtn = card.querySelector('[data-action="keep"]');
    const discardBtn = card.querySelector('[data-action="discard"]');

    keepBtn.addEventListener('click', () => toggleClip(index, true));
    discardBtn.addEventListener('click', () => toggleClip(index, false));

    return card;
}

function toggleClip(index, keep) {
    if (keep) {
        state.keptClipIndices.add(index);
    } else {
        state.keptClipIndices.delete(index);
    }

    // Update card appearance
    const card = document.getElementById(`clip-card-${index}`);
    if (card) {
        if (keep) {
            card.classList.add('kept');
        } else {
            card.classList.remove('kept');
        }
    }

    updateExportButton();
}

function updateExportButton() {
    const btn = document.getElementById('btn-export-selected');
    const count = state.keptClipIndices.size;

    btn.disabled = count === 0;
    btn.textContent = count > 0 ? `Export ${count} Selected` : 'Select clips to export';
}

// ============================================================================
// Step 4: Export
// ============================================================================

function initExportStep() {
    const backBtn = document.getElementById('btn-back-export');
    const exportBtn = document.getElementById('btn-start-export');
    const doneBtn = document.getElementById('btn-done');

    // Back button
    backBtn.addEventListener('click', () => {
        goToStep(3);
    });

    // Export button
    exportBtn.addEventListener('click', async () => {
        await exportClips();
    });

    // Done button (starts new project)
    doneBtn.addEventListener('click', () => {
        if (confirm('Start a new project? Current project will remain saved.')) {
            // Reset state
            state.reset();

            // Reset all UI elements
            resetUploadUI();
            resetTranscribeUI();
            resetReviewUI();
            resetExportUI();

            // Go to step 1
            goToStep(1);
        }
    });
}

function updateExportStepUI() {
    const count = state.keptClipIndices.size;
    document.getElementById('export-count').textContent = count;
}

async function exportClips() {
    try {
        console.log('Exporting clips...');

        // Hide options
        document.querySelector('.export-options').style.display = 'none';
        document.querySelector('#step-4 .wizard-actions').style.display = 'none';

        // Show progress
        const progressDiv = document.getElementById('export-progress');
        progressDiv.style.display = 'block';

        const keptClips = Array.from(state.keptClipIndices).map(index => state.clips[index]);
        const total = keptClips.length;
        let completed = 0;

        state.exportedPaths = [];

        // First, detect clips in backend to get database IDs
        console.log('Detecting clips in backend to get IDs...');
        const detectResponse = await fetch(
            `${API_BASE}/clips/${state.projectId}/detect?min_score=20&max_clips=50`,
            { method: 'POST' }
        );

        if (!detectResponse.ok) {
            throw new Error('Failed to detect clips in backend');
        }

        // Get all clips from backend
        const clipsResponse = await fetch(`${API_BASE}/clips/${state.projectId}`);
        if (!clipsResponse.ok) {
            throw new Error('Failed to get clip IDs');
        }

        const backendClips = await clipsResponse.json();
        console.log(`Got ${backendClips.length} clips from backend`);

        // Export each kept clip
        for (const [arrayIndex, clip] of keptClips.entries()) {
            try {
                // Find matching backend clip by start time
                const backendClip = backendClips.find(
                    bc => Math.abs(bc.start_time - clip.start) < 0.1
                );

                if (!backendClip) {
                    console.warn(`Could not find backend clip for ${clip.start}s, skipping`);
                    continue;
                }

                console.log(`Exporting clip ${backendClip.id}...`);

                // Export the clip
                const exportResponse = await fetch(
                    `${API_BASE}/export/clip/${backendClip.id}`,
                    {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({
                            caption_preset: 'academic',
                            crop_mode: 'center'
                        })
                    }
                );

                if (!exportResponse.ok) {
                    const error = await exportResponse.json();
                    throw new Error(error.detail || 'Export failed');
                }

                const exportResult = await exportResponse.json();
                state.exportedPaths.push(exportResult.output_path);

                completed++;

                // Update progress
                const progress = (completed / total) * 100;
                document.getElementById('export-progress-fill').style.width = `${progress}%`;
                document.getElementById('export-progress-count').textContent = `${completed} of ${total} complete`;

                console.log(`Exported clip ${completed}/${total}`);

            } catch (error) {
                console.error(`Error exporting clip ${arrayIndex}:`, error);
                // Continue with other clips
            }
        }

        if (completed === 0) {
            throw new Error('No clips were exported successfully');
        }

        console.log(`Export complete! ${completed} clips exported.`);
        showExportSuccess();

    } catch (error) {
        console.error('Export error:', error);
        showError(`Export failed: ${error.message}`);

        // Reset UI
        document.querySelector('.export-options').style.display = 'block';
        document.querySelector('#step-4 .wizard-actions').style.display = 'flex';
        document.getElementById('export-progress').style.display = 'none';
    }
}

function showExportSuccess() {
    // Hide progress
    document.getElementById('export-progress').style.display = 'none';

    // Show success
    const successDiv = document.getElementById('export-success');
    successDiv.style.display = 'block';

    // Show export path (use first clip's path directory)
    if (state.exportedPaths.length > 0) {
        const firstPath = state.exportedPaths[0];
        const pathParts = firstPath.split(/[/\\]/);
        pathParts.pop(); // Remove filename
        const exportDir = pathParts.join('/');

        document.getElementById('export-path').textContent = exportDir;

        // Show list of exported files
        const filesDiv = document.getElementById('export-files');
        filesDiv.innerHTML = '<strong>Exported clips:</strong><br>' +
            state.exportedPaths.map(path => {
                const filename = path.split(/[/\\]/).pop();
                return `<div style="padding: 4px 0;">• ${filename}</div>`;
            }).join('');
    }

    // Hide back and export buttons, show done button
    document.getElementById('btn-back-export').style.display = 'none';
    document.getElementById('btn-start-export').style.display = 'none';
    document.getElementById('btn-done').style.display = 'inline-block';
}

// ============================================================================
// UI Reset Functions
// ============================================================================

function resetUploadUI() {
    document.getElementById('upload-zone').style.display = 'block';
    document.getElementById('upload-zone').innerHTML = `
        <div class="upload-icon">📁</div>
        <div class="upload-text">Drop your video here or click to browse</div>
        <div class="upload-formats">Supports MP4, MOV, MKV</div>
    `;
    document.getElementById('upload-success').style.display = 'none';
    document.getElementById('btn-continue-upload').disabled = true;
    document.getElementById('video-file-input').value = '';
}

function resetTranscribeUI() {
    document.querySelector('.transcribe-options').style.display = 'block';
    document.querySelector('#step-2 .wizard-actions').style.display = 'flex';
    document.getElementById('transcribe-progress').style.display = 'none';
    document.getElementById('transcribe-progress-fill').style.width = '0%';

    // Reset to base model
    document.querySelector('input[name="model"][value="base"]').checked = true;
}

function resetReviewUI() {
    document.getElementById('clips-grid').innerHTML = '';
    document.getElementById('selectivity-slider').value = 2;
    document.getElementById('btn-export-selected').disabled = true;
}

function resetExportUI() {
    document.querySelector('.export-options').style.display = 'block';
    document.querySelector('#step-4 .wizard-actions').style.display = 'flex';
    document.getElementById('export-progress').style.display = 'none';
    document.getElementById('export-success').style.display = 'none';
    document.getElementById('export-progress-fill').style.width = '0%';
    document.getElementById('btn-back-export').style.display = 'inline-block';
    document.getElementById('btn-start-export').style.display = 'inline-block';
    document.getElementById('btn-done').style.display = 'none';

    // Reset to YouTube Shorts
    document.querySelector('input[name="platform"][value="youtube"]').checked = true;
}

// ============================================================================
// Initialization
// ============================================================================

document.addEventListener('DOMContentLoaded', () => {
    console.log('History Clip Tool - Initializing...');

    // Initialize all steps
    initUploadStep();
    initTranscribeStep();
    initReviewStep();
    initExportStep();

    // Start at step 1
    goToStep(1);

    console.log('Ready!');
});
