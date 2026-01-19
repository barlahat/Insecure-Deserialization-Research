import pickle
import base64
from flask import Flask, request, make_response, render_template_string

app = Flask(__name__)


# דף הבית
@app.route('/')
def index():
    user_cookie = request.cookies.get('user_data')

    if user_cookie:
        try:
            # שלב 1: פענוח מ-Base64
            decoded_data = base64.b64decode(user_cookie)

            # שלב 2: דה-סריאליזציה לא בטוחה באמצעות pickle
            # כאן החולשה! השרת טוען אובייקט לא מוכר
            user_obj = pickle.loads(decoded_data)

            return f"<h1>Welcome back, {user_obj['username']}!</h1>"
        except Exception as e:
            return f"Error: {e}"

    # אם אין עוגייה, ניצור משתמש אורח
    response = make_response("<h1>Welcome Guest! I gave you a cookie. Reload the page.</h1>")

    # יצירת אובייקט לגיטימי
    guest_user = {'username': 'Guest', 'role': 'user'}

    # סריאליזציה (הפיכה לבייטים) וקידוד ל-Base64
    serialized_data = pickle.dumps(guest_user)
    cookie_value = base64.b64encode(serialized_data).decode()

    response.set_cookie('user_data', cookie_value)
    return response


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)