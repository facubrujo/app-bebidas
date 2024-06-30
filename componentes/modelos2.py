import componentes.config_db as config_db
from flask_login import UserMixin
import bcrypt

class Usuario(UserMixin):
    def __init__(self, id, nombre, apellido, genero, email, password, mayor, rol, alta, image):
        self.id = id
        self.nombre = nombre
        self.apellido = apellido
        self.genero = genero
        self.email = email
        self.password = password
        self.mayor = mayor
        self.rol = rol
        self.alta = alta
        self.image = image
    
    @classmethod
    def obtener_todos(cls):
        try:
            config_db.conexion.ping(reconnect=True, attempts=3, delay=5)
            
            consulta = "SELECT id, nombre, apellido, genero, email, password, mayor, rol, alta, image FROM usuarios;"
            cursor = config_db.conexion.cursor()
            cursor.execute(consulta)
            datos = cursor.fetchall()
            
            usuarios = []
            if datos:
                for tupla in datos:
                    id, nombre, apellido, genero, email, password, mayor, rol, alta, image = tupla
                    #usuario = Usuario(id, nombre, apellido, genero, email, password, mayor, rol, alta, image)
                    usuario = Usuario(id, nombre, apellido, genero, email, password, mayor, rol, alta, None)
                    usuarios.append(usuario)
                    #print("desde Consulta---", usuario.email)
                
                return usuarios
            else:
                print("No hay usuarios")
                return []
        except Exception as e:
            print(f"Error al obtener usuarios: {e}")
            return []
        finally:
            #if cursor:
            #    cursor.close()
            config_db.conexion.close()

    # @classmethod
    # def obtener_uno(cls, user_id):
    #     try:
    #         config_db.conexion.ping(reconnect=True, attempts=3, delay=5)
            
    #         consulta = "SELECT id, nombre, apellido, genero, email, password, mayor, rol, alta, image FROM usuarios WHERE id = %s;"
    #         cursor = config_db.conexion.cursor()
    #         cursor.execute(consulta, (user_id,))
    #         datos = cursor.fetchone()
            
    #         if datos:
    #             id, nombre, apellido, genero, email, password, mayor, rol, alta, image = datos
    #             usuario = Usuario(id, nombre, apellido, genero, email, password, mayor, rol, alta, image)
    #             return usuario
    #         else:
    #             print("Usuario no existe")
    #             return None
    #     except Exception as e:
    #         print(f"Error al obtener usuario: {e}")
    #         return None
    #     finally:
    #         if cursor:
    #             cursor.close()
    #         config_db.conexion.close()



    # Se aplico un bucle que maneja para hacer reintentos a la conexion en caso 
    # de que salga una excepcion para evitar que la aplicacion se caiga en caso de algun fallo 
    # tambien al momento de conectar con la DB en lugar de conectar directamete se hace ping a 
    # la conexion para verificar si la conexion esta cerrada reconecta (ping(reconect=True)), 
    # esto lo intenta hacer 3 veces en un intervalo de 5 segundos
    @classmethod
    def obtener_uno(cls, user_id):
        reintentos = 0
        reintentos_maximos=3
        cursor=None
        while reintentos < reintentos_maximos:
            try:
                #config_db.conexion.ping(reconnect=True, attempts=3, delay=5)
                config_db.conexion.connect()

                consulta = "SELECT id, nombre, apellido, genero, email, password, mayor, rol, alta, image FROM usuarios WHERE id = %s;"
                #consulta = "SELECT id, nombre, apellido, genero, email, password, mayor, rol, alta FROM usuarios WHERE id = %s;"
                cursor = config_db.conexion.cursor()
                cursor.execute(consulta, (user_id,))
                datos = cursor.fetchone()

                if datos:
                #     id, nombre, apellido, genero, email, password, mayor, rol, alta, image = datos
                #     #id, nombre, apellido, genero, email, password, mayor, rol, alta = datos
                #     usuario = Usuario(id, nombre, apellido, genero, email, password, mayor, rol, alta, image)
                #     #usuario = Usuario(id, nombre, apellido, genero, email, password, mayor, rol, alta, None)
                #     return usuario

                    try:
                        id, nombre, apellido, genero, email, password, mayor, rol, alta, image = datos
                    except ValueError:
                        # Si la imagen falla, establece image como None
                        id, nombre, apellido, genero, email, password, mayor, rol, alta = datos
                        image = None
                    
                    usuario = Usuario(id, nombre, apellido, genero, email, password, mayor, rol, alta, image)
                    return usuario

                else:
                    print("usuario no existe")
                    return None
            except Exception as e:
                print(f"metodo obtener_uno... error al obtener usuario: {e}")
                reintentos += 1
                if reintentos < reintentos_maximos:
                    print(f"reintentando conexion... ({reintentos}/{reintentos_maximos})")
                else:
                    print("numero maximo de reintentos")
                    return None
            finally:
                try:
                    if cursor:
                        cursor.close()
                    config_db.conexion.close()
                except Exception as error:
                    print(f"error al cerrar la conexion: {error}")
        return None



    @classmethod 
    def obtener_uno_por_email(cls, email): 
        config_db.conexion.connect()
        consulta = f"SELECT id, nombre, apellido, genero, email, password, mayor, rol, alta, image FROM usuarios WHERE email = %s;"
        cursor = config_db.conexion.cursor() 
        cursor.execute(consulta, (email,)) 
        datos = cursor.fetchone() 
        #print("-----------------",datos)

        if datos:
            id, nombre, apellido, genero, email, password, mayor, rol, alta, image = datos
            usuario = Usuario(id, nombre, apellido, genero, email, password, mayor, rol, alta, image)
            config_db.conexion.close()
            return usuario
        else:
            config_db.conexion.close()
            print("Usuario no existe")
            return None
    
    @classmethod 
    def eliminar(cls, id):
        config_db.conexion.connect()
        consulta = f"DELETE FROM usuarios WHERE id = {id};"
        cursor = config_db.conexion.cursor()
        cursor.execute(consulta)
        config_db.conexion.commit()
        config_db.conexion.close()
        print("Usuario eliminado de la bd")
    
    @classmethod
    def agregar(cls, nombre, apellido, genero, email, password, mayor, rol, alta, image):
        hash_pass = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        alta = True
        rol = "USUARIO"
        consulta = f"INSERT INTO usuarios ( nombre, apellido, genero, email, password, mayor, rol, alta, image) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s);"
        config_db.conexion.connect()
        # config_db.conexion.cursor().execute(consulta, ( nombre, apellido, genero, email, password, mayor, alta, image))
        config_db.conexion.cursor().execute(consulta, ( nombre, apellido, genero, email, hash_pass, mayor, rol, alta, image))
        #cursor.execute(consulta,( nombre, email, password, mayor, alta, image))
        config_db.conexion.commit()
        config_db.conexion.close()
        print("Usuario agregado a la bd")
    
    @classmethod
    def verificar_password(cls, hashed_password, password):
        if isinstance(hashed_password, str):
            hashed_password = hashed_password.encode('utf-8')
        return bcrypt.checkpw(password.encode('utf-8'), hashed_password)
    
    @classmethod
    def modificar(cls, id, nombre = None, apellido = None, genero = None, email = None, password = None, mayor = None, rol = None, alta = None, image = None):
        usuario = cls.obtener_uno(id)
        #print(usuario.nombre, usuario.apellido)
        if usuario:
            if nombre is not None:
                usuario.nombre = nombre
            if apellido is not None:
                usuario.apellido = apellido
            if genero is not None:
                usuario.genero = genero
            if email is not None:
                usuario.email = email
            if password is not None:
                usuario.password = password
            if mayor is not None:
                usuario.mayor = mayor
            if rol is not None:
                usuario.rol = rol
            if alta is not None:
                usuario.alta = alta
            if image is not None:
                usuario.image = image

            config_db.conexion.connect()
            consulta = f"UPDATE usuarios SET nombre = %s, apellido = %s, genero = %s, email = %s, password = %s, mayor = %s, rol = %s, alta = %s, image = %s WHERE id = %s;"
            cursor = config_db.conexion.cursor()
            cursor.execute(consulta, (usuario.nombre, usuario.apellido, usuario.genero, usuario.email, usuario.password, usuario.mayor, usuario.rol, usuario.alta, usuario.image, usuario.id))
            config_db.conexion.commit()
            config_db.conexion.close()
            print("Usuario modificado")
        else:
            print("Usuario no encontrado")


