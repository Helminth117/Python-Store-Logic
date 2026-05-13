# ============================================================
#  Tienda RPG - Sistema de Inventario y Ventas
# ============================================================

from datetime import datetime

# ── Inventario principal ──────────────
inventario = {
    "espada_de_fuego": {
        "nombre": "Espada de Fuego",
        "tipo": "arma",
        "precio": 1500,
        "cantidad": 4,
        "stats": {"ataque": 85, "velocidad": 60, "magia": 10},
        "rareza": "raro",
    },
    "baston_arcano": {
        "nombre": "Bastón Arcano",
        "tipo": "arma",
        "precio": 2000,
        "cantidad": 2,
        "stats": {"ataque": 40, "velocidad": 30, "magia": 120},
        "rareza": "épico",
    },
    "pocion_vida": {
        "nombre": "Poción de Vida",
        "tipo": "consumible",
        "precio": 150,
        "cantidad": 5,
        "stats": {"curacion": 200},
        "rareza": "común",
    },
    "armadura_dragon": {
        "nombre": "Armadura del Dragón",
        "tipo": "armadura",
        "precio": 5000,
        "cantidad": 10,
        "stats": {"defensa": 150, "resistencia_fuego": 80},
        "rareza": "legendario",
    },
    "bota_velocidad": {
        "nombre": "Botas de Velocidad",
        "tipo": "accesorio",
        "precio": 800,
        "cantidad": 5,
        "stats": {"velocidad": 90, "agilidad": 70},
        "rareza": "raro",
    },
}

# ── Clientes registrados ───────────────────────────────────
clientes = {
    "C001": {"nombre": "Arturia", "oro": 100000, "historial": []},
    "C002": {"nombre": "Emiya",   "oro": 4500, "historial": []},
    "C003": {"nombre": "Rin",     "oro": 6500, "historial": []},
    "C004": {"nombre": "Gilgamesh", "oro": 1000000, "historial":[]},
    "C005": {"nombre": "Amy", "oro": 1, "historial":[]}
}

# ── Registro de ventas del día ─────────────────────────────
ventas_del_dia: list[dict] = []


# ════════════════════════════════════════════════════════════
#  FUNCIONES
# ════════════════════════════════════════════════════════════

def mostrar_inventario(filtro_tipo: str | None = None) -> None:
    """Muestra el inventario, opcionalmente filtrado por tipo."""
    print("\n" + "═" * 55)
    print(f"  📦  INVENTARIO {'(' + filtro_tipo.upper() + ')' if filtro_tipo else 'COMPLETO'}")
    print("═" * 55)

    items = {
        k: v for k, v in inventario.items()
        if filtro_tipo is None or v["tipo"] == filtro_tipo
    }

    if not items:
        print("  No hay items con ese filtro.")
        return

    for clave, item in items.items():
        stats_str = " | ".join(f"{k}: {v}" for k, v in item["stats"].items())
        print(
            f"  [{item['rareza'].upper():10}] {item['nombre']:<25} "
            f"💰 {item['precio']:>5} oro  x{item['cantidad']}\n"
            f"           Stats → {stats_str}"
        )
    print("═" * 55)


def comprar(id_cliente: str, id_item: str, cantidad: int = 1) -> bool:
    """Procesa la compra de un item por un cliente."""
    # Validaciones usando .get() para evitar KeyError
    cliente = clientes.get(id_cliente)
    item    = inventario.get(id_item)

    if not cliente:
        print(f"  ❌ Cliente '{id_cliente}' no encontrado.")
        return False
    if not item:
        print(f"  ❌ Item '{id_item}' no existe en el inventario.")
        return False
    if item["cantidad"] < cantidad:
        print(f"  ❌ Stock insuficiente. Disponibles: {item['cantidad']}")
        return False

    costo_total = item["precio"] * cantidad

    if cliente["oro"] < costo_total:
        falta = costo_total - cliente["oro"]
        print(f"  ❌ {cliente['nombre']} no tiene oro suficiente. Le faltan {falta} oro.")
        return False

    # Actualizar estado
    cliente["oro"]    -= costo_total
    item["cantidad"]  -= cantidad

    # Registrar en el historial del cliente
    registro = {
        "item": item["nombre"],
        "cantidad": cantidad,
        "costo": costo_total,
        "hora": datetime.now().strftime("%H:%M:%S"),
    }
    cliente["historial"].append(registro)
    ventas_del_dia.append({"cliente": cliente["nombre"], **registro})

    print(
        f"  ✅ {cliente['nombre']} compró {cantidad}x {item['nombre']} "
        f"por {costo_total} oro. Oro restante: {cliente['oro']}"
    )
    return True


def agregar_item(clave: str, datos: dict) -> None:
    """Añade o actualiza un item en el inventario."""
    if clave in inventario:
        inventario[clave]["cantidad"] += datos.get("cantidad", 0)
        print(f"  🔄 Stock de '{datos['nombre']}' actualizado.")
    else:
        inventario[clave] = datos
        print(f"  ➕ '{datos['nombre']}' añadido al inventario.")


def estadisticas() -> dict:
    """Calcula y muestra estadísticas usando comprensión de diccionarios."""
    print("\n" + "═" * 55)
    print("  📊  ESTADÍSTICAS DE LA TIENDA")
    print("═" * 55)

    # Valor total en stock por tipo
    valor_por_tipo: dict[str, int] = {}
    for item in inventario.values():
        tipo  = item["tipo"]
        valor = item["precio"] * item["cantidad"]
        valor_por_tipo[tipo] = valor_por_tipo.get(tipo, 0) + valor

    print("\n  Valor en stock por tipo:")
    for tipo, valor in sorted(valor_por_tipo.items(), key=lambda x: -x[1]):
        print(f"    {tipo:<15} → {valor:>8} oro")

    # Item más caro y más barato (comprensión de diccionario)
    precios = {k: v["precio"] for k, v in inventario.items()}
    mas_caro   = max(precios, key=precios.get)
    mas_barato = min(precios, key=precios.get)

    print(f"\n  Item más caro   : {inventario[mas_caro]['nombre']} ({precios[mas_caro]} oro)")
    print(f"  Item más barato : {inventario[mas_barato]['nombre']} ({precios[mas_barato]} oro)")

    # Resumen de ventas del día
    total_vendido = sum(v["costo"] for v in ventas_del_dia)
    print(f"\n  💵 Total recaudado hoy : {total_vendido} oro")
    print(f"  🛒 Transacciones       : {len(ventas_del_dia)}")

    if ventas_del_dia:
        # Cliente que más gastó (usando diccionario acumulador)
        gasto_cliente: dict[str, int] = {}
        for venta in ventas_del_dia:
            nombre = venta["cliente"]
            gasto_cliente[nombre] = gasto_cliente.get(nombre, 0) + venta["costo"]
        mejor_cliente = max(gasto_cliente, key=gasto_cliente.get)
        print(f"  🏆 Mejor cliente       : {mejor_cliente} ({gasto_cliente[mejor_cliente]} oro)")

    print("═" * 55)
    return valor_por_tipo


# ════════════════════════════════════════════════════════════
#  Salidaaaa
# ════════════════════════════════════════════════════════════

if __name__ == "__main__":
    mostrar_inventario()

    print("\n── Compras ──")
    comprar("C001", "armadura_dragon", 5)          
    comprar("C002", "espada_de_fuego")          
    comprar("C002", "espada_de_fuego", 2)      
    comprar("C003", "pocion_vida", 5)          
    comprar("C003", "baston_arcano", 2)       

    print("\n── Añadir nuevo item ──")
    agregar_item("espada_X", {
        "nombre": "X",
        "tipo": "arma",
        "precio": 1000000,
        "cantidad": 1,
        "stats": {"defensa": 50, "resistencia_magia": 200},
        "rareza": "legendaria",
    })

    mostrar_inventario(filtro_tipo="armadura")
    estadisticas()

print("\n" + "═" * 55)
print("\n── Clientes ──")
print("\n" + "═" * 55)

for cliente in clientes.values():
    print(f"- {cliente['nombre']}")
