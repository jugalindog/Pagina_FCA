from flask import Flask
from datetime import timedelta
from main import main as main_blueprint

def create_app():
    app = Flask(__name__)
    app.secret_key = "FCA2080179"
    app.permanent_session_lifetime = timedelta(minutes=15)

    
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
