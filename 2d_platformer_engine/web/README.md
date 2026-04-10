# גרסת ווב - משחק Platformer 2D

גרסה אינטראקטיבית של מנוע ה-Platformer בדפדפן! משחק מלא עם פיזיקה, אויבים, וקולקטיבלים.

## הפעלה מהירה

### אפשרות 1: השתמש בשרתן Python (המלצה)

```bash
cd web
python server.py
```

ואז פתח את: **http://localhost:8000**

### אפשרות 2: שרת HTTP רגיל

```bash
cd web
python -m http.server 8000
```

### אפשרות 3: Live Server (אם יש לך VS Code)

1. התקן את Live Server extension
2. Right-click על `index.html`
3. בחר "Open with Live Server"

## בקרים

| כפתור | פעולה |
|------|-------|
| **A** / **←** | תנועה שמאלה |
| **D** / **→** | תנועה ימינה |
| **Space** / **W** / **↑** | קפיצה |
| **R** | ריסט המשחק |

## תכונות

✨ **מנוע Phaser 3** - גרסת ווב מלאה
🎮 **פיזיקה מציאותית** - כוח משיכה והתנגשויות
👾 **אויבים חכמים** - נעים בתבנית סדורה
💎 **קולקטיבלים** - אזרים בעלי ערך נקודות
📱 **עיצוב רספונסיבי** - עובד גם בטלפון

## קבצים

- `index.html` - HTML עיקרי
- `styles.css` - עיצובים ותעונים
- `game.js` - הלוגיקה של המשחק
- `server.py` - שרתן HTTP Python
- `README.md` - קובץ זה

## טכנולוגיה

- **Phaser 3** - מנוע משחקים לדפדפן
- **HTML5 Canvas** - rendering
- **Vanilla JavaScript** - קוד המשחק

## פיתוח

### הוספת רמה חדשה

ערוך את הפונקציה `createLevel()` ב-`game.js`:

```javascript
createLevel() {
    this.levelObjects = {
        platforms: [
            { x: 0, y: 1350, width: 2400, height: 100 }
        ],
        enemies: [
            { x: 700, y: 1250, patrolDistance: 200, speed: 120 }
        ],
        collectibles: [
            { x: 250, y: 1270, value: 10 }
        ]
    };
}
```

### התאמת הגדרות פיזיקה

בתוך `create()`:

```javascript
this.player.moveSpeed = 300;      // מהירות תנועה
this.player.jumpPower = 400;      // כוח קפיצה
this.player.maxJumpPower = 500;   // קפיצה מקסימלית
```

## ביצועים

- 60 FPS בדפדפרים מודרניים
- Viewport culling ל-optimization
- Rendering דינמי של sprites

## ברausen Compatibility

✅ Chrome/Chromium
✅ Firefox
✅ Safari
✅ Edge
⚠️ Internet Explorer (לא תומך)

## עוד עזרה

עיין ב-`../README.md` לתיעוד מלא של מנוע ה-Platformer.

---

**Made with ❤️ using Phaser 3**
