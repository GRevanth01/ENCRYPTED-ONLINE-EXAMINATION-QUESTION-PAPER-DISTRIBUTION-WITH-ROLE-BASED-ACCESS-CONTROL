import os
import logging
from flask import Flask
from werkzeug.middleware.proxy_fix import ProxyFix
from tinydb import TinyDB, Query

logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)
app.secret_key = os.environ.get('SESSION_SECRET', 'secure-system-key-2024')
app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)

os.makedirs('data', exist_ok=True)
os.makedirs('uploads', exist_ok=True)
os.makedirs('keys', exist_ok=True)

db = TinyDB('data/exam_db.json')
users_table = db.table('users')
papers_table = db.table('papers')
keys_table = db.table('keys')
authorizations_table = db.table('authorizations')
logs_table = db.table('access_logs')

from routes import auth, ea, aef
app.register_blueprint(auth.bp)
app.register_blueprint(ea.bp)
app.register_blueprint(aef.bp)

from flask import redirect, url_for

@app.route('/')
def index():
    return redirect(url_for('auth.home'))


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
