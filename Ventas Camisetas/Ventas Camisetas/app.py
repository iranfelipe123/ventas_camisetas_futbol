from flask import *
import csv
from datetime import datetime
import os

app = Flask(__name__)
app.secret_key = 'tienda_futbol_premium_2026'

# PRODUCTOS USANDO TUS IMÁGENES LOCALES (.png) Y PRECIOS VARIABLES
PRODUCTOS = [
    {"id": 1, "nombre": "Real Madrid Local", "precio": 69990, "img": "/static/img/madrid.png"},
    {"id": 2, "nombre": "FC Barcelona Local", "precio": 59990, "img": "/static/img/barcelona.png"},
    {"id": 3, "nombre": "Manchester City Local", "precio": 55000, "img": "/static/img/city.png"},
    {"id": 4, "nombre": "Bayern Munich Local", "precio": 60000, "img": "/static/img/bayern.png"},
    {"id": 5, "nombre": "AC Milan Local", "precio": 50000, "img": "/static/img/milan.png"},
    {"id": 6, "nombre": "Liverpool FC Local", "precio": 65000, "img": "/static/img/liverpool.png"},
    {"id": 7, "nombre": "Inter Milán Local", "precio": 58990, "img": "/static/img/inter.png"},
]

@app.route('/')
def index():
    if 'carrito' not in session:
        session['carrito'] = []
    total_carrito = sum(item['precio'] for item in session['carrito'])
    return render_template('index.html', productos=PRODUCTOS, carrito=session['carrito'], total=total_carrito)

@app.route('/agregar/<int:id>')
def agregar(id):
    producto = next((p for p in PRODUCTOS if p['id'] == id), None)
    if producto:
        carrito = session.get('carrito', [])
        carrito.append(producto)
        session['carrito'] = carrito
    return redirect(url_for('index'))

@app.route('/limpiar')
def limpiar():
    session.pop('carrito', None)
    return redirect(url_for('index'))

@app.route('/checkout', methods=['POST'])
def checkout():
    carrito = session.get('carrito', [])
    if not carrito: return redirect(url_for('index'))

    datos = {
        "nombre": request.form.get('nombre'),
        "rut": request.form.get('rut'),
        "email": request.form.get('email'),
        "telefono": request.form.get('telefono'),
        "direccion": request.form.get('direccion')
    }

    total = sum(item['precio'] for item in carrito)
    file_exists = os.path.isfile('ventas.csv')
    with open('ventas.csv', mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        if not file_exists:
            writer.writerow(['Fecha', 'Cliente', 'RUT', 'Email', 'Telefono', 'Direccion', 'Productos', 'Total'])
        
        nombres_p = ", ".join([p['nombre'] for p in carrito])
        writer.writerow([datetime.now().strftime("%Y-%m-%d %H:%M"), datos['nombre'], datos['rut'], datos['email'], datos['telefono'], datos['direccion'], nombres_p, total])

    session.pop('carrito', None)
    return redirect("https://mpago.la/16LNvjf")

if __name__ == '__main__':
    app.run(debug=True)