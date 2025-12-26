from flask import Flask, render_template, request, redirect, session, url_for
import base64
import hashlib
import json

app = Flask(__name__)
app.secret_key = 'kuib_secret_key_2025'  # Ключ для сесій

# Імітація бази даних (Завдання 2: Admin та User)
users_db = {
    "admin": "admin777",
    "student": "kuib_pass"
}


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if username in users_db and users_db[username] == password:
            session['user'] = username
            return redirect(url_for('dashboard'))
        return "<h3>Помилка: Невірний логін або пароль!</h3><a href='/login'>Спробувати знову</a>"
    return render_template('login.html')


@app.route('/dashboard')
def dashboard():
    if 'user' not in session:
        return redirect(url_for('login'))
    return render_template('dashboard.html', user=session['user'])


@app.route('/pay')
def pay():
    # Завдання 3: Інтеграція LiqPay
    public_key = 'i90804629055'  # Тестовий ключ
    private_key = 'test_private_key'  # Тестовий приватний ключ

    params = {
        "public_key": public_key,
        "version": "3",
        "action": "pay",
        "amount": "100",
        "currency": "UAH",
        "description": "Оплата послуг аудиту ShapKUIB",
        "order_id": "order_001"
    }

    # 1. Base64 JSON
    data = base64.b64encode(json.dumps(params).encode()).decode()
    # 2. Підпис: SHA1(private_key + data + private_key)
    signature_step = private_key + data + private_key
    signature = base64.b64encode(hashlib.sha1(signature_step.encode()).digest()).decode()

    return render_template('pay.html', data=data, signature=signature)


@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('index'))


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)