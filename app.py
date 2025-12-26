from flask import Flask, render_template, request, redirect, session, url_for
import base64
import hashlib
import json

app = Flask(__name__)
app.secret_key = 'kuib_secret_key_2025'

# База даних у пам'яті (скидається при перезавантаженні Render)
users_db = {
    "admin": "admin777"
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
        return "<h3>Помилка: Невірний логін!</h3><a href='/login'>Назад</a>"
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if username in users_db:
            return "<h3>Користувач вже існує!</h3><a href='/register'>Назад</a>"
        users_db[username] = password
        return "<h3>Реєстрація успішна!</h3><a href='/login'>Увійти</a>"
    return render_template('register.html')

@app.route('/dashboard')
def dashboard():
    if 'user' not in session:
        return redirect(url_for('login'))
    return render_template('dashboard.html', user=session['user'])

@app.route('/pay')
def pay():
    public_key = 'i90804629055' # Тестовий ключ
    private_key = 'test_private_key'
    params = {
        "public_key": public_key, "version": "3", "action": "pay",
        "amount": "100", "currency": "UAH", "description": "Audit ShapKUIB",
        "order_id": "order_123"
    }
    data = base64.b64encode(json.dumps(params).encode()).decode()
    signature = base64.b64encode(hashlib.sha1((private_key + data + private_key).encode()).digest()).decode()
    return render_template('pay.html', data=data, signature=signature)

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
