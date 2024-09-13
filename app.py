from flask import Flask

from flask import render_template
from flask import request

import pusher

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("app.html")

@app.route("/alumnos")
def alumnos():
    return render_template("alumnos.html")

@app.route("/alumnos/guardar", methods=["GEt"])
def alumnosGuardar():
    matricula      = request.form["txtMatriculaFA"]
    nombreapellido = request.form["txtNombreApellidoFA"]
    return f"Matrícula: {matricula} Nombre y Apellido: {nombreapellido}"

@app.route("/evento")
def evento():
   import pusher

pusher_client = pusher.Pusher(
  app_id='1864234',
  key='97e3a65a4669fc2eb4bd',
  secret='6cd2985bbce79a4bf274',
  cluster='us2',
  ssl=True
)

pusher_client.trigger("conexion", "evento", request.args)
