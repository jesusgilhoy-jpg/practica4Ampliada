import os
from dotenv import load_dotenv
from bbdd import ConexionBD

load_dotenv(os.path.join(os.path.dirname(__file__), '../Entyties/.env'))


class EtapaRepository:
    DB_CONFIG = {
        "host": os.getenv("DB_HOST", "127.0.0.1"),
        "port": int(os.getenv("DB_PORT", "33006")),
        "user": os.getenv("DB_USER", "root"),
        "password": os.getenv("DB_PASSWORD", "dbrootpass"),
        "database": os.getenv("DB_NAME", "ciclistas"),
    }

    def __init__(self):
        self.config = self.DB_CONFIG

    def obtener_etapas_cambio_ciudad(self) -> list:
        consulta = (
            "SELECT e2.netapa "
            "FROM etapa e1 "
            "JOIN etapa e2 ON e2.netapa = e1.netapa + 1 "
            "WHERE e2.salida <> e1.llegada"
        )
        with ConexionBD(self.config) as cnx:
            cursor = cnx.cursor()
            cursor.execute(consulta)
            resultado = []
            for (netapa,) in cursor:
                resultado.append(netapa)
            cursor.close()
            return resultado

    def crear_etapas(self, etapas: list[tuple]) -> None:
        consulta = (
            "INSERT INTO etapa (netapa, km, salida, llegada, dorsal) "
            "VALUES (%s, %s, %s, %s, %s)"
        )
        with ConexionBD(self.config) as cnx:
            cursor = cnx.cursor()
            cursor.executemany(consulta, etapas)
            cnx.commit()
            cursor.close()
