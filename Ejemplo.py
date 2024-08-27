import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter import messagebox as tkmsg
import sqlite3

# Conexión a la base de datos
conexion = sqlite3.connect('BaseDeDatos')
cursorBD = conexion.cursor()

# Crear o modificar la tabla PRODUCTO
def crear_tabla_producto():
    cursorBD.execute('''
        CREATE TABLE IF NOT EXISTS PRODUCTO (
            CODIGO INTEGER PRIMARY KEY AUTOINCREMENT, 
            NOMBRE TEXT, 
            DISTRIBUIDOR TEXT, 
            PRECIO_COMPRA REAL, 
            PRECIO_VENTA REAL
        )
    ''')
    conexion.commit()

crear_tabla_producto()

# Funciones CRUD
def insertarProducto(nombre, distribuidor, precio_compra, precio_venta):
    cursorBD.execute(''' INSERT INTO PRODUCTO (NOMBRE, DISTRIBUIDOR, PRECIO_COMPRA, PRECIO_VENTA) VALUES (?, ?, ?, ?)''', (nombre, distribuidor, precio_compra, precio_venta))
    conexion.commit()


def seleccionarItems():
    cursorBD.execute('SELECT * FROM PRODUCTO')
    lista = cursorBD.fetchall()
    return lista

def actualizarItem(codigo, diccionario):
    valoresValidos = ['NOMBRE', 'DISTRIBUIDOR', 'PRECIO_COMPRA', 'PRECIO_VENTA']
    for key in diccionario.keys():
        if key not in valoresValidos:
            raise Exception('Esa columna no existe, revise la sintaxis')

    for key in diccionario.keys():
        query = '''UPDATE PRODUCTO SET {} = '{}' WHERE CODIGO = {}'''.format(key, diccionario[key], codigo)
        cursorBD.execute(query)
    conexion.commit()

def borrarProducto(codigo):
    cursorBD.execute('''DELETE FROM PRODUCTO WHERE CODIGO = {}'''.format(codigo))
    conexion.commit()


def borrarProducto(codigo):
    cursorBD.execute('''DELETE FROM PRODUCTO WHERE CODIGO = ?''', (codigo,))
    conexion.commit()

def abrir_ventana_principal():

    #funciones para crear ventanas de los distintos roles
    def abrir_ventana_gerente():
        ventana_gerente = tk.Toplevel()
        ventana_gerente.title("Rol elegido: Gerente")
        ventana_gerente.geometry(centrar_ventana(ventana_gerente, 600, 600))

         # Variables de la interfaz
        nombre_var = tk.StringVar()
        distribuidor_var = tk.StringVar()
        precio_compra_var = tk.StringVar()
        precio_venta_var = tk.StringVar()
    
        # Función para actualizar la lista de productos
        def actualizar_lista():
            lista_productos.delete(0, tk.END)
            productos = seleccionarItems()
            for producto in productos:
                print(producto)  # Imprime el producto para ver su estructura
                try:
                    lista_productos.insert(tk.END, f"Código: {producto[0]}, Nombre: {producto[1]}, Distribuidor: {producto[2]}, Precio Compra: {producto[3]}, Precio Venta: {producto[4]}")
                except IndexError:
                    tkmsg.showerror("Error", "Error al acceder a los datos del producto.")

        # Función para agregar producto
        def agregar_producto():
            nombre = nombre_var.get()
            distribuidor = distribuidor_var.get()
            precio_compra = precio_compra_var.get()
            precio_venta = precio_venta_var.get()

            if nombre and distribuidor and precio_compra and precio_venta:
                try:
                    insertarProducto(nombre, distribuidor, float(precio_compra), float(precio_venta))
                    actualizar_lista()
                    nombre_var.set("")
                    distribuidor_var.set("")
                    precio_compra_var.set("")
                    precio_venta_var.set("")
                except ValueError:
                    tkmsg.showerror("Error", "El precio debe ser un número.")
            else:
                tkmsg.showerror("Error", "Todos los campos son obligatorios.")

        # Función para eliminar producto
        def eliminar_producto():
            seleccion = lista_productos.curselection()
            if seleccion:
                producto = lista_productos.get(seleccion)
                codigo = int(producto.split(",")[0].split(":")[1].strip())
                borrarProducto(codigo)
                actualizar_lista()
            else:
                tkmsg.showwarning("Advertencia", "Debe seleccionar un producto para eliminar.")

        # Widgets de la interfaz
        tk.Label(ventana_gerente, text="Nombre del Producto").pack(pady=5)
        tk.Entry(ventana_gerente, textvariable=nombre_var).pack(pady=5)

        tk.Label(ventana_gerente, text="Nombre del distribuidor").pack(pady=5)
        tk.Entry(ventana_gerente, textvariable=distribuidor_var).pack(pady=5)

        tk.Label(ventana_gerente, text="Precio de compra").pack(pady=5)
        tk.Entry(ventana_gerente, textvariable=precio_compra_var).pack(pady=5)

        tk.Label(ventana_gerente, text="Precio de venta").pack(pady=5)
        tk.Entry(ventana_gerente, textvariable=precio_venta_var).pack(pady=5)

        tk.Button(ventana_gerente, text="Agregar Producto", command=agregar_producto).pack(pady=10)
        tk.Button(ventana_gerente, text="Eliminar Producto", command=eliminar_producto).pack(pady=5)

        # Listbox para mostrar productos
        lista_productos = tk.Listbox(ventana_gerente, width=80)
        lista_productos.pack(pady=20)

        # Inicializar lista de productos
        actualizar_lista()

    def abrir_ventana_administrador():
        ventana_administrador = tk.Toplevel()
        ventana_administrador.title("Rol elegifo: Administrador")
        ventana_administrador.geometry(centrar_ventana(ventana_administrador, 400, 400))

    def abrir_ventana_empacador():
        ventana_empacador = tk.Toplevel()
        ventana_empacador.title("Rol elegido: Empacador")
        ventana_empacador.geometry(centrar_ventana(ventana_empacador, 400, 400))

    def abrir_ventana_transportador():
        ventana_transportador = tk.Toplevel()
        ventana_transportador.title("Rol elegido: Transportador")
        ventana_transportador.geometry(centrar_ventana(ventana_transportador, 400, 400))

    def abrir_ventana_recepcionista():
        ventana_recepcionista = tk.Toplevel()
        ventana_recepcionista.title("Rol elegido: Recepcionista")
        ventana_recepcionista.geometry(centrar_ventana(ventana_recepcionista, 400, 400))

    #función del botón de consulta
    def boton_consulta():
        rol = cb.get()
        if rol == 'Gerente':
            abrir_ventana_gerente()
        elif rol == 'Administrador':
            abrir_ventana_administrador()
        elif rol == 'Empacador':
            abrir_ventana_empacador()
        elif rol == 'Transportador':
            abrir_ventana_transportador()
        elif rol == 'Recepcionista':
            abrir_ventana_recepcionista()
        else:
            tkmsg.showwarning("Selección no válida", "Por favor, seleccione un rol de la lista.")
            
            
    ventana_principal = Tk()
    ventana_principal.title('Comercializadora Gremlin')

    #Función para centrar la pantalla
    def centrar_ventana(ventana, ancho_ventana, alto_ventana):
        ancho_pantalla = ventana.winfo_screenwidth()
        alto_pantalla = ventana.winfo_screenheight()

        #Calcular el alto y el ancho
        posicion_x= (ancho_pantalla-ancho_ventana)//2
        posicion_y= (alto_pantalla-alto_ventana)//2

        return f"{ancho_ventana}x{alto_ventana}+{posicion_x}+{posicion_y}"

    #Colocando el ancho y el alto de la ventana de acuerdo a la pantalla
    ventana_principal.geometry(centrar_ventana(ventana_principal,550,250))
    
    #Creando un LabelFrame
    frame = LabelFrame(ventana_principal, relief="ridge", text="Bienvenidos a comercializadora Gremlin, seleccione su rol para continuar")
    frame.pack(padx=20, pady=10, fill="both", expand=True)

    #Creando comboBox y su lista contenedora para seleccionar el rol de la empresa
    roles = ['Gerente','Administrador','Empacador','Transportador', 'Recepcionista']
    cb = ttk.Combobox(frame, values=roles)
    cb.pack(padx=10, pady=20)
    #Realizando botón de consulta
    btn_consulta = Button(frame, text='Ingresar', command=boton_consulta)
    btn_consulta.pack(padx=10, pady=60)

    ventana_principal.mainloop()


 
if __name__ == "__main__":
    abrir_ventana_principal()


