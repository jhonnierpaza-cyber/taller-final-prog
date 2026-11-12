"""
pruebas.py
Pruebas documentadas (P01 a P15) de la lógica del sistema.

Se ejecutan con:  python pruebas.py
Usan una carpeta temporal: NO modifican los archivos JSON reales.
"""

import json
import os
import tempfile

import main as programa

# Todo el programa vive en main.py; estos nombres cortos apuntan a él.
persistencia = inv = vt = cj = programa

resultados = []


def prueba(codigo, descripcion, esperado):
    """Decorador: ejecuta la prueba y anota si pasó o falló."""
    def decorador(funcion):
        try:
            obtenido = funcion()
            estado = "OK"
        except AssertionError as error:
            obtenido = f"FALLÓ: {error}"
            estado = "FALLA"
        except Exception as error:  # cualquier otro error también es una falla
            obtenido = f"ERROR {type(error).__name__}: {error}"
            estado = "FALLA"
        resultados.append((codigo, descripcion, esperado, obtenido, estado))
        return funcion
    return decorador


def datos_base():
    """Devuelve (productos, ventas, caja) limpios para cada prueba."""
    productos = {}
    inv.registrar_producto(productos, "P001", "Arroz", "Granos", 3000, 4000, 50, 10)
    inv.registrar_producto(productos, "P002", "Leche", "Lácteos", 3200, 4200, 8, 10)
    ventas = {"siguiente_factura": 1, "facturas": []}
    caja = {"abierta": False, "monto_inicial": 0, "fecha_apertura": None,
            "movimientos": [], "historial": []}
    return productos, ventas, caja


def debe_fallar(funcion, texto_esperado):
    """Comprueba que la función lance ValueError con ese texto."""
    try:
        funcion()
    except ValueError as error:
        assert texto_esperado in str(error), f"mensaje inesperado: {error}"
        return str(error)
    raise AssertionError("no se rechazó la operación")


def vender(productos, ventas, caja, codigo, cantidad, pago):
    carrito = []
    vt.agregar_carrito(carrito, productos, codigo, cantidad)
    factura = vt.generar_factura(carrito, productos, ventas, pago)
    cj.registrar_movimiento(caja, "venta", "venta", factura["total"])
    return factura


# ---------------------------------------------------------------- P01
@prueba("P01", "Registrar un producto correctamente", "Aparece en el inventario y en productos.json")
def _():
    productos, _v, _c = datos_base()
    inv.registrar_producto(productos, "p003", "Pan", "Panadería", 1000, 1500, 20, 5)
    assert "P003" in dict(inv.consultar_inventario(productos))
    with tempfile.TemporaryDirectory() as carpeta:
        persistencia.CARPETA_DATOS = carpeta
        assert persistencia.guardar_datos("productos.json", productos)
        with open(os.path.join(carpeta, "productos.json"), encoding="utf-8") as f:
            assert "P003" in json.load(f)
    return "P003 en inventario y en el JSON"


# ---------------------------------------------------------------- P02
@prueba("P02", "Registrar un código duplicado", "Se rechaza con mensaje de error")
def _():
    productos, _v, _c = datos_base()
    return debe_fallar(lambda: inv.registrar_producto(
        productos, "P001", "Otro", "X", 1, 2, 1, 1), "El código P001 ya existe")


# ---------------------------------------------------------------- P03
@prueba("P03", "Consultar inventario", "Lista con el stock actual")
def _():
    productos, _v, _c = datos_base()
    lista = inv.consultar_inventario(productos)
    assert [c for c, _ in lista] == ["P001", "P002"]
    assert lista[0][1]["stock"] == 50
    return "P001=50, P002=8 (stock bajo: " + str(inv.es_stock_bajo(lista[1][1])) + ")"


# ---------------------------------------------------------------- P04
@prueba("P04", "Vender un producto disponible", "Baja el stock y se genera la factura")
def _():
    productos, ventas, caja = datos_base()
    cj.abrir_caja(caja, 100000)
    factura = vender(productos, ventas, caja, "P001", 2, 20000)
    assert productos["P001"]["stock"] == 48
    assert factura["numero"] == 1 and factura["subtotal"] == 8000
    assert factura["total"] == 9520  # 8000 + 19 % IVA
    assert factura["cambio"] == 20000 - 9520
    return f"Stock 48, factura {factura['numero']} por {factura['total']}"


# ---------------------------------------------------------------- P05
@prueba("P05", "Vender más unidades de las existentes", "Venta bloqueada; stock sin cambios")
def _():
    productos, ventas, caja = datos_base()
    mensaje = debe_fallar(lambda: vt.agregar_carrito([], productos, "P002", 9),
                          "Stock insuficiente: quedan 8")
    assert productos["P002"]["stock"] == 8 and ventas["facturas"] == []
    return mensaje


# ---------------------------------------------------------------- P06
@prueba("P06", "Realizar una devolución parcial", "El stock sube solo en lo devuelto")
def _():
    productos, ventas, caja = datos_base()
    cj.abrir_caja(caja, 100000)
    factura = vender(productos, ventas, caja, "P001", 5, 50000)
    assert productos["P001"]["stock"] == 45
    monto = vt.registrar_devolucion(factura, productos, {"P001": 2})
    assert productos["P001"]["stock"] == 47
    assert monto == round(2 * 4000 * factura["total"] / factura["subtotal"])
    return f"Stock 47, reembolso {monto}"


# ---------------------------------------------------------------- P07
@prueba("P07", "Cerrar y abrir el programa", "Los datos siguen disponibles")
def _():
    productos, _v, _c = datos_base()
    productos["P001"]["stock"] = 33
    with tempfile.TemporaryDirectory() as carpeta:
        persistencia.CARPETA_DATOS = carpeta
        persistencia.guardar_datos("productos.json", productos)
        recargado = persistencia.cargar_datos("productos.json", {})  # "al abrir de nuevo"
    assert recargado == productos and recargado["P001"]["stock"] == 33
    return "Datos idénticos tras volver a cargar"


# ---------------------------------------------------------------- P08
@prueba("P08", "Verificar el cierre de caja", "El total coincide con las ventas")
def _():
    productos, ventas, caja = datos_base()
    cj.abrir_caja(caja, 100000)
    f1 = vender(productos, ventas, caja, "P001", 2, 20000)
    f2 = vender(productos, ventas, caja, "P001", 1, 10000)
    resumen = cj.cerrar_caja(caja)
    suma = f1["total"] + f2["total"]
    assert resumen["ventas"] == suma and resumen["num_ventas"] == 2
    assert resumen["saldo_final"] == 100000 + suma
    assert caja["abierta"] is False and len(caja["historial"]) == 1
    return f"Ventas {suma}, saldo final {resumen['saldo_final']}"


# ---------------------------------------------------------------- P09
@prueba("P09", "Realizar una devolución total", "El stock vuelve al inicial y se reembolsa el total")
def _():
    productos, ventas, caja = datos_base()
    cj.abrir_caja(caja, 100000)
    factura = vender(productos, ventas, caja, "P001", 3, 20000)
    monto = vt.registrar_devolucion(factura, productos, {"P001": 3})
    assert productos["P001"]["stock"] == 50 and monto == factura["total"]
    debe_fallar(lambda: vt.registrar_devolucion(factura, productos, {"P001": 1}),
                "solo quedan 0 por devolver")
    return f"Stock 50, reembolso {monto} = total de la factura"


# ---------------------------------------------------------------- P10
@prueba("P10", "Pago insuficiente", "Se pide completar el pago; stock sin cambios")
def _():
    productos, ventas, caja = datos_base()
    carrito = []
    vt.agregar_carrito(carrito, productos, "P001", 2)
    mensaje = debe_fallar(lambda: vt.generar_factura(carrito, productos, ventas, 5000),
                          "Falta dinero para completar el pago")
    assert productos["P001"]["stock"] == 50 and ventas["facturas"] == []
    return mensaje


# ---------------------------------------------------------------- P11
@prueba("P11", "Vender un producto desactivado", "Se rechaza; el producto no se borra")
def _():
    productos, _v, _c = datos_base()
    inv.desactivar_producto(productos, "P001")
    assert "P001" in productos and productos["P001"]["activo"] is False
    assert "P001" not in dict(inv.consultar_inventario(productos))
    return debe_fallar(lambda: vt.agregar_carrito([], productos, "P001", 1), "desactivado")


# ---------------------------------------------------------------- P12
@prueba("P12", "Archivo JSON dañado o inexistente", "Inicia vacío, avisa y conserva copia del dañado")
def _():
    with tempfile.TemporaryDirectory() as carpeta:
        persistencia.CARPETA_DATOS = carpeta
        persistencia.ADVERTENCIAS.clear()
        with open(os.path.join(carpeta, "productos.json"), "w", encoding="utf-8") as f:
            f.write("{ esto no es json ")
        datos = persistencia.cargar_datos("productos.json", {})
        assert datos == {}
        assert os.path.exists(os.path.join(carpeta, "productos.json.danado"))
        inexistente = persistencia.cargar_datos("no_existe.json", {})
        assert inexistente == {}
        avisos = list(persistencia.ADVERTENCIAS)
        persistencia.ADVERTENCIAS.clear()
    assert len(avisos) == 2
    return avisos[0]


# ---------------------------------------------------------------- P13
@prueba("P13", "Precio negativo", "Se rechaza con mensaje de error")
def _():
    productos, _v, _c = datos_base()
    return debe_fallar(lambda: inv.registrar_producto(
        productos, "P050", "X", "Y", 100, -5, 1, 1), "El precio no puede ser negativo")


# ---------------------------------------------------------------- P14
@prueba("P14", "Cantidad incorrecta (texto, cero o negativa)", "Ingrese una cantidad válida")
def _():
    productos, _v, _c = datos_base()
    for malo in ("abc", "0", "-3", "", "2.5"):
        debe_fallar(lambda m=malo: vt.agregar_carrito([], productos, "P001", m),
                    "Ingrese una cantidad válida")
    return "abc, 0, -3, vacío y 2.5 rechazados"


# ---------------------------------------------------------------- P15
@prueba("P15", "Error al guardar", "No se guardó; el archivo anterior queda intacto")
def _():
    with tempfile.TemporaryDirectory() as carpeta:
        persistencia.CARPETA_DATOS = carpeta
        persistencia.ADVERTENCIAS.clear()
        assert persistencia.guardar_datos("caja.json", {"valor": 1})
        # Datos que JSON no puede escribir -> debe fallar sin tocar el original.
        assert persistencia.guardar_datos("caja.json", {"valor": object()}) is False
        with open(os.path.join(carpeta, "caja.json"), encoding="utf-8") as f:
            assert json.load(f) == {"valor": 1}
        sobrantes = [n for n in os.listdir(carpeta) if n.endswith(".tmp")]
        assert sobrantes == [], "quedó un archivo temporal"
        persistencia.ADVERTENCIAS.clear()
    return "Archivo anterior intacto y sin temporales"


# ---------------------------------------------------------------- Informe
if __name__ == "__main__":
    print(f"{'N.º':<5}{'Resultado':<10}{'Prueba':<48}Obtenido")
    print("-" * 110)
    for codigo, descripcion, esperado, obtenido, estado in resultados:
        print(f"{codigo:<5}{estado:<10}{descripcion:<48}{obtenido}")
    fallas = [r for r in resultados if r[4] != "OK"]
    print("-" * 110)
    print(f"{len(resultados) - len(fallas)} de {len(resultados)} pruebas correctas")
    raise SystemExit(1 if fallas else 0)
