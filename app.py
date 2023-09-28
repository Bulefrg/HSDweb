from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, validators
import sqlite3
from test import parse_news
from settings import parse_status_page
from shop import scrape_image_urls
import json



app = Flask(__name__)
app.config['SECRET_KEY'] = '123456'

conn = sqlite3.connect('users.db')
cursor = conn.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT NOT NULL UNIQUE,
                    password TEXT NOT NULL
                )''')

# Создаем таблицу для комментариев
cursor.execute('''CREATE TABLE IF NOT EXISTS comments (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    comment TEXT NOT NULL,

                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users (id)
                )''')

conn.commit()
conn.close()

login_manager = LoginManager(app)
login_manager.login_view = 'login'


class User(UserMixin):
    def __init__(self, user_id, username, password):
        self.id = user_id
        self.username = username
        self.password = password


@login_manager.user_loader
def load_user(user_id):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE id = ?', (user_id,))
    user_data = cursor.fetchone()
    conn.close()

    if user_data:
        return User(user_data[0], user_data[1], user_data[2])
    return None


class LoginForm(FlaskForm):
    username = StringField('Имя', [validators.DataRequired()])
    password = PasswordField('Пароль', [validators.DataRequired()])
    submit = SubmitField('Войти')


@app.route('/base')
def base():
    return render_template('base.html')


@app.route('/main')
def main():
    return render_template('main.html')



@app.route('/about')
def about():
    image_urls = scrape_image_urls()  # Call the function to get image URLs

    # Load reaction counts from local storage
    reaction_counts = json.loads(request.cookies.get('reaction_counts', '{}'))

    return render_template('about.html', image_urls=image_urls, reaction_counts=reaction_counts)

@app.route('/submit_comment', methods=['POST'])
@login_required
def submit_comment():
    if request.method == 'POST':
        comment_text = request.form.get('comment')
        user_id = current_user.id  # Получаем ID текущего пользователя

        # Вставляем комментарий в таблицу comments
        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()
        cursor.execute('INSERT INTO comments (user_id, comment) VALUES (?, ?)', (user_id, comment_text))
        conn.commit()
        conn.close()

        flash('Ваш комментарий был успешно отправлен!', 'success')

    return redirect(url_for('education'))


@app.route('/education', methods=['GET', 'POST'])
def education():
    news_data = parse_news()  # Вызывайте ваш парсер

    # Получаем комментарии из базы данных
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('''
        SELECT comments.comment, users.username, comments.created_at 
        FROM comments 
        JOIN users ON comments.user_id = users.id 
        ORDER BY comments.created_at DESC
    ''')
    comment_data = cursor.fetchall()
    conn.close()

    return render_template('education.html', news_data=news_data, comment_data=comment_data)


@app.route('/projects')
def projects():
    return render_template('projects.html')


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/status')
def status():
    news_data = parse_status_page()
    return render_template('status.html', news_data=news_data)


@app.route('/home')
def home():
    return render_template('home.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method == 'POST' and form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users WHERE username = ?', (username,))
        user_data = cursor.fetchone()
        conn.close()

        if user_data and user_data[2] == password:
            user = User(user_data[0], user_data[1], user_data[2])
            login_user(user)
            return redirect(url_for('dashboard'))
        else:
            flash('Имя пользователя или пароль неверны', 'error')
    return render_template('login.html', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = LoginForm()
    if request.method == 'POST' and form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users WHERE username = ?', (username,))
        existing_user = cursor.fetchone()

        if existing_user:
            flash('Аккаунт с таким именем пользователя уже существует. Пожалуйста, войдите или используйте другое имя.',
                  'error')
        else:
            cursor.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, password))
            conn.commit()
            conn.close()

            flash('Регистрация прошла успешно. Теперь вы можете войти.', 'success')
            return redirect(url_for('login'))

    return render_template('register.html', form=form)


@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')



@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


if __name__ == '__main__':
    app.run(debug=True)
