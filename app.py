from flask import Flask, session, redirect, url_for, flash
from datetime import timedelta, datetime
from main import main as main_blueprint


def create_app():
    app = Flask(__name__)

    # 🔑 Clave secreta (en producción mejor usar variable de entorno)
    app.secret_key = "FCA2080179"

    # ⏳ Tiempo máximo por inactividad
    app.permanent_session_lifetime = timedelta(minutes=15)

    # ✅ CLAVE para que funcione en Google Sites (iframe)
    # Permite que el navegador guarde/mande la cookie de sesión en contexto "third-party"
    app.config.update(
        SESSION_COOKIE_NAME="fca_session",
        SESSION_COOKIE_HTTPONLY=True,
        SESSION_COOKIE_SECURE=True,      # SameSite=None requiere Secure (HTTPS)
        SESSION_COOKIE_SAMESITE="None",  # Necesario para iframes
    )

    @app.before_request
    def check_session_timeout():
        """
        Si existe user_email en sesión, revisa last_activity.
        Si pasó > 15 min, cierra sesión y redirige al index.
        """
        if 'user_email' in session:
            if 'last_activity' in session:
                now = datetime.now()
                last_activity = datetime.fromisoformat(session['last_activity'])

                if (now - last_activity) > timedelta(minutes=15):
                    session.clear()
                    flash("⌛ Tu sesión ha expirado por inactividad.", "warning")
                    return redirect(url_for('main.index'))

            # Actualiza última actividad
            session['last_activity'] = datetime.now().isoformat()

    # Registrar blueprint
    app.register_blueprint(main_blueprint)

    # 🚫 Evitar cache (útil en páginas protegidas/login)
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