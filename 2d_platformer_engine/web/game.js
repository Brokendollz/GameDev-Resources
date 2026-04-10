// Game configuration
const config = {
    type: Phaser.AUTO,
    width: 1280,
    height: 720,
    parent: 'game-container',
    physics: {
        default: 'arcade',
        arcade: {
            gravity: { y: 800 },
            debug: false
        }
    },
    scene: [GameScene]
};

const game = new Phaser.Game(config);

class GameScene extends Phaser.Scene {
    constructor() {
        super('GameScene');
        this.score = 0;
        this.gameOver = false;
    }

    preload() {
        // Assets are created dynamically
    }

    create() {
        // Set world bounds
        this.physics.world.setBounds(0, 0, 2400, 1400);
        this.cameras.main.setBounds(0, 0, 2400, 1400);

        // Create level
        this.createLevel();

        // Create player
        this.player = this.physics.add.sprite(100, 1000, null);
        this.drawPlayer(this.player);
        this.player.setBounce(0.2);
        this.player.setCollideWorldBounds(false);
        this.player.body.setDrag(0.95);
        this.player.isJumping = false;
        this.player.jumpCharge = 0;
        this.player.moveSpeed = 300;
        this.player.jumpPower = 400;
        this.player.maxJumpPower = 500;

        // Set camera to follow player
        this.cameras.main.startFollow(this.player);

        // Create groups
        this.platforms = this.physics.add.staticGroup();
        this.movingPlatforms = this.physics.add.group();
        this.enemies = this.physics.add.group();
        this.collectibles = this.physics.add.group();

        // Add level objects
        this.levelObjects.platforms.forEach(p => {
            const platform = this.platforms.create(p.x, p.y, null);
            platform.setScale(p.width / 40, 1);
            platform.body.setImmovable(true);
            this.drawRect(platform, p.color || '#64C864');
        });

        this.levelObjects.movingPlatforms.forEach(p => {
            const platform = this.physics.add.sprite(p.x, p.y, null);
            platform.setScale(p.width / 40, 1);
            platform.setBounce(0, 0);
            platform.body.setImmovable(true);
            platform.body.setAllowGravity(false);
            platform.moveDistance = p.moveDistance;
            platform.moveSpeed = p.speed;
            platform.direction = 1;
            platform.startX = p.x;
            this.drawRect(platform, '#9696C8');
            this.movingPlatforms.add(platform);
        });

        this.levelObjects.enemies.forEach(e => {
            const enemy = this.physics.add.sprite(e.x, e.y, null);
            enemy.setScale(0.75, 0.75);
            enemy.setBounce(0, 0);
            enemy.body.setCollideWorldBounds(false);
            enemy.body.setDrag(0.9);
            enemy.patrolDistance = e.patrolDistance;
            enemy.moveSpeed = e.speed;
            enemy.direction = 1;
            enemy.startX = e.x;
            this.drawEnemy(enemy);
            this.enemies.add(enemy);
        });

        this.levelObjects.collectibles.forEach(c => {
            const collectible = this.physics.add.sprite(c.x, c.y, null);
            collectible.setScale(0.5, 0.5);
            collectible.body.setAllowGravity(false);
            collectible.value = c.value;
            collectible.originalY = c.y;
            collectible.bobTime = 0;
            this.drawCollectible(collectible);
            this.collectibles.add(collectible);
        });

        // Collisions
        this.physics.add.collider(this.player, this.platforms);
        this.physics.add.collider(this.player, this.movingPlatforms);
        this.physics.add.collider(this.enemies, this.platforms);
        this.physics.add.collider(this.enemies, this.movingPlatforms);

        // Overlaps
        this.physics.add.overlap(this.player, this.collectibles, this.collectItem, null, this);
        this.physics.add.overlap(this.player, this.enemies, this.hitEnemy, null, this);

        // Input
        this.keys = this.input.keyboard.createCursorKeys();
        this.keys.a = this.input.keyboard.addKey(Phaser.Input.Keyboard.KeyCodes.A);
        this.keys.d = this.input.keyboard.addKey(Phaser.Input.Keyboard.KeyCodes.D);
        this.keys.w = this.input.keyboard.addKey(Phaser.Input.Keyboard.KeyCodes.W);
        this.keys.r = this.input.keyboard.addKey(Phaser.Input.Keyboard.KeyCodes.R);
        this.keys.space = this.input.keyboard.addKey(Phaser.Input.Keyboard.KeyCodes.SPACE);

        // UI Updates
        this.updateUI();
    }

    createLevel() {
        this.levelObjects = {
            platforms: [
                { x: 0, y: 1350, width: 2400, height: 100, color: '#64C864' }
            ],
            movingPlatforms: [
                { x: 1000, y: 950, width: 150, moveDistance: 200, speed: 150 },
                { x: 1300, y: 850, width: 150, moveDistance: 150, speed: 120 }
            ],
            enemies: [
                { x: 700, y: 1250, patrolDistance: 200, speed: 120 },
                { x: 1700, y: 1000, patrolDistance: 200, speed: 120 },
                { x: 1900, y: 1000, patrolDistance: 200, speed: 120 }
            ],
            collectibles: [
                { x: 250, y: 1270, value: 10 },
                { x: 500, y: 1220, value: 10 },
                { x: 750, y: 1170, value: 10 },
                { x: 1100, y: 920, value: 15 },
                { x: 1400, y: 820, value: 15 },
                { x: 1750, y: 970, value: 20 },
                { x: 2000, y: 1250, value: 25 }
            ]
        };

        // Add more platforms for a complete level
        const staticPlatforms = [
            { x: 200, y: 1300, width: 150, height: 20 },
            { x: 450, y: 1250, width: 150, height: 20 },
            { x: 700, y: 1200, width: 150, height: 20 },
            { x: 950, y: 1150, width: 150, height: 20 },
            { x: 1600, y: 1250, width: 300, height: 20 },
            { x: 2000, y: 1300, width: 80, height: 20 },
            { x: 2100, y: 1250, width: 80, height: 20 },
            { x: 2200, y: 1200, width: 80, height: 20 }
        ];

        staticPlatforms.forEach(p => {
            this.levelObjects.platforms.push(p);
        });
    }

    update() {
        if (this.gameOver) return;

        // Player movement
        this.player.setVelocityX(0);

        if (this.keys.a.isDown || this.keys.left.isDown) {
            this.player.setVelocityX(-this.player.moveSpeed);
            this.player.direction = -1;
        }
        if (this.keys.d.isDown || this.keys.right.isDown) {
            this.player.setVelocityX(this.player.moveSpeed);
            this.player.direction = 1;
        }

        // Jump logic
        if ((this.keys.space.isDown || this.keys.w.isDown || this.keys.up.isDown) && !this.player.isJumping) {
            if (this.player.body.touching.down) {
                this.player.isJumping = true;
                this.player.jumpCharge = 0;
            }
        }

        if (this.player.isJumping) {
            if (this.player.body.touching.down) {
                this.player.jumpCharge += this.player.jumpPower * 3 * 0.016;
                this.player.jumpCharge = Math.min(this.player.jumpCharge, this.player.maxJumpPower);
            } else {
                this.player.setVelocityY(-this.player.jumpCharge);
                this.player.isJumping = false;
            }
        }

        // Reset on R
        if (this.keys.r.isDown) {
            this.scene.restart();
        }

        // Update moving platforms
        this.movingPlatforms.children.entries.forEach(platform => {
            platform.x += platform.moveSpeed * platform.direction * 0.016;

            if (platform.x < platform.startX - platform.moveDistance ||
                platform.x > platform.startX + platform.moveDistance) {
                platform.direction *= -1;
            }
        });

        // Update enemies
        this.enemies.children.entries.forEach(enemy => {
            enemy.setVelocityX(enemy.moveSpeed * enemy.direction);

            if (enemy.x < enemy.startX - enemy.patrolDistance ||
                enemy.x > enemy.startX + enemy.patrolDistance) {
                enemy.direction *= -1;
            }
        });

        // Update collectibles
        this.collectibles.children.entries.forEach(collectible => {
            collectible.bobTime += 0.016;
            collectible.y = collectible.originalY + Math.sin(collectible.bobTime * 3) * 5;
        });

        // Redraw player to show direction
        this.drawPlayer(this.player);

        // Check if player fell
        if (this.player.y > 1500) {
            this.endGame();
        }

        // Update UI
        this.updateUI();
    }

    collectItem(player, collectible) {
        this.score += collectible.value;
        collectible.destroy();
    }

    hitEnemy(player, enemy) {
        player.setVelocityY(-300);
        player.y -= 10;
    }

    endGame() {
        this.gameOver = true;
        this.showGameOverScreen();
    }

    showGameOverScreen() {
        const modal = document.createElement('div');
        modal.className = 'game-over-screen';
        modal.innerHTML = `
            <div class="game-over-content">
                <h2>GAME OVER</h2>
                <p>נקודות סופיות: ${this.score}</p>
                <button onclick="location.reload()">משחק חדש</button>
            </div>
        `;
        document.body.appendChild(modal);
    }

    updateUI() {
        document.getElementById('score').textContent = this.score;
        document.getElementById('fps').textContent = Math.round(this.game.loop.actualFps);
        document.getElementById('height').textContent = Math.max(0, Math.round(1350 - this.player.y));
    }

    // Drawing utilities
    drawPlayer(sprite) {
        const graphics = this.make.graphics({ x: 0, y: 0, add: false });
        graphics.fillStyle(0x6496FF, 1);
        graphics.fillRect(0, 0, 40, 60);

        // Eyes
        graphics.fillStyle(0xFFFFFF, 1);
        graphics.fillCircle(10, 15, 3);
        graphics.fillCircle(30, 15, 3);

        // Direction indicator
        graphics.lineStyle(2, 0xFF6464, 1);
        if (this.player.direction > 0) {
            graphics.lineBetween(30, 50, 40, 50);
        } else {
            graphics.lineBetween(10, 50, 0, 50);
        }

        graphics.generateTexture('player', 40, 60);
        graphics.destroy();
        sprite.setTexture('player');
    }

    drawEnemy(sprite) {
        const graphics = this.make.graphics({ x: 0, y: 0, add: false });
        graphics.fillStyle(0xFF6464, 1);
        graphics.fillRect(0, 0, 30, 30);

        graphics.fillStyle(0xFFFFFF, 1);
        graphics.fillCircle(8, 8, 2);
        graphics.fillCircle(22, 8, 2);

        graphics.generateTexture('enemy', 30, 30);
        graphics.destroy();
        sprite.setTexture('enemy');
    }

    drawCollectible(sprite) {
        const graphics = this.make.graphics({ x: 0, y: 0, add: false });
        graphics.fillStyle(0xFFFF64, 1);

        // Draw star
        const centerX = 10, centerY = 10, radius = 8;
        const points = [];
        for (let i = 0; i < 10; i++) {
            const angle = (i * Math.PI / 5) - Math.PI / 2;
            const r = i % 2 === 0 ? radius : radius * 0.4;
            const x = centerX + r * Math.cos(angle);
            const y = centerY + r * Math.sin(angle);
            points.push(x, y);
        }
        graphics.fillPoints(points);

        graphics.generateTexture('collectible', 20, 20);
        graphics.destroy();
        sprite.setTexture('collectible');
    }

    drawRect(sprite, color) {
        const graphics = this.make.graphics({ x: 0, y: 0, add: false });
        graphics.fillStyle(parseInt(color.replace('#', '0x')), 1);
        graphics.fillRect(0, 0, 40, 20);
        graphics.lineStyle(2, 0xFFFFFF, 1);
        graphics.strokeRect(0, 0, 40, 20);

        graphics.generateTexture('rect_' + color, 40, 20);
        graphics.destroy();
        sprite.setTexture('rect_' + color);
    }
}
