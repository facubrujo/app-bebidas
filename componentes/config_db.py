import mysql.connector

datos_db = {
    'host' : 'localhost',
    'user' : 'root',
    'password' : 'root',
    'database' : 'cocktelesarg'#'nuevo'
}

# config_produccion = {}# esta se va a usar para la config de el despliegue

# mydb = mysql.connector.connect(
#     host = "localhost",#"127.0.0.1",#"localhost",
#     user = "root",
#     password = "root",
#     database = "cocktelesarg"#,#"mydatabase"
#     #charset="utf8mb4" 
# )

conexion = mysql.connector.connect(**datos_db)