import json
import base64
import hmac
import hashlib
import os
from flask import Flask, request, make_response, render_template_string

app = Flask(__name__)

# מפתח סודי לחתימה
SECRET_KEY = b"MySuperSecretKey_DoNotShare"


class Player:
    def __init__(self, username, level=1, coins=10, is_admin=False):
        self.username = username
        self.level = level
        self.coins = coins
        self.is_admin = is_admin

    def to_dict(self):
        return {
            "username": self.username,
            "level": self.level,
            "coins": self.coins,
            "is_admin": self.is_admin
        }


def sign_data(data_str):
    return hmac.new(SECRET_KEY, data_str.encode(), hashlib.sha256).hexdigest()


# HTML עם תוספת של אזור התראות אדום
HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Secure Store</title>
    <style>
        body { font-family: 'Courier New', monospace; background-color: #0d1117; color: #c9d1d9; text-align: center; padding: 50px; }
        .card { border: 2px solid #2ea043; padding: 20px; display: inline-block; background-color: #161b22; border-radius: 10px; min-width: 400px; }
        h1 { color: #2ea043; }
        .secure-badge { background-color: #2ea043; color: white; padding: 5px 10px; border-radius: 5px; font-weight: bold; }
        .stats { color: #79c0ff; font-size: 18px; margin-bottom: 20px; border-bottom: 1px solid #30363d; padding-bottom: 15px; text-align: left; }

        /* עיצוב ההתראה האדומה */
        .alert-box {
            background-color: #3d0c0c;
            border: 2px solid #ff0000;
            color: #ff0000;
            padding: 15px;
            margin-bottom: 20px;
            font-weight: bold;
            animation: blink 1s infinite;
        }
        @keyframes blink { 50% { border-color: transparent; } }
    </style>
</head>
<body>
    <div class="card">
        <h1>🛡️ SECURE GAME 🛡️</h1>
        <div class="secure-badge">JSON + HMAC Protected</div>
        <br><br>

        {% if alert %}
            <div class="alert-box">
                🚨 SECURITY ALERT 🚨<br>
                {{ alert }}<br>
                (Attack Blocked & IP Logged)
            </div>
        {% endif %}

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
                <p style="color: green;">FLAG: CTF{S3cur1ty_B3st_Pr4ct1c3s}</p>
            {% else %}
                <p style="color: #ff7b72;">🔒 INSUFFICIENT FUNDS</p>
            {% endif %}
        </div>
    </div>
</body>
</html>
"""


@app.route('/')
def home():
    cookie_value = request.cookies.get('secure_session')
    player_data = None
    alert_msg = None  # משתנה להודעת האבטחה

    if cookie_value:
        try:
            # ניסיון לפענח את העוגייה
            decoded = base64.b64decode(cookie_value).decode()

            # בדיקה ראשונית: האם הפורמט תקין? (מידע::חתימה)
            if "::" not in decoded:
                raise ValueError("Invalid cookie format")

            data_json, signature = decoded.split("::", 1)

            # חישוב חתימה צפויה
            expected_signature = sign_data(data_json)

            # === רגע האמת: השוואת חתימות ===
            if hmac.compare_digest(expected_signature, signature):
                # הכל תקין - טוענים את המשתמש
                data_dict = json.loads(data_json)
                player_data = Player(**data_dict)
            else:
                # === תקיפה זוהתה! ===
                print("[!] SECURITY ALERT: Signature mismatch! Cookie tampering detected.")
                alert_msg = "Data Tampering Detected! Invalid HMAC Signature."

        except Exception as e:
            # תקיפה זוהתה (למשל ניסיון להכניס Pickle במקום JSON)
            print(f"[!] SECURITY ALERT: Malformed Payload. Error: {e}")
            alert_msg = "Malicious Payload Detected! Structure invalid."

    # אם לא הצלחנו לטעון משתמש (כי זו כניסה ראשונה או כי חסמנו תקיפה)
    if not player_data:
        # אנחנו יוצרים משתמש אורח חדש, אבל...
        # אם יש alert_msg, המשתמש יראה את האזהרה האדומה על המסך!
        player_data = Player("Guest_Secure")

        # יצירת עוגייה תקינה חדשה
        data_json = json.dumps(player_data.to_dict())
        signature = sign_data(data_json)
        final_payload = f"{data_json}::{signature}"
        cookie_val = base64.b64encode(final_payload.encode()).decode()

        # אנחנו מעבירים את ה-alert ל-HTML
        resp = make_response(render_template_string(HTML_TEMPLATE, player=player_data, alert=alert_msg))
        resp.set_cookie('secure_session', cookie_val)
        return resp

    return render_template_string(HTML_TEMPLATE, player=player_data, alert=alert_msg)


if __name__ == '__main__':
    print("[*] Secure Server running on port 5001")
    app.run(host='0.0.0.0', port=5001)