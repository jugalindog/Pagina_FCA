from flask import Blueprint, Flask,render_template,request,redirect, url_for, flash, jsonify
from flask import session
from functools import wraps
from werkzeug.security import check_password_hash, generate_password_hash



main=Blueprint('main',__name__)

# Decorador para rutas protegidas
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get("user_email"):
            flash("🔒 Debes iniciar sesión para acceder a esta página.", "warning")
            return redirect(url_for('main.index'))
        return f(*args, **kwargs)
    return decorated_function

# Decorador para verificar roles de usuario
def role_required(*required_roles):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            # 1. Primero, verificar si el usuario ha iniciado sesión
            if "user_role" not in session:
                flash("🔒 Debes iniciar sesión para acceder a esta página.", "warning")
                return redirect(url_for('main.index'))

            user_role = session.get("user_role")

            # 2. El 'superadmin' tiene acceso a todo
            if user_role == 'superadmin':
                return f(*args, **kwargs)

            # 3. Verificar si el rol del usuario está en los roles permitidos
            if user_role not in required_roles:
                flash("🚫 No tienes permiso para acceder a esta sección.", "danger")
                return redirect(url_for('main.UI')) # Redirigir a la página principal

            return f(*args, **kwargs)
        return decorated_function
    return decorator


# --- GESTIÓN DE USUARIOS ---
# Ahora cada usuario tiene un hash y un rol.
usuarios = {
    'autoevaluacion': {'hash': 'pbkdf2:sha256:1000000$dCUKL3yflOeqNCDV$05f59af1a8108731c2f323a2dbf77fe865c4a7d019402a3c5fb3db23959b0635', 'role': 'secretaria'},
    'superadmin': {'hash': 'pbkdf2:sha256:1000000$K0VKCTErirOMxvjq$4d11b15ea1e28b2e1f6cad1ad0151bb97453719ba6482cbf59432148de702ae2', 'role': 'superadmin'},
    'DirecBienestar': {'hash': 'pbkdf2:sha256:1000000$iwVhT0ySuK9Zte2R$e43ff89d01e742d4a64ce1e5c9cb36cd6d221c7472400640f761c5025e457b7e', 'role': 'bienestar'},
    'DirecCurricular': {'hash': 'pbkdf2:sha256:1000000$lqaOMa5rJvdJ6Bxf$7845f17bcb65e398cb030fac10e248f238fd018e6eef84fab1a84b920397f778', 'role': 'curricular'},
    'Vicedecanatura': {'hash': 'pbkdf2:sha256:1000000$nuxxmORBPW2lptGv$a3b915a3ab1ae3b3732e73f35b4616072d84deb283ec41f4008d000b49ba46f3', 'role': 'vicedecanatura'},
    'Decanatura': {'hash': 'pbkdf2:sha256:1000000$Z5D0lyXRksAaAAEM$c22ec029edb1c6f9146b66dad5e6a1bead8e6221af9ed3bb4fb9ada6a8a099f0', 'role': 'decanatura'}
}

def iniciar_sesion(email, password):
    user_data = usuarios.get(email)
    if user_data and check_password_hash(user_data['hash'], password):
        print(f"✅ Inicio de sesión exitoso para {email} con rol {user_data['role']}.")
        return user_data # Devolvemos toda la info del usuario
    
    print(f"❌ Intento de inicio de sesión fallido para {email}.")
    return None

@main.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        user_data = iniciar_sesion(email, password)
        if user_data:
            session.permanent = True # Usa el tiempo de vida de la sesión definido en app.py
            session["user_email"] = email  # Guardar email del usuario en la sesión
            session["user_role"] = user_data['role'] # ¡Guardamos el rol!
            flash("✅ Inicio de sesión exitoso.", "success")
            return redirect(url_for("main.UI"))  # 
        else:
            flash("❌ Usuario o contraseña incorrectos.", "danger")

    return render_template("login.html")


@main.route('/PrincipalInterface')
@login_required
def UI():
    return render_template('PrincipalInterface.html')

# Ruta para mantener la sesión activa desde el cliente
@main.route('/keep-alive')
@login_required
def keep_alive():
    # Al acceder a esta ruta, el decorador @login_required ya está activo
    # y el @app.before_request de app.py actualizará 'last_activity'.
    return jsonify(status='session_extended')

#Desconexión
@main.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('main.index'))



# Interfaz de secretaria
@main.route('/secretaria')
@role_required('decanatura','vicedecanatura','secretaria')
def secretaria():
    return render_template('secretaria.html', page_title='Secretaría')
# Interfaz de ViceDecanatura
@main.route('/ViceDecanatura')
@role_required('decanatura','vicedecanatura','secretaria')
def ViceDecanatura():
    return render_template('Prac_pro.html', page_title='ViceDecanatura')
# Interfaz de curricular
@main.route('/curricular')
@role_required('decanatura','vicedecanatura','secretaria','curricular')
def curricular():
    return render_template('curricular.html', page_title='Curricular')
# Interfaz de normatividad
@main.route('/normatividad')
@role_required('decanatura','vicedecanatura','secretaria') # Ejemplo: solo el rol 'decanatura' puede ver esto
def normatividad():
    return render_template('normatividad.html', page_title='Normatividad')
# Interfaz de Bienestar
@main.route('/Bienestar')
@role_required('decanatura','vicedecanatura','secretaria','bienestar')
def Bienestar():
    return render_template('Bienestar.html', page_title='Bienestar')
# Interfaz de Departamento
@main.route('/Departamento')
@role_required('decanatura','vicedecanatura','secretaria','bienestar')
def Departamento():
    return render_template('Departamento.html', page_title='Departamento')
# Interfaz de PTA
@main.route('/PTA')
@role_required('decanatura','vicedecanatura','secretaria')
def PTA():
    return render_template('PTA.html', page_title='PTA')


######            ########
###### Curricular ########
######            ######## (Protegido por el rol 'curricular')
## Interfaz de pregrado
@main.route('/curricular/pregrado')
@role_required('decanatura','vicedecanatura','secretaria','curricular')
def pregrado():
    return render_template('pregrado.html', page_title='Curricular', sub_page_title='Pregrado')
## Interfaz de posgrado
@main.route('/curricular/posgrado')
@role_required('decanatura','vicedecanatura','secretaria','curricular')
def posgrado():
    return render_template('posgrado.html', page_title='Curricular', sub_page_title='Posgrado')


######            ########
###### SECRETARIA ######## (Protegido por el rol 'secretaria')
######            ######## 

## 1. Interfaz de admitidos posgrado
@main.route('/secretaria/admi_pos')
@role_required('decanatura','vicedecanatura','secretaria')
def admi_pos():
    return render_template('admi_pos.html', page_title='Secretaría', sub_page_title='Admitidos Posgrado')
## 2. Interfaz de matriculados posgrados
@main.route('/secretaria/matri_pos')
@role_required('decanatura','vicedecanatura','secretaria')
def matri_pos():
    return render_template('matri_pos.html', page_title='Secretaría', sub_page_title='Matriculados Posgrado')
## 3. Interfaz de movilidad saliente estudiantes
@main.route('/secretaria/movi_sal_est')
@role_required('decanatura','vicedecanatura','secretaria')
def movi_sal_est():
    return render_template('movi_sal_est.html', page_title='Secretaría', sub_page_title='Movilidad Saliente Estudiantes')
## 4. Interfaz de movilidad entrante estudiantes
@main.route('/secretaria/movi_ent_est')
@role_required('decanatura','vicedecanatura','secretaria')
def movi_ent_est():
    return render_template('movi_ent_est.html', page_title='Secretaría', sub_page_title='Movilidad Entrante Estudiantes')
## 5. Interfaz de movilidad saliente docente
@main.route('/secretaria/movi_sal_doc')
@role_required('decanatura','vicedecanatura','secretaria')
def movi_sal_doc():
    return render_template('movi_sal_doc.html', page_title='Secretaría', sub_page_title='Movilidad Saliente Docente')
## 6. Interfaz de movilidad entrante docente
@main.route('/secretaria/movi_ent_doc')
@role_required('decanatura','vicedecanatura','secretaria')
def movi_ent_doc():
    return render_template('movi_ent_doc.html', page_title='Secretaría', sub_page_title='Movilidad Entrante Docente')
## 7. Interfaz de convenios
@main.route('/secretaria/convenios')
@role_required('decanatura','vicedecanatura','secretaria')
def convenios():
    return render_template('convenios.html', page_title='Secretaría', sub_page_title='Convenios')

######            ########
###### ViceDecanatura ########
######            ########


######            ########
###### Departamento ########
######            ########

## Interfaz de Docentes
@main.route('/Departamento/Docentes')
@role_required('decanatura','vicedecanatura','secretaria','bienestar')
def Docentes():
    return render_template('Docentes.html', page_title='Departamento', sub_page_title='Docentes')


######            ########
###### PTA  ######## (Protegido por el rol 'secretaria')
######            ######## 
