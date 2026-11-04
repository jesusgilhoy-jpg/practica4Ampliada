import os
from dotenv import load_dotenv
from bbdd import ConexionBD

load_dotenv(os.path.join(os.path.dirname(__file__), '../Entyties/.env'))


class EquipoRepository:
    DB_CONFIG = {
        "host": os.getenv("DB_HOST", "127.0.0.1"),
        "port": int(os.getenv("DB_PORT", "33006")),
        "user": os.getenv("DB_USER", "root"),
        "password": os.getenv("DB_PASSWORD", "dbrootpass"),
        "database": os.getenv("DB_NAME", "ciclistas"),
    }

    def __init__(self):
        self.config = self.DB_CONFIG

    def obtener_equipos_con_conteo(self) -> list:
        consulta = (
            "SELECT eq.nomeq, COUNT(c.dorsal) as total_ciclistas "
            "FROM equipo eq "
            "JOIN ciclista c ON eq.nomeq = c.nomeq "
            "GROUP BY eq.nomeq"
        )
        with ConexionBD(self.config) as cnx:
            cursor = cnx.cursor()
            cursor.execute(consulta)
            resultado = []
            for nomeq, total in cursor:
                resultado.append({
                    "nomeq": nomeq,
                    "total_ciclistas": total
                })
            cursor.close()
            return resultado

    def crear_equipo(self, nomeq: str, director: str) -> None:
        consulta = "INSERT INTO equipo (nomeq, director) VALUES (%s, %s)"
        with ConexionBD(self.config) as cnx:
            cursor = cnx.cursor()
            cursor.execute(consulta, (nomeq, director))
            cnx.commit()
            cursor.close()
