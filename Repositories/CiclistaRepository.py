import os
from dotenv import load_dotenv
from bbdd import ConexionBD

load_dotenv(os.path.join(os.path.dirname(__file__), '../Entyties/.env'))


class CiclistaRepository:
    DB_CONFIG = {
        "host": os.getenv("DB_HOST", "127.0.0.1"),
        "port": int(os.getenv("DB_PORT", "33006")),
        "user": os.getenv("DB_USER", "root"),
        "password": os.getenv("DB_PASSWORD", "dbrootpass"),
        "database": os.getenv("DB_NAME", "ciclistas"),
    }

    def __init__(self):
        self.config = self.DB_CONFIG

    def obtener_ganadores(self) -> list:
        consulta = (
            "SELECT p.nompuerto, p.categoria "
            "FROM puerto p "
            "JOIN ciclista c ON p.dorsal = c.dorsal "
            "WHERE c.nomeq = 'Banesto'"
        )
        with ConexionBD(self.config) as cnx:
            cursor = cnx.cursor()
            cursor.execute(consulta)
            resultado = []
            for nombre, categoria in cursor:
                resultado.append({
                    "nombre": nombre,
                    "categoria": categoria
                })
            cursor.close()
            return resultado

    def obtener_equipos_ciclistas_mayores_33(self) -> list:
        consulta = (
            "SELECT DISTINCT eq.nomeq, eq.director "
            "FROM equipo eq "
            "JOIN ciclista c ON eq.nomeq = c.nomeq "
            "WHERE c.edad > 33"
        )
        with ConexionBD(self.config) as cnx:
            cursor = cnx.cursor()
            cursor.execute(consulta)
            resultado = []
            for nomeq, director in cursor:
                resultado.append({
                    "nomeq": nomeq,
                    "director": director
                })
            cursor.close()
            return resultado

    def obtener_nombre_y_maillot(self) -> list:
        consulta = (
            "SELECT DISTINCT c.nombre, m.color "
            "FROM ciclista c "
            "JOIN llevar l ON c.dorsal = l.dorsal "
            "JOIN maillot m ON l.codigo = m.codigo"
        )
        with ConexionBD(self.config) as cnx:
            cursor = cnx.cursor()
            cursor.execute(consulta)
            resultado = []
            for nombre, color in cursor:
                resultado.append({
                    "nombre": nombre,
                    "color": color
                })
            cursor.close()
            return resultado

    def obtener_ciclistas_ganadores_maillot_amarillo(self) -> list:
        consulta = (
            "SELECT DISTINCT c.nombre, e.netapa "
            "FROM etapa e "
            "JOIN ciclista c ON e.dorsal = c.dorsal "
            "JOIN llevar l ON l.netapa = e.netapa AND l.dorsal = e.dorsal "
            "JOIN maillot m ON l.codigo = m.codigo "
            "WHERE m.color = 'Amarillo'"
        )
        with ConexionBD(self.config) as cnx:
            cursor = cnx.cursor()
            cursor.execute(consulta)
            resultado = []
            for nombre, netapa in cursor:
                resultado.append({
                    "nombre": nombre,
                    "netapa": netapa
                })
            cursor.close()
            return resultado

    def crear_ciclistas(self, ciclistas: list[tuple]) -> None:
        consulta = (
            "INSERT INTO ciclista (dorsal, nombre, edad, nomeq) "
            "VALUES (%s, %s, %s, %s)"
        )
        with ConexionBD(self.config) as cnx:
            cursor = cnx.cursor()
            cursor.executemany(consulta, ciclistas)
            cnx.commit()
            cursor.close()