import os
from flask import Flask, render_template, request, redirect, url_for, send_file, send_from_directory, flash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename
from apscheduler.schedulers.background import BackgroundScheduler
import shutil
from datetime import datetime
from functools import wraps
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.routing import Rule

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////home/0zero/Name/database.db'
app.config['UPLOAD_FOLDER'] = '/home/0zero/Name/static/uploads'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = '^DT0{M)Wl<RzEh]'  # Change this to a random secret key
db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'admin_login'

# Add the custom URL rule
app.url_map.add(Rule('/dickdickdickdickdickdickdickdickdcik/aaaa/8888/0000/admin', endpoint='admin_login'))

# Ensure necessary directories exist
for directory in ['backups', app.config['UPLOAD_FOLDER']]:
    if not os.path.exists(directory):
        os.makedirs(directory)

class Tool(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    image = db.Column(db.String(100), nullable=False)
    download_file = db.Column(db.String(100))

class Combo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    thumbnail = db.Column(db.String(100), nullable=False)
    download_file = db.Column(db.String(100))
    media_type = db.Column(db.String(10))
    media_content = db.Column(db.String(200))

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

def backup_database():
    try:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_filename = f"database_backup_{timestamp}.db"
        shutil.copy2("/home/0zero/Name/database.db", f"/home/0zero/Name/backups/{backup_filename}")
        print(f"Database backed up: {backup_filename}")
    except Exception as e:
        print(f"Backup failed: {str(e)}")

scheduler = BackgroundScheduler()
scheduler.add_job(func=backup_database, trigger="interval", hours=24)

# Only start the scheduler if we're not running under uWSGI
if os.environ.get('RUNNING_UNDER_UWSGI') != 'true':
    scheduler.start()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/tools')
def tools():
    tools = Tool.query.all()
    return render_template('tools.html', tools=tools)

@app.route('/tool/<int:tool_id>')
def tool_detail(tool_id):
    tool = Tool.query.get_or_404(tool_id)
    return render_template('tool_detail.html', tool=tool)

@app.route('/combos')
def combos():
    combos = Combo.query.all()
    return render_template('combos.html', combos=combos)

@app.route('/combo/<int:combo_id>')
def combo_detail(combo_id):
    combo = Combo.query.get_or_404(combo_id)
    return render_template('combo_detail.html', combo=combo)

@app.route('/download/<int:combo_id>')
def download_file(combo_id):
    combo = Combo.query.get_or_404(combo_id)
    if combo.download_file:
        return send_file(os.path.join(app.config['UPLOAD_FOLDER'], combo.download_file), as_attachment=True)
    return "No file available for download", 404

@app.endpoint('admin_login')
def admin_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            login_user(user)
            return redirect(url_for('admin'))
        flash('Invalid username or password')
    return render_template('login.html')

@app.route('/dickdickdickdickdickdickdickdickdcik/aaaa/8888/0000/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/dickdickdickdickdickdickdickdickdcik/aaaa/8888/0000/adminpanel', methods=['GET', 'POST'])
@login_required
def admin():
    if request.method == 'POST':
        item_type = request.form['item_type']
        title = request.form['title']
        description = request.form['description']

        try:
            if item_type == 'tool':
                image = request.files['image']
                image_filename = secure_filename(image.filename)
                image.save(os.path.join(app.config['UPLOAD_FOLDER'], image_filename))

                download_file = request.files.get('download_file')
                download_filename = None
                if download_file:
                    download_filename = secure_filename(download_file.filename)
                    download_file.save(os.path.join(app.config['UPLOAD_FOLDER'], download_filename))

                new_item = Tool(
                    title=title,
                    description=description,
                    image=image_filename,
                    download_file=download_filename
                )
            else:
                thumbnail = request.files['thumbnail']
                thumbnail_filename = secure_filename(thumbnail.filename)
                thumbnail.save(os.path.join(app.config['UPLOAD_FOLDER'], thumbnail_filename))

                download_file = request.files.get('download_file')
                download_filename = None
                if download_file:
                    download_filename = secure_filename(download_file.filename)
                    download_file.save(os.path.join(app.config['UPLOAD_FOLDER'], download_filename))

                media_type = request.form.get('media_type')
                media_content = None
                if media_type == 'video':
                    video_file = request.files.get('video_file')
                    if video_file:
                        media_content = secure_filename(video_file.filename)
                        video_file.save(os.path.join(app.config['UPLOAD_FOLDER'], media_content))
                elif media_type == 'youtube':
                    media_content = request.form.get('youtube_link')

                new_item = Combo(
                    title=title,
                    description=description,
                    thumbnail=thumbnail_filename,
                    download_file=download_filename,
                    media_type=media_type,
                    media_content=media_content
                )

            db.session.add(new_item)
            db.session.commit()
            print(f"New {item_type} added: {new_item.title}")
        except Exception as e:
            print(f"Error adding {item_type}: {str(e)}")
            db.session.rollback()

        return redirect(url_for('admin'))

    return render_template('admin.html')

@app.route('/static/<path:filename>')
def serve_static(filename):
    return send_from_directory('static', filename)

def create_admin_user():
    admin_username = 'Milo123'  # Change this to your desired admin username
    admin_password = 'Milopilo0811'  # Change this to a secure password

    if not User.query.filter_by(username=admin_username).first():
        admin_user = User(username=admin_username)
        admin_user.set_password(admin_password)
        db.session.add(admin_user)
        db.session.commit()
        print(f"Admin user '{admin_username}' created.")

def add_download_file_to_tool():
    with app.app_context():
        if not db.engine.has_table('tool'):
            db.create_all()
            return

        if 'download_file' not in [column.name for column in Tool.__table__.columns]:
            db.engine.execute('ALTER TABLE tool ADD COLUMN download_file VARCHAR(100)')
            print("Added download_file column to tool table.")

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        create_admin_user()
        add_download_file_to_tool()
    app.run(debug=False)
