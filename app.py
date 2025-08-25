from flask import Flask, session, redirect, url_for, flash
from datetime import timedelta, datetime
from main import main as main_blueprint

def create_app():
    app = Flask(__name__)
    app.secret_key = "FCA2080179"
    app.permanent_session_lifetime = timedelta(minutes=5)

    @app.before_request
    def check_session_timeout():
        if 'user_email' in session:
            if 'last_activity' in session:
                now = datetime.now()
                last_activity = datetime.fromisoformat(session['last_activity'])
                if (now - last_activity) > timedelta(minutes=5):
                    session.clear()
                    flash("⌛ Tu sesión ha expirado por inactividad.", "warning")
                    return redirect(url_for('main.index'))
            session['last_activity'] = datetime.now().isoformat()

    
    app.register_blueprint(main_blueprint)
    # 🔒 Evita uso de cache en las páginas protegidas
    @app.after_request
    def add_header(response):
        response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
        response.headers['Pragma'] = 'no-cache'
        response.headers['Expires'] = '0'
        return response

    return app
app = create_app()

if __name__ == "__main__":
    app.run(debug=True)

