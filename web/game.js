const START_STATE = [8, 7, 6, 5, 4, 3, 2, 1, 0];
const TARGET_STATE = [0, 1, 2, 3, 4, 5, 6, 7, 8];

let currentState = [...START_STATE];
let isAnimating = false;
let isSimulationPaused = false;

// DOM Elements
const boardEl = document.getElementById('board');
const statusEl = document.getElementById('status-message');
const btnBfs = document.getElementById('btn-bfs');
const btnAstar = document.getElementById('btn-astar');
const btnPause = document.getElementById('btn-pause');
const btnReset = document.getElementById('btn-reset');
const btnShuffle = document.getElementById('btn-shuffle');

const metricExpansions = document.getElementById('metric-expansions');
const metricMemory = document.getElementById('metric-memory');
const metricMoves = document.getElementById('metric-moves');
const metricTime = document.getElementById('metric-time');

// Configuration
const SIZE = 3;

// Helper to calculate pixel position based on row and col
function getPosition(index) {
    const row = Math.floor(index / SIZE);
    const col = index % SIZE;
    const tileSize = parseInt(getComputedStyle(document.documentElement).getPropertyValue('--tile-size'));
    const gapSize = parseInt(getComputedStyle(document.documentElement).getPropertyValue('--gap-size'));
    const padding = parseInt(getComputedStyle(document.documentElement).getPropertyValue('--board-padding'));
    
    return {
        x: padding + col * (tileSize + gapSize),
        y: padding + row * (tileSize + gapSize)
    };
}

// Initialize the board UI
function initBoard() {
    boardEl.innerHTML = '';
    
    for (let i = 1; i < SIZE * SIZE; i++) {
        const tile = document.createElement('div');
        tile.className = 'tile';
        tile.id = `tile-${i}`;
        tile.innerText = i;
        tile.addEventListener('click', () => handleTileClick(i));
        boardEl.appendChild(tile);
    }
    
    renderBoard();
}

// Update tile positions based on current state
function renderBoard() {
    for (let i = 0; i < currentState.length; i++) {
        const tileNumber = currentState[i];
        if (tileNumber === 0) continue; // Blank space has no tile
        
        const tileEl = document.getElementById(`tile-${tileNumber}`);
        const pos = getPosition(i);
        
        tileEl.style.transform = `translate(${pos.x}px, ${pos.y}px)`;
        
        // Check if tile is in its target position
        if (currentState[i] === TARGET_STATE[i]) {
            tileEl.classList.add('correct');
        } else {
            tileEl.classList.remove('correct');
        }
    }
}

// Handle user clicking a tile
function handleTileClick(tileNumber) {
    if (isAnimating) return;
    
    const tileIndex = currentState.indexOf(tileNumber);
    const blankIndex = currentState.indexOf(0);
    
    // Check if adjacent
    const tileRow = Math.floor(tileIndex / SIZE);
    const tileCol = tileIndex % SIZE;
    const blankRow = Math.floor(blankIndex / SIZE);
    const blankCol = blankIndex % SIZE;
    
    const isAdjacent = Math.abs(tileRow - blankRow) + Math.abs(tileCol - blankCol) === 1;
    
    if (isAdjacent) {
        // Swap
        currentState[blankIndex] = tileNumber;
        currentState[tileIndex] = 0;
        renderBoard();
        checkWin();
    }
}

function checkWin() {
    if (currentState.join(',') === TARGET_STATE.join(',')) {
        statusEl.innerText = 'Puzzle Solved!';
        statusEl.style.color = '#10b981';
    } else {
        statusEl.innerText = 'Ready';
        statusEl.style.color = '#cbd5e1';
    }
}

// API Call to solve
async function solve(algorithm) {
    if (isAnimating) return;
    
    setLoading(true, `Solving with ${algorithm.toUpperCase()}...`);
    
    try {
        const response = await fetch('/api/solve', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                start: currentState,
                algorithm: algorithm
            })
        });
        
        const data = await response.json();
        
        if (data.error) {
            setLoading(false);
            statusEl.innerText = 'Error: ' + data.error;
            statusEl.style.color = '#ef4444';
            return;
        }
        
        if (!data.found) {
            setLoading(false);
            statusEl.innerText = 'No solution found!';
            statusEl.style.color = '#ef4444';
            return;
        }
        
        // Setup initial metrics at 0
        metricExpansions.innerText = '0';
        metricMemory.innerText = '0';
        metricMoves.innerText = '0';
        metricTime.innerText = data.elapsed_seconds.toFixed(4); // Time is instant
        
        // Animate path with data
        await animatePath(data);
        
    } catch (err) {
        setLoading(false);
        statusEl.innerText = 'Connection error!';
        statusEl.style.color = '#ef4444';
        console.error(err);
    }
}

async function animatePath(data) {
    const path = data.path;
    isAnimating = true;
    isSimulationPaused = false;
    
    // Show pause button
    btnPause.style.display = 'block';
    btnPause.innerText = 'Pause Simulation';
    statusEl.innerText = 'Animating solution...';
    
    const totalSteps = path.length - 1;
    
    // Skip the first state since it's the current one
    for (let i = 1; i < path.length; i++) {
        // Wait if paused
        while (isSimulationPaused) {
            await new Promise(r => setTimeout(r, 100));
        }
        
        currentState = path[i];
        renderBoard();
        
        // Interpolate metrics for this step
        const stepRatio = i / totalSteps;
        const currentExpansions = Math.round(data.expansions * stepRatio);
        const currentMemory = Math.round(data.max_nodes_in_memory * stepRatio);
        
        metricExpansions.innerText = currentExpansions.toLocaleString();
        metricMemory.innerText = currentMemory.toLocaleString();
        metricMoves.innerText = i;
        
        // Wait 300ms between moves
        await new Promise(r => setTimeout(r, 300));
    }
    
    isAnimating = false;
    isSimulationPaused = false;
    btnPause.style.display = 'none';
    setLoading(false);
    checkWin();
}

function setLoading(isLoading, message = '') {
    const buttons = [btnBfs, btnAstar, btnReset, btnShuffle];
    buttons.forEach(btn => btn.disabled = isLoading);
    
    if (isLoading) {
        statusEl.innerText = message;
    }
}

// Shuffle by making random legal moves
function shuffle() {
    if (isAnimating) return;
    let moves = 50; // number of random moves
    
    for (let i = 0; i < moves; i++) {
        const blankIndex = currentState.indexOf(0);
        const blankRow = Math.floor(blankIndex / SIZE);
        const blankCol = blankIndex % SIZE;
        
        const possibleMoves = [];
        if (blankRow > 0) possibleMoves.push(blankIndex - SIZE); // Up
        if (blankRow < SIZE - 1) possibleMoves.push(blankIndex + SIZE); // Down
        if (blankCol > 0) possibleMoves.push(blankIndex - 1); // Left
        if (blankCol < SIZE - 1) possibleMoves.push(blankIndex + 1); // Right
        
        const randomMoveIndex = possibleMoves[Math.floor(Math.random() * possibleMoves.length)];
        currentState[blankIndex] = currentState[randomMoveIndex];
        currentState[randomMoveIndex] = 0;
    }
    
    renderBoard();
    
    // Clear metrics
    metricExpansions.innerText = '-';
    metricMemory.innerText = '-';
    metricMoves.innerText = '-';
    metricTime.innerText = '-';
    statusEl.innerText = 'Shuffled';
}

// Event Listeners
btnBfs.addEventListener('click', () => solve('bfs'));
btnAstar.addEventListener('click', () => solve('astar'));

btnPause.addEventListener('click', () => {
    if (!isAnimating) return;
    isSimulationPaused = !isSimulationPaused;
    if (isSimulationPaused) {
        btnPause.innerText = 'Resume Simulation';
        statusEl.innerText = 'Simulation Paused';
    } else {
        btnPause.innerText = 'Pause Simulation';
        statusEl.innerText = 'Animating solution...';
    }
});

btnReset.addEventListener('click', () => {
    if (isAnimating && !isSimulationPaused) return; // Prevent reset during active animation unless paused
    isAnimating = false;
    isSimulationPaused = false;
    btnPause.style.display = 'none';
    
    currentState = [...START_STATE];
    renderBoard();
    
    metricExpansions.innerText = '-';
    metricMemory.innerText = '-';
    metricMoves.innerText = '-';
    metricTime.innerText = '-';
    statusEl.innerText = 'Ready';
});

btnShuffle.addEventListener('click', shuffle);

// Initial setup
// Slight delay to ensure CSS variables are loaded
setTimeout(() => {
    initBoard();
}, 100);
