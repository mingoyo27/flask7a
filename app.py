from flask import Flask, jsonify, render_template, request
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

        return jsonify({"status": "Registro exitoso"}), 200

    except mysql.connector.Error as err:
        return jsonify({"error": str(err)}), 500

    finally:
        if con.is_connected():
            con.close()

# Ruta para editar un contacto
@app.route("/editar", methods=["POST"])
def editar_contacto():
    data = request.get_json()
    Id_Contacto = data.get("id")
    correo_electronico = data.get("correo_electronico")
    nombre = data.get("nombre")
    asunto = data.get("asunto")

    try:
        con = obtener_conexion()
        cursor = con.cursor()

        # Actualizar contacto
        sql = "UPDATE tst0_contacto SET Correo_Electronico = %s, Nombre = %s, Asunto = %s WHERE Id_Contacto = %s"
        val = (correo_electronico, nombre, asunto, Id_Contacto)
        cursor.execute(sql, val)
        con.commit()

        return jsonify({"status": "Contacto actualizado correctamente"}), 200

    except mysql.connector.Error as err:
        return jsonify({"error": str(err)}), 500

    finally:
        if con.is_connected():
            con.close()

# Ruta para eliminar un contacto
@app.route("/eliminar/<int:Id_Contacto>", methods=["DELETE"])
def eliminar_contacto(Id_Contacto):
    try:
        con = obtener_conexion()
        cursor = con.cursor()

        # Eliminar contacto
        sql = "DELETE FROM tst0_contacto WHERE Id_Contacto = %s"
        cursor.execute(sql, (Id_Contacto,))
        con.commit()

        return jsonify({"status": "Contacto eliminado correctamente"}), 200

    except mysql.connector.Error as err:
        return jsonify({"error": str(err)}), 500

    finally:
        if con.is_connected():
            con.close()

if __name__ == "__main__":
    app.run(debug=True)
