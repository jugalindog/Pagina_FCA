from flask import Blueprint, Flask,render_template,request,redirect, url_for, flash
from flask import session
from functools import wraps



main=Blueprint('main',__name__)

# Decorador para rutas protegidas
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get("usuario_logueado"):
            flash("🔒 Debes iniciar sesión para acceder a esta página.", "warning")
            return redirect(url_for('main.index'))
        return f(*args, **kwargs)
    return decorated_function



# Inicio de sesión
usuarios={'autoevaluacion_fcabog@unal.edu.co':'fcaxauto345*',
          'superadmin':'jorge123'}
def iniciar_sesion(email, password):
    if email in usuarios and usuarios[email] == password:
        print("✅ Inicio de sesión exitoso.")
        return True
    print("❌ Usuario o contraseña incorrectos.")
    return False

@main.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        if iniciar_sesion(email, password):
            session["usuario_logueado"] = True  #Valirar inicio de sesión
            flash("✅ Inicio de sesión exitoso.", "success")
            return redirect(url_for("main.UI"))  # 
        else:
            flash("❌ Usuario o contraseña incorrectos.", "danger")

    return render_template("login.html")


@main.route('/PrincipalInterface')
@login_required
def UI():
    return render_template('PrincipalInterface.html')


#Desconexión
@main.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('main.index'))



# Interfaz de secretaria
@main.route('/secretaria')
@login_required
def secretaria():
    return render_template('secretaria.html')
# Interfaz de curricular
@main.route('/curricular')
@login_required
def curricular():
    return render_template('curricular.html')
# Interfaz de normatividad
@main.route('/normatividad')
@login_required
def normatividad():
    return render_template('normatividad.html')

######            ########
###### SECRETARIA ########
######            ########

## 1. Interfaz de admitidos posgrado
@main.route('/secretaria/admi_pos')
@login_required
def admi_pos():
    return render_template('admi_pos.html')
## 2. Interfaz de matriculados posgrados
@main.route('/secretaria/matri_pos')
@login_required
def matri_pos():
    return render_template('matri_pos.html')
## 3. Interfaz de movilidad saliente estudiantes
@main.route('/secretaria/movi_sal_est')
@login_required
def movi_sal_est():
    return render_template('movi_sal_est.html')
## 4. Interfaz de movilidad entrante estudiantes
@main.route('/secretaria/movi_ent_est')
@login_required
def movi_ent_est():
    return render_template('movi_ent_est.html')
## 5. Interfaz de movilidad saliente docente
@main.route('/secretaria/movi_sal_doc')
@login_required
def movi_sal_doc():
    return render_template('movi_sal_doc.html')
## 6. Interfaz de movilidad entrante docente
@main.route('/secretaria/movi_ent_doc')
@login_required
def movi_ent_doc():
    return render_template('movi_ent_doc.html')
## 7. Interfaz de convenios
@main.route('/secretaria/convenios')
@login_required
def convenios():
    return render_template('convenios.html')

######            ########
###### CURRICULAR ########
######            ########
