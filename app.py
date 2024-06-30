from flask import Flask
from flask import render_template
from flask import request
from flask import url_for
from flask import send_file
from flask import redirect
from flask_login import LoginManager
from flask_login import login_user
from flask_login import login_required
from flask_login import logout_user
from flask_login import current_user
from componentes.test import tragos_con_alcohol
from componentes.test import tragos_sin_alcohol
from componentes.test import tragos_alfabetico
from componentes.test import tragos_busqueda
from componentes.modelos2 import Usuario
import componentes.config_db as config_db
import io
import os

app = Flask(__name__)

#genera una clave secreata para manejar el login
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'default_secret_key')
login_manager = LoginManager(app)
login_manager.login_view = 'login'

#objeto visitante en caso de no haber ningun usuario logueado
visitante = {'nombre':'visitante',
            'rol':'VISITANTE'}

#--- Login ---

# Manejo de login, recibe de POST email y contraseña 
# luego busca en la DB el usuario por su email 
# si el usuario existe verifica la contraseña hasheada con la contraseña ingresada
# si son correctas accede al perfil de usuario
# Tambien maneja el GET de la vista y si el usuario ya ha iniciado sesion he intenta acceder al login es redireccionado a su perfil
# del caso contrario significa que no existe ningun usuario logueado y accede al formulario de login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = Usuario.obtener_uno_por_email(email=email) 
        if user and Usuario.verificar_password(user.password , password):
            login_user(user)
            return redirect(url_for('vista_perfil_usuario'))
    if current_user.is_authenticated:
        return redirect(url_for('vista_perfil_usuario'))
        #return render_template('perfil_usuario.html',user=current_user)
    else:
        return render_template('login.html',user=visitante)

# Este metodo de cargar usuario retorna el usuario de la DB por su ID
@login_manager.user_loader
def load_user(user_id):
    return Usuario.obtener_uno(user_id)

# Metodo para cerrar sesion
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))
# ------ fin login  -----------------------

@app.route('/perfil_usuario')
@login_required
def vista_perfil_usuario():
    if current_user.is_authenticated:
        return render_template('perfil_usuario.html',user=current_user )
    else:
        return render_template('login.html')

# --- rutas de la pagina, controladores ---
# vista principal de la pagina
@app.route("/")
def principal():
    if current_user.is_authenticated:
        return render_template('index.html',user=current_user)
    else:
        return render_template('index.html', user=visitante)

# vista de Quienes somos
@app.route("/quienes_somos")
def quienes_somos():
    if current_user.is_authenticated:
        return render_template('quienes_somos.html',user=current_user)
    else:
        return render_template('quienes_somos.html',user=visitante)


#----- Registro -----
# Vista y metodo de registro GET y POST
@app.route('/registro', methods=['GET', 'POST'])
def registrar_usuario():
    try:
        if request.method == 'POST':
            print("REGISTAR USUARIO METODO....")
            nombre = request.form['nombre']
            apellido = request.form['apellido']
            genero = request.form['genero']
            email = request.form['email']
            password = request.form['password']
            mayor = request.form['mayor'] 
            rol = "USUARIO"
            alta = True #request.form['alta']
            image = request.files['image']
            image_data = image.read() if image else None
            Usuario.agregar(nombre, apellido, genero, email, password, mayor, rol, alta, image_data)
            return redirect(url_for('login'))
        #return render_template('registro.html')
        if current_user.is_authenticated:
            return redirect(url_for('vista_perfil_usuario'))
            #return render_template('login.html',user=current_user)
        else:
            return render_template('registro.html',user=visitante)
    except Exception as e:
        mensaje = str(e)
        # Capura la excepcion y verifica si es un email repetido, devuelve mensaje de "Email ya registrado"
        if 'Duplicate entry' in mensaje and 'for key' in mensaje:
            mensaje = "Ese email ya se encuentra registrado. Pruebe un email diferente"
        else:
            mensaje = mensaje
        
        return render_template('registro.html',user=visitante, mensaje=mensaje)


#Todas las imagenes en DB se guardan en formato Byte(Long Blob),
# este metodo las interpreta de nuevo como imagen
@app.route('/user/<user_id>/image')
def get_user_image(user_id):
    try:
        # Este metodo busca el usuario con la imagen
        user = Usuario.obtener_uno(user_id)
        # Si el usuario existe y tiene imagen, 
        # toma el la imagen en Bytes y lo interpreta como imagen nuevamente
        if user and user.image:
            return send_file(io.BytesIO(user.image), mimetype='image/jpeg')
        else:
            # si no existe imagen devuelve un mensaje y un 404 no econtrado       
            return "Imagen no encontrada", 404
    except Exception as e:
        print(f"error al obtener la imagen{e}")



# ----- Parte Admin   ----
# Metodos y acciones que solo puede realizar la cuenta de ADMINISTRADOR
@app.route("/admin_dashboard")
@login_required
def admin_dashboard():
    usuarios = Usuario.obtener_todos()
    if current_user.is_authenticated and current_user.rol == "ADMIN":
        return render_template('dashboard2.html', usuarios=usuarios,user=current_user)
    else:
        return render_template('index.html', user=visitante)

# El ADMIN puede modificar todos los atributos de cualquier usuario
@app.route('/admin_dashboard/<int:id>', methods=['GET', 'POST'])
@login_required
def modificar_usuario(id):
    if request.method == 'POST':
        nombre = request.form['nombre']
        apellido = request.form['apellido']
        genero = request.form['genero']
        email = request.form['email']
        password = request.form['password']
        mayor = request.form['mayor'] 
        rol = request.form['rol']
        alta = None #request.form['alta']
        #image =request.files['image']
        #image_data = image.read() if image else None
        Usuario.modificar(id, nombre, apellido, genero, email, password, mayor, rol, alta, None)
        
        return redirect(url_for('admin_dashboard'))
    else:
        usuario = Usuario.obtener_uno(id)
        
        return render_template('modificar_usuario.html', usuario=usuario)

# Metodo para dar de alta o baja un usuario
@app.route('/alta_usuario/<int:id>', methods=['POST'])
@login_required
def alta_de_usuario(id):
    if request.method == 'POST':
        usuario = Usuario.obtener_uno(id)
        print(usuario.email," -- Estado de Alta --",usuario.alta)
        if usuario.alta == 1:
            usuario.alta = 0
            Usuario.modificar(id, usuario.nombre, usuario.apellido, usuario.genero, usuario.email, usuario.password, usuario.mayor, usuario.rol, usuario.alta, usuario.image)
        else:
            usuario.alta = 1
            Usuario.modificar(id, usuario.nombre, usuario.apellido, usuario.genero, usuario.email, usuario.password, usuario.mayor, usuario.rol, usuario.alta, usuario.image)
            
        return redirect(url_for('admin_dashboard'))

# Metodo para eliminar usuario de la DB
@app.route('/eliminar_usuario/<int:id>', methods=['POST'])
@login_required
def eliminar_usuario(id):
    if current_user.is_authenticated and current_user.rol == "ADMIN":
        Usuario.eliminar(id)
        if request.method == 'POST':
            return redirect(url_for('admin_dashboard'))

# ------ Fin parte ADMIN -----
#
#
#
# ------ API cocktails -----

    # vista principal donde se muestran todas las bebidas en la API
    # crea 2 listas separadas de bebidas con y sin alcohol
@app.route('/bebidas')
def test():
    tragos_con_alcohol_lista = tragos_con_alcohol()
    tragos_sin_alcohol_lista = tragos_sin_alcohol()
    # une las dos listas en una sola
    todos_los_tragos_lista = tragos_con_alcohol_lista + tragos_sin_alcohol_lista
    
    #print(current_user.mayor)
    if current_user.is_authenticated:
        if current_user.mayor == "si":
            return render_template('bebidas.html', tragos=todos_los_tragos_lista, user=current_user)
        else:
            return render_template('bebidas.html', tragos=tragos_sin_alcohol_lista, user=current_user)
    else:
        return render_template('bebidas.html', tragos=tragos_sin_alcohol_lista, user=visitante)

@app.route('/busqueda', methods=['GET', 'POST'])
def tes_alfabetico():
    # Este metodo devuelve bebidas segun una busqueda alfabetica,
    # recibe una letra y devuelve bebidas que comienzan con esa letra
    letra = request.args.get('letra')
    tragosAlfa = tragos_alfabetico(letra)
    #print(tragosAlfa)
    # crea una segunda lista dejando solamente las bebidas sin alcohol 
    tragos_s_alcohol = [trago for trago in tragosAlfa if trago.get('strAlcoholic') == 'Non alcoholic']
    
    if current_user.is_authenticated:
        return render_template('bebidas.html', tragos=tragosAlfa, user=current_user)
    else:
        return render_template('bebidas.html', tragos=tragos_s_alcohol, user=visitante)
    # return render_template('bebidas.html', tragos=tragosAlfa)


@app.route('/resultados_busqueda', methods=['GET', 'POST'])
def resultados_busqueda():
        # Este metodo busca bebidas por nombre
        # devuelve una lista de bebidas con el mismo nombre
        palabra = request.args.get('palabra')
        print("desde el form palabra es: ", palabra)
        tragosBusqueda = tragos_busqueda(palabra)
        # toma la lista de bebidas con el mismo nombre y devuelve una solo con las bebidas sin alcohol
        tragos_s_alcohol = [trago for trago in tragosBusqueda if trago.get('strAlcoholic') == 'Non alcoholic']
        
        if current_user.is_authenticated:
            return render_template('bebidas.html', tragos=tragosBusqueda, user=current_user)
        else:
            return render_template('bebidas.html', tragos=tragos_s_alcohol, user=visitante)
        # return render_template('bebidas.html', tragos=tragosBusqueda)



@app.route('/con_alcohol')
def con_alcohol():
    # este metodo devuelve todas las bebidas con alcohol y las envia al front
    tragos_con_alcohol_lista = tragos_con_alcohol()
    if current_user.is_authenticated:
        return render_template('bebidas.html', tragos=tragos_con_alcohol_lista, user=current_user)
    else:
        return render_template('bebidas.html', tragos=tragos_con_alcohol_lista, user=visitante)

@app.route('/sin_alcohol')
def sin_alcohol():
    # este metodo devuelve todas las bebidas sin alcohol y las envia al front
    tragos_sin_alcohol_lista = tragos_sin_alcohol()
    if current_user.is_authenticated:
        return render_template('bebidas.html', tragos=tragos_sin_alcohol_lista, user=current_user)
    else:
        return render_template('bebidas.html', tragos=tragos_sin_alcohol_lista, user=visitante)

# ---- Usuario ----
@app.route('/perfil_usuario/<int:id>', methods=['POST'])
@login_required
def usuario_modificar_usuario(id):
    # Este metodo modifica los datos del usuario logueado
    if request.method == 'POST':
        nombre = request.form['nombre']
        apellido = request.form['apellido']
        genero = request.form['genero']
        mayor = request.form['mayor'] 
        Usuario.modificar(current_user.id, nombre, apellido, genero, current_user.email, current_user.password, mayor, current_user.rol, current_user.alta, current_user.image)
        return redirect(url_for('vista_perfil_usuario'))

@app.route('/perfil_usuario_imagen/<int:id>', methods=['POST'])
@login_required
def usuario_modificar_imagen(id):
    # Este metodo modifica la imagen del usuario logueado
    if request.method == 'POST':
        image = request.files['image']
        image_data = image.read()
        Usuario.modificar(current_user.id, current_user.nombre, current_user.apellido, current_user.genero, current_user.email, current_user.password, current_user.mayor, current_user.rol, current_user.alta, image_data)
        return redirect(url_for('vista_perfil_usuario'))

if __name__ == '__main__' :
    app.run(debug=True)