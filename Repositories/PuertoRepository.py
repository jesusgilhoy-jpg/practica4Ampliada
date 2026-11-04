import os
from dotenv import load_dotenv
from bbdd import ConexionBD

load_dotenv(os.path.join(os.path.dirname(__file__), '../Entyties/.env'))


class PuertoRepository:
    DB_CONFIG = {
        "host": os.getenv("DB_HOST", "127.0.0.1"),
        "port": int(os.getenv("DB_PORT", "33006")),
        "user": os.getenv("DB_USER", "root"),
        "password": os.getenv("DB_PASSWORD", "dbrootpass"),
        "database": os.getenv("DB_NAME", "ciclistas"),
    }

    def __init__(self):
        self.config = self.DB_CONFIG

    def obtener_puertos_con_km(self) -> list:
        consulta = (
            "SELECT p.nompuerto, p.netapa, e.km "
            "FROM puerto p "
            "JOIN etapa e ON p.netapa = e.netapa"
        )

        with ConexionBD(self.config) as cnx:
            cursor = cnx.cursor()
            cursor.execute(consulta)
            resultado = []

            for nombre, etapa, km in cursor:
                resultado.append({
                    "nombre puerto": nombre,
                    "netapa": etapa,
                    "km": km
                })
            cursor.close()
            return resultado