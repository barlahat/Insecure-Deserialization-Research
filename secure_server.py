import json
import base64
from flask import Flask, request, make_response

app = Flask(__name__)


@app.route('/')
def index():
    user_cookie = request.cookies.get('user_data')

    if user_cookie:
        try:
            # שלב 1: פענוח מ-Base64
            decoded_data = base64.b64decode(user_cookie).decode('utf-8')

            # שלב 2: שימוש ב-JSON במקום ב-Pickle
            # JSON הוא פורמט מידע בלבד, הוא לא יכול להריץ קוד!
            user_obj = json.loads(decoded_data)

            return f"<h1>Welcome back (SECURE), {user_obj['username']}!</h1>"
        except Exception as e:
            return f"Error loading user: {e}"

    # יצירת משתמש אורח חדש בצורה מאובטחת
    response = make_response("<h1>Welcome Guest! You are mostly secure now.</h1>")
    guest_user = {'username': 'Guest', 'role': 'user'}

    # שימוש ב-JSON לסריאליזציה
    json_data = json.dumps(guest_user)
    cookie_value = base64.b64encode(json_data.encode()).decode()

    response.set_cookie('user_data', cookie_value)
    return response


if __name__ == '__main__':
    app.run(port=5001)  # נריץ בפורט אחר (5001) כדי לא להתנגש