from cmath import e
#from crypt import methods
from flask import Flask, jsonify, request
from flask_mysqldb import MySQL
from config import config


app = Flask(__name__)#Con este parametro comprobamos si se ejecuta este archivo como el principal

conexion = MySQL(app)#Seteamos la conexion

#FUNCIÓN LISTAR CURSOS
@app.route('/cursos') #preestablecemos la ruta raiz y el método
def listar_cursos(): # Creamos la funcion listar
    try:
        cursor=conexion.connection.cursor()
        sql="SELECT codigo, nombre, creditos FROM cursos"
        cursor.execute(sql)
        datos=cursor.fetchall()
        #print(datos)
        cursos=[]
        for fila in datos:
            curso = {'codigo':fila[0], 'nombre':fila[1], 'creditos':fila[2]}#Creamos diccionario para almacenar los datos en JSON
            cursos.append(curso)#Cada que se cree un curso lo anexamos a la lista
            
        return jsonify({'cursos':cursos,'mensaje':"Cursos listados."})#Retornamos el Json con la consulta

    except Exception as e:
        return jsonify({'mensaje':"Error"})

@app.route('/cursos/<codigo>')
def leer_curso(codigo):
    try:
        cursor=conexion.connection.cursor()
        sql="SELECT codigo, nombre, creditos FROM cursos WHERE codigo = '{0}'".format(codigo)
        cursor.execute(sql)
        datos=cursor.fetchone()
        if datos!= None:
            curso = {'codigo':datos[0], 'nombre':datos[1], 'creditos':datos[2]}
            return jsonify({'curso':curso,'mensaje':"Curso Encontrado."})
        else:
            return jsonify({'mensaje':"Curso no encontrado."})

    except Exception as e:
        return jsonify({'mensaje':"Error"})

@app.route('/cursos')#methods =['POST']
def registrar_curso():
    try:
        cursor=conexion.connection.cursor()
        sql="""INSERT INTO  curso (codigo, nombre, creditos)
         VALUES ('{0}','{1}','{2}')""".format(request.json['codigo'], request.json['nombre'], request.json['creditos'])
        cursor.execute(sql)
        conexion.connection.commit()# Confirmamos la acción de inserción
        #print(request.json)
        return({'mensaje':"Curso registrado."})
    except Exception as e:
        return jsonify({'mensaje':"Error"})

@app.route('/cursos/<codigo>')#methods =['PUT']
def modificar_curso(codigo):
    try:
        cursor=conexion.connection.cursor()
        sql="UPDATE curso SET nombre = '{0}', creditos = '{1}' WHERE codigo = '{2}'".format(request.json['nombre'], request.json['creditos'], codigo)
        cursor.execute(sql)
        conexion.connection.commit()# Confirmamos la acción de inserción
        #print(request.json)
        return({'mensaje':"Curso actualizado."})
    except Exception as e:
        return jsonify({'mensaje':"Error"})
        
@app.route('/cursos/<codigo>')#methods =['DELETE']
def eliminar_curso(codigo):
    try:
        cursor=conexion.connection.cursor()
        sql=" DELETE FROM curso WHERE codigo = '{0}'".format(codigo)
        cursor.execute(sql)
        conexion.connection.commit()# Confirmamos la acción de inserción
        #print(request.json)
        return({'mensaje':"Curso eliminado."})
    except Exception as e:
        return jsonify({'mensaje':"Error"})       

def pag_no_encontrada(error):
    return "<h1>La página que buscas no existe</h1>",404 #Mensae de respuesta mas el código del error

if __name__=='__main__':#Se hace la comprobación
    app.config.from_object(config['development'])
    app.register_error_handler(404, pag_no_encontrada)#Registramos el manejador de errores
    app.run()# DSi es así ejecutamos la app mediante el método run en modo dev
    