from flask import Flask, render_template, request, redirect, session
from datetime import datetime
import uuid  # Para generar IDs únicos

app = Flask(__name__)
app.secret_key = 'clave_secreta_para_sesion'  # Necesaria para manejar sesiones

# Inicializamos los productos en la sesión si no existen
@app.before_request
def inicializar_sesion():
    if 'productos' not in session:
        session['productos'] = []

# Ruta principal para gestionar productos
@app.route('/')
def gestion_productos():
    return render_template('index.html', productos=session['productos'])

# Ruta para agregar un nuevo producto
@app.route('/agregar', methods=['GET', 'POST'])
def agregar_producto():
    if request.method == 'POST':
        nombre = request.form['nombre']
        cantidad = int(request.form['cantidad'])
        precio = float(request.form['precio'])
        fecha_vencimiento = request.form['fecha_vencimiento']
        categoria = request.form['categoria']
        
        # Creamos un nuevo producto con un ID único
        nuevo_producto = {
            'id': str(uuid.uuid4()),  # Generamos un ID único
            'nombre': nombre,
            'cantidad': cantidad,
            'precio': precio,
            'fecha_vencimiento': fecha_vencimiento,
            'categoria': categoria
        }
        
        # Agregamos el producto a la sesión
        productos = session['productos']
        productos.append(nuevo_producto)
        session['productos'] = productos
        
        return redirect('/')
    
    return render_template('agregar.html')

# Ruta para editar un producto
@app.route('/editar/<id>', methods=['GET', 'POST'])
def editar_producto(id):
    productos = session['productos']
    producto = next((p for p in productos if p['id'] == id), None)
    
    if request.method == 'POST':
        producto['nombre'] = request.form['nombre']
        producto['cantidad'] = int(request.form['cantidad'])
        producto['precio'] = float(request.form['precio'])
        producto['fecha_vencimiento'] = request.form['fecha_vencimiento']
        producto['categoria'] = request.form['categoria']
        
        session['productos'] = productos  # Guardamos cambios en la sesión
        return redirect('/')
    
    return render_template('editar.html', producto=producto)

# Ruta para eliminar un producto
@app.route('/eliminar/<id>', methods=['GET'])
def eliminar_producto(id):
    productos = session['productos']
    session['productos'] = [p for p in productos if p['id'] != id]  # Eliminamos el producto
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)