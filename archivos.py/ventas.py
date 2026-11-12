
# ==========================================
# MODULO DE VENTAS
# ==========================================

# Porcentajes iniciales.
# Se pueden modificar cuando se definan las reglas del supermercado.
PORCENTAJE_DESCUENTO = 0
PORCENTAJE_IVA = 0


# Lista donde se guardan las facturas realizadas
ventas_realizadas = []


# ==========================================
# 1. AGREGAR PRODUCTOS AL CARRITO
# ==========================================

def agregar_carrito(productos, carrito):

    codigo = input("Ingrese el codigo del producto: ").strip().upper()

    if codigo not in productos:
        print("El producto no existe.")
        return

    producto = productos[codigo]

    if not producto["activo"]:
        print("Este producto esta desactivado.")
        return

    try:
        cantidad = int(input("Ingrese la cantidad que desea comprar: "))

        if cantidad <= 0:
            print("La cantidad debe ser mayor que cero.")
            return

        cantidad_actual = 0

        if codigo in carrito:
            cantidad_actual = carrito[codigo]["cantidad"]

        disponible = producto["stock"] - cantidad_actual

        if cantidad > disponible:
            print("Stock insuficiente. Unidades disponibles:", disponible)
            return

        if codigo in carrito:
            carrito[codigo]["cantidad"] += cantidad

        else:
            carrito[codigo] = {
                "nombre": producto["nombre"],
                "precio": producto["precio_venta"],
                "cantidad": cantidad
            }

        print("Producto agregado correctamente al carrito.")

    except ValueError:
        print("Error: debe ingresar una cantidad numerica.")
        return


# ==========================================
# 2. RETIRAR PRODUCTOS DEL CARRITO
# ==========================================

def retirar_carrito(carrito):

    if not carrito:
        print("El carrito esta vacio.")
        return

    codigo = input("Ingrese el codigo del producto que desea retirar: ").strip().upper()

    if codigo not in carrito:
        print("El producto no se encuentra en el carrito.")
        return

    del carrito[codigo]

    print("Producto retirado correctamente.")


# ==========================================
# 3. CALCULAR SUBTOTAL
# ==========================================

def calcular_subtotal(carrito):

    subtotal = 0

    for codigo, producto in carrito.items():

        subtotal += producto["precio"] * producto["cantidad"]

    return subtotal


# ==========================================
# 4. CALCULAR DESCUENTO
# ==========================================

def calcular_descuento(subtotal, porcentaje=PORCENTAJE_DESCUENTO):

    descuento = subtotal * porcentaje / 100

    return descuento


# ==========================================
# 5. CALCULAR IMPUESTO
# ==========================================

def calcular_impuesto(base, porcentaje=PORCENTAJE_IVA):

    impuesto = base * porcentaje / 100

    return impuesto


# ==========================================
# 6. PROCESAR PAGO
# ==========================================

def procesar_pago(total):

    while True:

        try:
            pago = float(input("Ingrese el dinero recibido: $"))

            if pago <= 0:
                print("El pago debe ser mayor que cero.")
                continue

            if pago < total:
                print("Dinero insuficiente. Falta: $", round(total - pago, 2))
                continue

            cambio = pago - total

            print("Pago realizado correctamente.")
            print("Su cambio es: $", round(cambio, 2))

            return pago, cambio

        except ValueError:
            print("Error: ingrese un valor numerico.")
            continue


# ==========================================
# 7. GENERAR FACTURA
# ==========================================

def generar_factura(carrito, subtotal, descuento, impuesto, total, pago, cambio):

    factura = {
        "numero": len(ventas_realizadas) + 1,
        "productos": {},
        "subtotal": subtotal,
        "descuento": descuento,
        "impuesto": impuesto,
        "total": total,
        "pago": pago,
        "cambio": cambio,
        "devueltos": {}
    }

    # Copiar los productos vendidos a la factura
    for codigo, producto in carrito.items():

        factura["productos"][codigo] = {
            "nombre": producto["nombre"],
            "precio": producto["precio"],
            "cantidad": producto["cantidad"]
        }

    ventas_realizadas.append(factura)

    print("\n========== FACTURA ==========")
    print("Numero de factura:", factura["numero"])

    for codigo, producto in factura["productos"].items():

        valor = producto["precio"] * producto["cantidad"]

        print(
            producto["nombre"],
            "x", producto["cantidad"],
            "=", "$", round(valor, 2)
        )

    print("-----------------------------")
    print("Subtotal: $", round(subtotal, 2))
    print("Descuento: $", round(descuento, 2))
    print("Impuesto: $", round(impuesto, 2))
    print("TOTAL: $", round(total, 2))
    print("Pago: $", round(pago, 2))
    print("Cambio: $", round(cambio, 2))
    print("=============================")

    return factura


# ==========================================
# 8. REGISTRAR DEVOLUCION
# ==========================================

def registrar_devolucion(productos, ventas):

    if not ventas:
        print("No hay ventas registradas para devolver.")
        return

    try:
        numero = int(input("Ingrese el numero de factura: "))

        factura_encontrada = None

        for factura in ventas:

            if factura["numero"] == numero:
                factura_encontrada = factura
                break

        if factura_encontrada is None:
            print("La factura no existe.")
            return

        codigo = input("Ingrese el codigo del producto: ").strip().upper()

        if codigo not in factura_encontrada["productos"]:
            print("Este producto no aparece en la factura.")
            return

        cantidad = int(input("Ingrese la cantidad que desea devolver: "))

        if cantidad <= 0:
            print("La cantidad debe ser mayor que cero.")
            return

        producto_vendido = factura_encontrada["productos"][codigo]

        cantidad_vendida = producto_vendido["cantidad"]

        cantidad_devuelta = factura_encontrada["devueltos"].get(codigo, 0)

        disponible_devolucion = cantidad_vendida - cantidad_devuelta

        if cantidad > disponible_devolucion:
            print("No puede devolver mas unidades de las compradas.")
            return

        productos[codigo]["stock"] += cantidad

        factura_encontrada["devueltos"][codigo] = cantidad_devuelta + cantidad

        print("Devolucion registrada correctamente.")
        print("Inventario actualizado.")

    except ValueError:
        print("Error: ingrese un numero valido.")
        return


# ==========================================
# MENU PRINCIPAL DE VENTAS
# ==========================================

def menu_ventas(productos):

    carrito = {}

    while True:

        print("\n========== MENU DE VENTAS ==========")
        print("1. Agregar producto al carrito")
        print("2. Retirar producto del carrito")
        print("3. Mostrar subtotal")
        print("4. Procesar venta")
        print("5. Registrar devolucion")
        print("6. Mostrar ventas realizadas")
        print("7. Salir")

        try:
            opcion = int(input("Seleccione una opcion: "))

            if opcion == 1:

                agregar_carrito(productos, carrito)

            elif opcion == 2:

                retirar_carrito(carrito)

            elif opcion == 3:

                if not carrito:
                    print("El carrito esta vacio.")

                else:
                    subtotal = calcular_subtotal(carrito)
                    print("El subtotal es: $", round(subtotal, 2))

            elif opcion == 4:

                if not carrito:
                    print("No puede procesar una venta con el carrito vacio.")
                    continue

                subtotal = calcular_subtotal(carrito)
                descuento = calcular_descuento(subtotal)
                base = subtotal - descuento
                impuesto = calcular_impuesto(base)
                total = base + impuesto
                print("Total a pagar: $", round(total, 2))

                pago, cambio = procesar_pago(total)

                for codigo, producto in carrito.items():

                    productos[codigo]["stock"] -= producto["cantidad"]

                generar_factura(
                    carrito,
                    subtotal,
                    descuento,
                    impuesto,
                    total,
                    pago,
                    cambio
                )

                carrito.clear()

            elif opcion == 5:
                registrar_devolucion(productos, ventas_realizadas)
            elif opcion == 6:

                if not ventas_realizadas:
                    print("Todavia no hay ventas realizadas.")

                else:
                    for factura in ventas_realizadas:
                        print(
                            "Factura:", factura["numero"],
                            "| Total: $", round(factura["total"], 2)
                        )

            elif opcion == 7:

                print("Saliendo del modulo de ventas...")
                break

            else:
                print("Opcion incorrecta. Intente nuevamente.")

        except ValueError:
            print("Error: debe ingresar una opcion numerica.")
            continue
