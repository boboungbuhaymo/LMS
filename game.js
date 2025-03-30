// Game configuration
const config = {
    width: 800,
    height: 600,
    backgroundColor: 0x0f172a,
    playerSpeed: 5,
    bulletSpeed: 7,
    enemySpeed: 2,
    asteroidSpeed: 1.5,
    spawnRate: 60,
    particleCount: 20,
    particleSpeed: 2,
    particleSize: 3
};

// Game state
let gameState = {
    score: 0,
    lives: 3,
    gameOver: false,
    soundOn: true,
    fullscreen: false,
    keys: {
        left: false,
        right: false,
        up: false,
        down: false,
        space: false
    }
};

// Game objects
let player = {
    x: config.width / 2,
    y: config.height - 100,
    width: 50,
    height: 50,
    color: '#8b5cf6'
};

let bullets = [];
let enemies = [];
let asteroids = [];
let particles = [];
let lastSpawn = 0;
let animationId = null;

// DOM elements
const canvas = document.getElementById('gameCanvas');
const ctx = canvas.getContext('2d');
const scoreElement = document.getElementById('score');
const livesElement = document.getElementById('lives');
const gameOverElement = document.getElementById('gameOver');
const finalScoreElement = document.getElementById('finalScore');
const startScreenElement = document.getElementById('startScreen');
const startBtn = document.getElementById('startBtn');
const restartBtn = document.getElementById('restartBtn');
const soundBtn = document.getElementById('soundBtn');
const fullscreenBtn = document.getElementById('fullscreenBtn');

// Initialize game
function init() {
    canvas.width = config.width;
    canvas.height = config.height;
    
    // Event listeners
    window.addEventListener('keydown', handleKeyDown);
    window.addEventListener('keyup', handleKeyUp);
    startBtn.addEventListener('click', startGame);
    restartBtn.addEventListener('click', restartGame);
    soundBtn.addEventListener('click', toggleSound);
    fullscreenBtn.addEventListener('click', toggleFullscreen);
    
    // Draw initial screen
    drawStartScreen();
}

// Start game
function startGame() {
    startScreenElement.classList.add('hidden');
    resetGame();
    gameLoop();
}

// Game loop
function gameLoop() {
    if (gameState.gameOver) return;
    
    update();
    render();
    
    animationId = requestAnimationFrame(gameLoop);
}

// Update game state
function update() {
    // Update player position
    if (gameState.keys.left && player.x > 0) player.x -= config.playerSpeed;
    if (gameState.keys.right && player.x < config.width - player.width) player.x += config.playerSpeed;
    if (gameState.keys.up && player.y > 0) player.y -= config.playerSpeed;
    if (gameState.keys.down && player.y < config.height - player.height) player.y += config.playerSpeed;

    // Fire bullets
    if (gameState.keys.space && Date.now() - lastSpawn > 300) {
        bullets.push({
            x: player.x + player.width / 2 - 2.5,
            y: player.y,
            width: 5,
            height: 15,
            color: '#f59e0b'
        });
        lastSpawn = Date.now();
    }

    // Update bullets
    bullets.forEach((bullet, index) => {
        bullet.y -= config.bulletSpeed;
        if (bullet.y < 0) {
            bullets.splice(index, 1);
        }
    });

    // Spawn enemies
    if (Math.random() < 0.01) {
        enemies.push({
            x: Math.random() * (config.width - 40),
            y: -40,
            width: 40,
            height: 40,
            color: '#ef4444',
            health: 2
        });
    }

    // Update enemies
    enemies.forEach((enemy, eIndex) => {
        enemy.y += config.enemySpeed;

        // Check collision with player
        if (checkCollision(player, enemy)) {
            enemies.splice(eIndex, 1);
            gameState.lives--;
            livesElement.textContent = gameState.lives;
            if (gameState.lives <= 0) {
                gameOver();
            }
            return;
        }

        // Check collision with bullets
        bullets.forEach((bullet, bIndex) => {
            if (checkCollision(bullet, enemy)) {
                bullets.splice(bIndex, 1);
                enemy.health--;
                if (enemy.health <= 0) {
                    enemies.splice(eIndex, 1);
                    gameState.score += 100;
                    scoreElement.textContent = gameState.score;
                    createParticles(enemy.x, enemy.y, enemy.width, enemy.height, '#ef4444');
                }
            }
        });

        if (enemy.y > config.height) {
            enemies.splice(eIndex, 1);
        }
    });

    // Spawn asteroids
    if (Math.random() < 0.005) {
        const size = 20 + Math.random() * 30;
        asteroids.push({
            x: Math.random() * (config.width - size),
            y: -size,
            width: size,
            height: size,
            color: '#64748b',
            speedX: (Math.random() - 0.5) * 2,
            speedY: config.asteroidSpeed
        });
    }

    // Update asteroids
    asteroids.forEach((asteroid, aIndex) => {
        asteroid.x += asteroid.speedX;
        asteroid.y += asteroid.speedY;

        // Check collision with player
        if (checkCollision(player, asteroid)) {
            asteroids.splice(aIndex, 1);
            gameState.lives--;
            livesElement.textContent = gameState.lives;
            createParticles(asteroid.x, asteroid.y, asteroid.width, asteroid.height, '#64748b');
            if (gameState.lives <= 0) {
                gameOver();
            }
            return;
        }

        // Check collision with bullets
        bullets.forEach((bullet, bIndex) => {
            if (checkCollision(bullet, asteroid)) {
                bullets.splice(bIndex, 1);
                asteroids.splice(aIndex, 1);
                gameState.score += 50;
                scoreElement.textContent = gameState.score;
                createParticles(asteroid.x, asteroid.y, asteroid.width, asteroid.height, '#64748b');
            }
        });

        if (asteroid.y > config.height || asteroid.x < -asteroid.width || asteroid.x > config.width) {
            asteroids.splice(aIndex, 1);
        }
    });

    // Update particles
    particles.forEach((particle, pIndex) => {
        particle.x += particle.speedX;
        particle.y += particle.speedY;
        particle.alpha -= 0.01;
        if (particle.alpha <= 0) {
            particles.splice(pIndex, 1);
        }
    });
}

// Render game
function render() {
    // Clear canvas
    ctx.fillStyle = `rgb(15, 23, 42)`;
    ctx.fillRect(0, 0, config.width, config.height);

    // Draw player
    ctx.fillStyle = player.color;
    ctx.fillRect(player.x, player.y, player.width, player.height);

    // Draw bullets
    bullets.forEach(bullet => {
        ctx.fillStyle = bullet.color;
        ctx.fillRect(bullet.x, bullet.y, bullet.width, bullet.height);
    });

    // Draw enemies
    enemies.forEach(enemy => {
        ctx.fillStyle = enemy.color;
        ctx.fillRect(enemy.x, enemy.y, enemy.width, enemy.height);
    });

    // Draw asteroids
    asteroids.forEach(asteroid => {
        ctx.fillStyle = asteroid.color;
        ctx.beginPath();
        ctx.arc(asteroid.x + asteroid.width/2, asteroid.y + asteroid.height/2, asteroid.width/2, 0, Math.PI * 2);
        ctx.fill();
    });

    // Draw particles
    particles.forEach(particle => {
        ctx.globalAlpha = particle.alpha;
        ctx.fillStyle = particle.color;
        ctx.fillRect(particle.x, particle.y, particle.size, particle.size);
        ctx.globalAlpha = 1;
    });
}

// Helper functions
function checkCollision(obj1, obj2) {
    return obj1.x < obj2.x + obj2.width &&
           obj1.x + obj1.width > obj2.x &&
           obj1.y < obj2.y + obj2.height &&
           obj1.y + obj1.height > obj2.y;
}

function createParticles(x, y, width, height, color) {
    for (let i = 0; i < config.particleCount; i++) {
        particles.push({
            x: x + Math.random() * width,
            y: y + Math.random() * height,
            size: Math.random() * config.particleSize + 1,
            color: color,
            speedX: (Math.random() - 0.5) * config.particleSpeed * 2,
            speedY: (Math.random() - 0.5) * config.particleSpeed * 2,
            alpha: 1
        });
    }
}

function handleKeyDown(e) {
    if (e.key === 'ArrowLeft') gameState.keys.left = true;
    if (e.key === 'ArrowRight') gameState.keys.right = true;
    if (e.key === 'ArrowUp') gameState.keys.up = true;
    if (e.key === 'ArrowDown') gameState.keys.down = true;
    if (e.key === ' ') gameState.keys.space = true;
}

function handleKeyUp(e) {
    if (e.key === 'ArrowLeft') gameState.keys.left = false;
    if (e.key === 'ArrowRight') gameState.keys.right = false;
    if (e.key === 'ArrowUp') gameState.keys.up = false;
    if (e.key === 'ArrowDown') gameState.keys.down = false;
    if (e.key === ' ') gameState.keys.space = false;
}

function drawStartScreen() {
    ctx.fillStyle = `rgba(15, 23, 42, 0.8)`;
    ctx.fillRect(0, 0, config.width, config.height);
}

function resetGame() {
    player.x = config.width / 2;
    player.y = config.height - 100;
    bullets = [];
    enemies = [];
    asteroids = [];
    particles = [];
    gameState.score = 0;
    gameState.lives = 3;
    gameState.gameOver = false;
    scoreElement.textContent = gameState.score;
    livesElement.textContent = gameState.lives;
    gameOverElement.classList.add('hidden');
}

function gameOver() {
    gameState.gameOver = true;
    cancelAnimationFrame(animationId);
    gameOverElement.classList.remove('hidden');
    finalScoreElement.textContent = gameState.score;
}

function restartGame() {
    gameOverElement.classList.add('hidden');
    resetGame();
    gameLoop();
}

function toggleSound() {
    gameState.soundOn = !gameState.soundOn;
    soundBtn.innerHTML = gameState.soundOn ? '<i class="fas fa-volume-up"></i>' : '<i class="fas fa-volume-mute"></i>';
}

function toggleFullscreen() {
    if (!document.fullscreenElement) {
        canvas.requestFullscreen().catch(err => {
            console.error(`Error attempting to enable fullscreen: ${err.message}`);
        });
    } else {
        document.exitFullscreen();
    }
}

// Start the game
init();