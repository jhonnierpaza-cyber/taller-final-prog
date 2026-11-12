<<<<<<< HEAD
<<<<<<< HEAD
dxfgfthmthctfcfjjggvgh
=======
=======
>>>>>>> 30b55040d9eb27b6afa9d3109d33df6ee86e6d0f

# ==========================================
# MODULO DE INVENTARIO
# SISTEMA DE GESTION DE SUPERMERCADO
# ==========================================

def convertir_entero(valor):
    numero = int(valor)

    if numero < 0:
        raise ValueError("El numero no puede ser negativo")
    return numero

def registrar_producto(productos, codigo, nombre, categoria,
            precio_compra, precio_venta, stock, stock_minimo):

    try:
        codigo = codigo.strip().upper()
        nombre = nombre.strip()
        categoria = categoria.strip()

        if codigo == "" or nombre == "" or categoria == "":
            return False, "Todos los campos son obligatorios"

        if codigo in productos:
            return False, "El codigo del producto ya existe"

        precio_compra = convertir_entero(precio_compra)
        precio_venta = convertir_entero(precio_venta)
        stock = convertir_entero(stock)
        stock_minimo = convertir_entero(stock_minimo)

        productos[codigo] = {
            "nombre": nombre,
            "categoria": categoria,
            "precio_compra": precio_compra,
            "precio_venta": precio_venta,
            "stock": stock,
            "stock_minimo": stock_minimo,
            "activo": True
        }

        return True, "Producto registrado correctamente"

    except ValueError:
        return False, "Ingrese valores numericos enteros y positivos"

# 2. EDITAR PRODUCTO
def editar_producto(productos, codigo, datos):

    if codigo not in productos:
        return False, "El producto no existe"

    try:
        producto = productos[codigo].copy()

        for campo in datos:

            if campo in ["precio_compra", "precio_venta",
                        "stock", "stock_minimo"]:

                producto[campo] = convertir_entero(datos[campo])

            elif campo in ["nombre", "categoria"]:
                valor = datos[campo].strip()
                if valor == "":
                    return False, "El campo no puede estar vacio"
                producto[campo] = valor
        productos[codigo] = producto

        return True, "Producto actualizado correctamente"

    except ValueError:
        return False, "Ingrese valores numericos validos"


def buscar_producto(productos, codigo):

    codigo = codigo.strip().upper()
    if codigo in productos:
        return productos[codigo]

    return None


def desactivar_producto(productos, codigo):
    codigo = codigo.strip().upper()

    if codigo not in productos:
        return False, "El producto no existe"
    productos[codigo]["activo"] = False
    return True, "Producto desactivado correctamente"

def consultar_inventario(productos):
    inventario = {}

    for codigo, datos in productos.items():
        if datos["activo"]:
            inventario[codigo] = datos.copy()
    return inventario

def registrar_entrada(productos, codigo, cantidad):

    try:
        codigo = codigo.strip().upper()
        cantidad = convertir_entero(cantidad)

        if cantidad == 0:
            return False, "La cantidad debe ser mayor que cero"

        if codigo not in productos:
            return False, "El producto no existe"

        if not productos[codigo]["activo"]:
            return False, "El producto esta desactivado"

        productos[codigo]["stock"] += cantidad

        return True, "Entrada registrada correctamente"

    except ValueError:
        return False, "Ingrese una cantidad numerica valida"

def registrar_salida(productos, codigo, cantidad):

    try:
        codigo = codigo.strip().upper()
        cantidad = convertir_entero(cantidad)

        if cantidad == 0:
            return False, "La cantidad debe ser mayor que cero"

        if codigo not in productos:
            return False, "El producto no existe"

        if not productos[codigo]["activo"]:
            return False, "El producto esta desactivado"

        if cantidad > productos[codigo]["stock"]:
            return False, "No hay suficiente inventario"

        productos[codigo]["stock"] -= cantidad
        return True, "Salida registrada correctamente"
    except ValueError:
        return False, "Ingrese una cantidad numerica valida"

def verificar_stock(productos):

    productos_bajos = {}
    for codigo, datos in productos.items():
        if datos["activo"] and datos["stock"] <= datos["stock_minimo"]:
            productos_bajos[codigo] = datos.copy()
<<<<<<< HEAD
    return productos_bajos
>>>>>>> ea5ceffeaa3f3dc22acb53f693358bfe2e0a36b0
=======
    return productos_bajos
>>>>>>> 30b55040d9eb27b6afa9d3109d33df6ee86e6d0f
