import os
from dotenv import load_dotenv
from bbdd import inicializar_base_datos
from Repositories.CiclistaRepository import CiclistaRepository
from Repositories.PuertoRepository import PuertoRepository
from Repositories.EquipoRepository import EquipoRepository
from Repositories.EtapaRepository import EtapaRepository

load_dotenv('Entyties/.env')

DB_CONFIG = {
    "host": os.getenv("DB_HOST", "127.0.0.1"),
    "port": int(os.getenv("DB_PORT", "33006")),
    "user": os.getenv("DB_USER", "root"),
    "password": os.getenv("DB_PASSWORD", "dbrootpass"),
    "database": os.getenv("DB_NAME", "ciclistas"),
}

def mostrar_menu():
    print("\n--- MENÚ PRÁCTICA 4 AMPLIACIÓN - CICLISTAS ---")
    print("1. Inicializar base de datos (crear BD y cargar ciclistas.sql)")
    print("2. Puertos ganados por ciclistas del equipo 'Banesto'")
    print("3. Puertos con número de etapa y kilómetros")
    print("4. Equipos con ciclistas mayores de 33 años")
    print("5. Ciclistas y colores de maillots llevados")
    print("6. Ciclistas ganadores de etapa que llevaron maillot Amarillo")
    print("7. Etapas que no comienzan en la ciudad donde acabó la anterior")
    print("8. Equipos con número de ciclistas")
    print("9. Crear un equipo")
    print("10. Crear 5 ciclistas asociados al equipo creado")
    print("11. Crear 3 etapas con ciclistas ganadores creados anteriormente")
    print("0. Salir")

def main():
    ciclista_repo = CiclistaRepository()
    puerto_repo = PuertoRepository()
    equipo_repo = EquipoRepository()
    etapa_repo = EtapaRepository()

    while True:
        mostrar_menu()
        opcion = input("\nSeleccione una opción: ").strip()

        if opcion == "1":
            try:
                inicializar_base_datos(DB_CONFIG)
                print("Base de datos 'ciclistas' inicializada y cargada correctamente desde ciclistas.sql.")
            except Exception as e:
                print(f"Error al inicializar la base de datos: {e}")

        elif opcion == "2":
            try:
                res = ciclista_repo.obtener_ganadores()
                print("\nPuertos ganados por ciclistas del equipo 'Banesto':")
                for r in res:
                    print(f"- Puerto: {r['nombre']}, Categoría: {r['categoria']}")
            except Exception as e:
                print(f"Error: {e}")

        elif opcion == "3":
            try:
                res = puerto_repo.obtener_puertos_con_km()
                print("\nPuertos, etapa y kilómetros:")
                for r in res:
                    print(f"- Puerto: {r['nombre puerto']}, Etapa: {r['netapa']}, Km: {r['km']}")
            except Exception as e:
                print(f"Error: {e}")

        elif opcion == "4":
            try:
                res = ciclista_repo.obtener_equipos_ciclistas_mayores_33()
                print("\nEquipos con ciclistas mayores de 33 años:")
                for r in res:
                    print(f"- Equipo: {r['nomeq']}, Director: {r['director']}")
            except Exception as e:
                print(f"Error: {e}")

        elif opcion == "5":
            try:
                res = ciclista_repo.obtener_nombre_y_maillot()
                print("\nCiclistas y colores de maillots llevados:")
                for r in res:
                    print(f"- Ciclista: {r['nombre']}, Maillot: {r['color']}")
            except Exception as e:
                print(f"Error: {e}")

        elif opcion == "6":
            try:
                res = ciclista_repo.obtener_ciclistas_ganadores_maillot_amarillo()
                print("\nCiclistas ganadores de etapa que llevaron maillot Amarillo:")
                for r in res:
                    print(f"- Ciclista: {r['nombre']}, Etapa: {r['netapa']}")
            except Exception as e:
                print(f"Error: {e}")

        elif opcion == "7":
            try:
                res = etapa_repo.obtener_etapas_cambio_ciudad()
                print("\nEtapas donde la salida no coincide con la llegada de la etapa anterior:")
                for netapa in res:
                    print(f"- Etapa número: {netapa}")
            except Exception as e:
                print(f"Error: {e}")

        elif opcion == "8":
            try:
                res = equipo_repo.obtener_equipos_con_conteo()
                print("\nEquipos y número de ciclistas:")
                for r in res:
                    print(f"- Equipo: {r['nomeq']}, Ciclistas: {r['total_ciclistas']}")
            except Exception as e:
                print(f"Error: {e}")

        elif opcion == "9":
            try:
                nomeq = input("Nombre del nuevo equipo: ").strip()
                director = input("Director del equipo: ").strip()
                if nomeq and director:
                    equipo_repo.crear_equipo(nomeq, director)
                    print(f"Equipo '{nomeq}' creado con éxito.")
                else:
                    print("Nombre y director no pueden estar vacíos.")
            except Exception as e:
                print(f"Error: {e}")

        elif opcion == "10":
            try:
                nomeq = input("Nombre del equipo al que asociar los 5 ciclistas: ").strip()
                ciclistas = []
                print("Introduce 5 ciclistas:")
                for i in range(1, 6):
                    dorsal = int(input(f"  Dorsal ciclista {i}: "))
                    nombre = input(f"  Nombre ciclista {i}: ").strip()
                    edad = int(input(f"  Edad ciclista {i}: "))
                    ciclistas.append((dorsal, nombre, edad, nomeq))
                ciclista_repo.crear_ciclistas(ciclistas)
                print("5 ciclistas creados y asociados con éxito.")
            except Exception as e:
                print(f"Error: {e}")

        elif opcion == "11":
            try:
                etapas = []
                print("Introduce 3 etapas:")
                for i in range(1, 4):
                    netapa = int(input(f"  Número de etapa {i}: "))
                    km = int(input(f"  Kilómetros etapa {i}: "))
                    salida = input(f"  Ciudad de salida etapa {i}: ").strip()
                    llegada = input(f"  Ciudad de llegada etapa {i}: ").strip()
                    dorsal = int(input(f"  Dorsal ciclista ganador etapa {i}: "))
                    etapas.append((netapa, km, salida, llegada, dorsal))
                etapa_repo.crear_etapas(etapas)
                print("3 etapas creadas con éxito.")
            except Exception as e:
                print(f"Error: {e}")

        elif opcion == "0":
            print("Saliendo de la aplicación...")
            break
        else:
            print("Opción no válida. Inténtelo de nuevo.")

if __name__ == '__main__':
    main()
