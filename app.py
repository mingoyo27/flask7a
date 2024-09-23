from flask import Flask, jsonify
from flask import render_template
from flask import request
import pusher
import mysql.connector

app = Flask(__name__)

# Función para conectar a la base de datos
def obtener_conexion():
    return mysql.connector.connect(
        host="185.232.14.52",
        database="u760464709_tst_sep",
        user="u760464709_tst_sep_usr",
        password="dJ0CIAFF="
    )

# Ruta para la página principal con el formulario de contacto
@app.route("/")
def index():
    return render_template("app.html")

# Ruta para visualizar los contactos
@app.route("/visualizar_contactos")
def visualizar_contactos():
    return render_template("visualizar_contactos.html")

# Ruta para listar los contactos registrados
@app.route("/listar_contactos", methods=["GET"])
def listar_contactos():
    try:
        # Conexión a la base de datos
        con = obtener_conexion()
        cursor = con.cursor(dictionary=True)

        # Consulta para obtener todos los contactos
        cursor.execute("SELECT * FROM tst0_contacto")
        contactos = cursor.fetchall()

        con.close()

        # Devolver los datos en formato JSON
        return jsonify(contactos), 200

    except mysql.connector.Error as err:
        return jsonify({"error": str(err)}), 500

# Ruta para registrar un nuevo contacto desde el formulario
@app.route("/registrar", methods=["GET"])
def registrar():
    # Parámetros de la solicitud GET
    args = request.args
    correo_electronico = args.get("correo_electronico")
    nombre = args.get("nombre")
    asunto = args.get("asunto")

    try:
        # Conexión a la base de datos
        con = obtener_conexion()
        cursor = con.cursor()

        # Consulta SQL para insertar el registro
        sql = "INSERT INTO tst0_contacto (Correo_Electronico, Nombre, Asunto) VALUES (%s, %s, %s)"
        val = (correo_electronico, nombre, asunto)
        cursor.execute(sql, val)
        con.commit()

        # Enviar notificación con Pusher
        pusher_client = pusher.Pusher(
            app_id='1864234',
            key='97e3a65a4669fc2eb4bd',
            secret='6cd2985bbce79a4bf274',
            cluster='us2',
            ssl=True
        )

        pusher_client.trigger("registrosTiempoReal", "registroTiempoReal", {
            "correo_electronico": correo_electronico,
            "nombre": nombre,
            "asunto": asunto
        })

        return jsonify({"status": "Registro exitoso"}), 200

    except mysql.connector.Error as err:
        return jsonify({"error": str(err)}), 500

    finally:
        if con.is_connected():
            con.close()

if __name__ == "__main__":
    app.run(debug=True)
