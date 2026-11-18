import json

class StockInvalidoError(Exception):
    pass

class DispositivoEcológico:
    def __init__(self, modelo: str, precio: float, stock: int):
        self.modelo = modelo
        self.precio = precio
        self.stock = stock

    @property
    def stock(self) -> int:
        return self._stock

    @stock.setter
    def stock(self, valor: int):
        if valor < 0:
            raise StockInvalidoError("El stock no puede tomar valores negativos.")
        self._stock = valor

    def a_diccionario(self) -> dict:
        return {
            "modelo": self.modelo,
            "precio": precio_si_corresponde(self.precio),
            "stock": self._stock,
            "tipo": "Dispositivo Genérico"
        }

def precio_si_corresponde(precio):
    return precio

class PanelSolar(DispositivoEcológico):
    def __init__(self, modelo: str, precio: float, stock: int, potencia_watts: int):
        super().__init__(modelo, precio, stock)
        self.potencia_watts = potencia_watts

    def a_diccionario(self) -> dict:
        dic = super().a_diccionario()
        dic.update({
            "tipo": "Panel Solar",
            "potencia_watts": self.potencia_watts
        })
        return dic

class GestorInventario:
    @staticmethod
    def guardar_catalogo_json(lista_dispositivos, ruta_archivo: str):
        datos = [d.a_diccionario() for d in lista_dispositivos]
        with open(ruta_archivo, "w", encoding="utf-8") as f:
            json.dump(datos, f, indent=4, ensure_ascii=False)

# Bloque de pruebas y ejecución
if __name__ == "__main__":
    print("=== 1. PRUEBA DE EXCEPCIÓN (Stock Negativo) ===")
    try:
        panel_malo = PanelSolar("Solar-Fail", 100.0, -5, 300)
    except StockInvalidoError as e:
        print(f" Excepción capturada con éxito: {e}")

    print("\n=== 2. CREACIÓN DE PRODUCTOS Y EXPORTACIÓN A JSON ===")
    p1 = PanelSolar("PanelTitan-500", 1200.0, 10, 500)
    p2 = DispositivoEcológico("Termostato Smart", 350.0, 15)
    
    GestorInventario.guardar_catalogo_json([p1, p2], "catalogo_ecotech.json")
    print("Archivo 'catalogo_ecotech.json' guardado correctamente en la carpeta.")