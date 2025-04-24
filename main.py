from flask import Blueprint, Flask,render_template,request,redirect, url_for, flash

main=Blueprint('main',__name__)


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
            flash("✅ Inicio de sesión exitoso.", "success")
            return redirect(url_for("main.UI"))  # 
        else:
            flash("❌ Usuario o contraseña incorrectos.", "danger")

    return render_template("login.html")


@main.route('/PrincipalInterface')
def UI():
    return render_template('PrincipalInterface.html')



# Interfaz de secretaria
@main.route('/secretaria')
def secretaria():
    return render_template('secretaria.html')
# Interfaz de curricular
@main.route('/curricular')
def curricular():
    return render_template('curricular.html')
# Interfaz de normatividad
@main.route('/normatividad')
def normatividad():
    return render_template('normatividad.html')

######            ########
###### SECRETARIA ########
######            ########

## 1. Interfaz de admitidos posgrado
@main.route('/secretaria/admi_pos')
def admi_pos():
    return render_template('admi_pos.html')
## 2. Interfaz de matriculados posgrados
@main.route('/secretaria/matri_pos')
def matri_pos():
    return render_template('matri_pos.html')
## 3. Interfaz de movilidad saliente estudiantes
@main.route('/secretaria/movi_sal_est')
def movi_sal_est():
    return render_template('movi_sal_est.html')
## 4. Interfaz de movilidad entrante estudiantes
@main.route('/secretaria/movi_ent_est')
def movi_ent_est():
    return render_template('movi_ent_est.html')
## 5. Interfaz de movilidad saliente docente
@main.route('/secretaria/movi_sal_doc')
def movi_sal_doc():
    return render_template('movi_sal_doc.html')
## 6. Interfaz de movilidad entrante docente
@main.route('/secretaria/movi_ent_doc')
def movi_ent_doc():
    return render_template('movi_ent_doc.html')
## 7. Interfaz de convenios
@main.route('/secretaria/convenios')
def convenios():
    return render_template('convenios.html')

######            ########
###### CURRICULAR ########
######            ########
