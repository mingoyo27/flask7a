from flask import Flask, jsonify, render_template, request
import mysql.connector

app = Flask(__name__)

# Conexión a la base de datos
def obtener_conexion():
    return mysql.connector.connect(
        host="185.232.14.52",
        database="u760464709_tst_sep",
        user="u760464709_tst_sep_usr",
        password="dJ0CIAFF="
    )

@app.route("/editar", methods=["POST"])
def editar_contacto():
    data = request.form
    id = data.get("id")
    correo_electronico = data.get("correo_electronico")
    nombre = data.get("nombre")
    asunto = data.get("asunto")
    try:
        con = obtener_conexion()
        cursor = con.cursor()
        sql = "UPDATE tst0_contacto SET Correo_Electronico = %s, Nombre = %s, Asunto = %s WHERE id = %s"
        cursor.execute(sql, (correo_electronico, nombre, asunto, id))
        con.commit()
        return jsonify({"status": True})
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return jsonify({"status": False})
    finally:
        cursor.close()
        con.close()

@app.route("/eliminar/<int:id>", methods=["DELETE"])
def eliminar_contacto(id):
    try:
        con = obtener_conexion()
        cursor = con.cursor()
        sql = "DELETE FROM tst0_contacto WHERE id = %s"
        cursor.execute(sql, (id,))
        con.commit()
        return jsonify({"status": True})
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return jsonify({"status": False})
    finally:
        cursor.close()
        con.close()
