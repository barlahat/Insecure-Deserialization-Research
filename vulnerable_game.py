import pickle
import base64
import os
from flask import Flask, request, make_response, render_template_string

# הגדרה קריטית: אנחנו קובעים את התיקייה הנוכחית כבסיס
# זה מבטיח שהשרת ימצא את קובץ ה-shell.html שנוצר באותה תיקייה
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__, template_folder=BASE_DIR)


# הגדרת אובייקט השחקן
class Player:
    def __init__(self, username):
        self.username = username
        self.level = 1
        self.coins = 10
        self.is_admin = False


# HTML משודרג עם עיצוב האקרים
HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>The Hacker Store</title>
    <style>
        body { font-family: 'Courier New', monospace; background-color: #0d1117; color: #c9d1d9; text-align: center; padding: 50px; }
        .card { border: 1px solid #30363d; padding: 20px; display: inline-block; background-color: #161b22; border-radius: 10px; min-width: 400px; box-shadow: 0 0 15px #30363d; }
        h1 { color: #58a6ff; text-shadow: 0 0 5px #58a6ff; }
        .stats { color: #79c0ff; font-size: 18px; margin-bottom: 20px; border-bottom: 1px solid #30363d; padding-bottom: 15px; text-align: left; }
        .shop-item { border: 1px solid #d2a8ff; padding: 15px; margin-top: 20px; color: #d2a8ff; background: #1f1f2e; }
        .locked { color: #ff7b72; font-weight: bold; }
        .success { color: #2ea043; font-weight: bold; border: 1px solid #2ea043; padding: 10px; background-color: #0f2d18; }
        a { color: #8b949e; text-decoration: none; font-size: 12px; }
        a:hover { color: #58a6ff; }
    </style>
</head>
<body>
    <div class="card">
        <h1>👾 Player Profile 👾</h1>

        <div class="stats">
            👤 USER: <b>{{ player.username }}</b><br>
            ⭐ LVL: {{ player.level }}<br>
            💰 COINS: {{ player.coins }}<br>
            🛡️ ADMIN: {{ '✅ YES' if player.is_admin else '❌ NO' }}
        </div>

        <div class="shop-item">
            <h3>🏆 The Golden Flag 🏆</h3>
            <p>Price: 1,000,000 Coins</p>

            {% if player.coins >= 1000000 or player.is_admin %}
                <div class="success">
                    🔓 ACCESS GRANTED<br>
                    FLAG: CTF{L0g1c_M4n1pul4t10n_W1n}
                </div>
            {% else %}
                <p class="locked">🔒 INSUFFICIENT FUNDS</p>
            {% endif %}
        </div>

        <br><br>
        <a href="/page/shell.html" target="_blank">[ Try Accessing Backdoor (shell.html) ]</a>
    </div>
</body>
</html>
"""


@app.route('/')
def home():
    user_cookie = request.cookies.get('game_session')
    player = None

    # ניסיון לטעון את המשתמש מהעוגייה
    if user_cookie:
        try:
            # === נקודת התורפה ===
            # השרת מקבל base64 ומבצע pickle.loads בלי בדיקה
            data = base64.b64decode(user_cookie)
            player = pickle.loads(data)
        except:
            pass  # אם העוגייה שבורה או לא תקינה, נתעלם

    # אם אין שחקן (כניסה ראשונה או שגיאה), ניצור אורח
    if not player:
        player = Player("Guest_Noob")
        # סריאליזציה ויצירת עוגייה חדשה
        serialized = pickle.dumps(player)
        cookie_val = base64.b64encode(serialized).decode()

        resp = make_response(render_template_string(HTML_TEMPLATE, player=player))
        resp.set_cookie('game_session', cookie_val)
        return resp

    return render_template_string(HTML_TEMPLATE, player=player)


# === הנתיב שמאפשר את הרצת הדלת האחורית ===
# הנתיב הזה נועד להציג דפים סטטיים, אבל בגלל render_template_string
# הוא יריץ את קוד ה-Python שיש בתוך shell.html
@app.route('/page/<path:filename>')
def show_page(filename):
    # בניית הנתיב המלא לקובץ המבוקש
    file_path = os.path.join(BASE_DIR, filename)

    # בדיקה אם הקובץ קיים
    if not os.path.exists(file_path):
        return f"<h1 style='color:red'>Error 404</h1><p>File not found: {filename}</p><p>Path checked: {file_path}</p>"

    try:
        # קריאת הקובץ כטקסט
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # רינדור הקובץ - כאן ה-SSTI קורה וה-Backdoor רץ!
        return render_template_string(content)

    except Exception as e:
        return f"<h1 style='color:red'>Execution Error</h1><p>{e}</p>"


if __name__ == '__main__':
    print(f"[*] Server is running on http://0.0.0.0:5000")
    print(f"[*] Working directory: {BASE_DIR}")
    app.run(host='0.0.0.0', port=5000)