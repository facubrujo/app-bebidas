from flask import Flask, render_template, request, url_for, send_file, redirect
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from componentes.test import tragos_con_alcohol, tragos_sin_alcohol, tragos_alfabetico, tragos_busqueda
from componentes.modelos2 import Usuario
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

@login_manager.user_loader
def load_user(user_id):
    return Usuario.obtener_uno(user_id)

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

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))
# ------ fin login  -----------------------

@app.route('/perfil_usuario')
def vista_perfil_usuario():
    if current_user.is_authenticated:
        return render_template('perfil_usuario.html',user=current_user )
    else:
        return render_template('login.html')

# rutas de la pagina, controladores

@app.route("/")
def principal():

    if current_user.is_authenticated:
        return render_template('index.html',user=current_user)
    else:
        return render_template('index.html', user=visitante)
    

@app.route("/quienes_somos")
def quienes_somos():
    if current_user.is_authenticated:
        return render_template('quienes_somos.html',user=current_user)
    else:
        return render_template('quienes_somos.html',user=visitante)


#----- Registro -----

@app.route('/registro', methods=['GET', 'POST'])
def registrar_usuario():
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


#manejo de rutas de imagenes (bits a img)
@app.route('/user/<user_id>/image')
def get_user_image(user_id):
    user = Usuario.obtener_uno(user_id)
    if user and user.image:
        return send_file(io.BytesIO(user.image), mimetype='image/jpeg')
    else:
        return "Imagen no encontrada", 404


# ----- Parte Admin   ----
@app.route("/admin_dashboard")
def admin_dashboard():
    usuarios = Usuario.obtener_todos()
    if current_user.is_authenticated and current_user.rol == "ADMIN":
        return render_template('dashboard2.html', usuarios=usuarios,user=current_user)
    else:
        return render_template('index.html', user=visitante)


@app.route('/admin_dashboard/<int:id>', methods=['GET', 'POST'])
def modificar_usuario(id):
    if request.method == 'POST':
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
        Usuario.modificar(id, nombre, apellido, genero, email, password, mayor, rol, alta, image_data)
        
        return redirect(url_for('admin_dashboard'))
    else:
        usuario = Usuario.obtener_uno(id)
        
        return render_template('modificar_usuario.html', usuario=usuario)


@app.route('/eliminar_usuario/<int:id>', methods=['POST'])
def eliminar_usuario(id):
    Usuario.eliminar(id)
    if request.method == 'POST':
        return redirect(url_for('admin_dashboard'))

@app.route('/alta_usuario/<int:id>', methods=['POST'])
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




#   ------  API cocktails   -----

@app.route('/bebidas')
def test():
    tragos_con_alcohol_lista = tragos_con_alcohol()
    tragos_sin_alcohol_lista = tragos_sin_alcohol()
    todos_los_tragos_lista = tragos_con_alcohol_lista + tragos_sin_alcohol_lista
    
    #print(current_user.mayor)
    if current_user.is_authenticated:
        if current_user.mayor == "si":
            return render_template('bebidas.html', tragos=todos_los_tragos_lista, user=current_user)
        else:
            return render_template('bebidas.html', tragos=tragos_sin_alcohol_lista, user=current_user)
            
    else:
        return render_template('bebidas.html', tragos=tragos_sin_alcohol_lista, user=visitante)

@app.route('/bebidas/busqueda', methods=['GET', 'POST'])
def tes_alfabetico():
    letra = request.args.get('letra')
    tragosAlfa = tragos_alfabetico(letra)
    print(tragosAlfa)
    #tragos = data['drinks'] if data['drinks'] else []
    tragos_s_alcohol = [trago for trago in tragosAlfa if trago.get('strAlcoholic') == 'Non alcoholic']
            
    
    if current_user.is_authenticated:
        return render_template('bebidas.html', tragos=tragosAlfa, user=current_user)
    else:
        return render_template('bebidas.html', tragos=tragos_s_alcohol, user=visitante)
    # return render_template('bebidas.html', tragos=tragosAlfa)


@app.route('/resultados_busqueda', methods=['GET', 'POST'])
def resultados_busqueda():
    # if request.method == 'POST':
        palabra = request.args.get('palabra')
        print("desde el form palabra es: ", palabra)
        tragosBusqueda = tragos_busqueda(palabra)
        
        tragos_s_alcohol = [trago for trago in tragosBusqueda if trago.get('strAlcoholic') == 'Non alcoholic']
        
        if current_user.is_authenticated:
            return render_template('bebidas.html', tragos=tragosBusqueda, user=current_user)
        else:
            return render_template('bebidas.html', tragos=tragos_s_alcohol, user=visitante)
        # return render_template('bebidas.html', tragos=tragosBusqueda)



@app.route('/bebidas/con_alcohol')
def con_alcohol():
    tragos_con_alcohol_lista = tragos_con_alcohol()
    if current_user.is_authenticated:
        return render_template('bebidas.html', tragos=tragos_con_alcohol_lista, user=current_user)
    else:
        return render_template('bebidas.html', tragos=tragos_con_alcohol_lista, user=visitante)

@app.route('/bebidas/sin_alcohol')
def sin_alcohol():
    tragos_sin_alcohol_lista = tragos_sin_alcohol()
    if current_user.is_authenticated:
        return render_template('bebidas.html', tragos=tragos_sin_alcohol_lista, user=current_user)
    else:
        return render_template('bebidas.html', tragos=tragos_sin_alcohol_lista, user=visitante)



if __name__ == '__main__' :
    app.run(debug=True)