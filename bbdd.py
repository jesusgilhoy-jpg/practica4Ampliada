import os
import mysql.connector
from mysql.connector import errorcode

def inicializar_base_datos(config: dict) -> None:
    cfg = config.copy()
    db_name = cfg.pop("database", "ciclistas")
    cnx = mysql.connector.connect(**cfg)
    cursor = cnx.cursor()
    cursor.execute(f"CREATE DATABASE IF NOT EXISTS {db_name}")
    cursor.execute(f"USE {db_name}")
    
    sql_path = os.path.join(os.path.dirname(__file__), "ciclistas.sql")
    if os.path.exists(sql_path):
        with open(sql_path, "r", encoding="utf-8") as f:
            sql_script = f.read()
        
        sql_script = sql_script.replace("ENGINE=maria", "ENGINE=InnoDB").replace("ENGINE=MARIA", "ENGINE=InnoDB")
        
        clean_lines = []
        for line in sql_script.splitlines():
            stripped = line.strip()
            if stripped.startswith("#"):
                continue
            clean_lines.append(line)
        clean_script = "\n".join(clean_lines)
        
        for statement in clean_script.split(";"):
            statement = statement.strip()
            if statement:
                try:
                    cursor.execute(statement)
                except Exception as e:
                    print(f"Error executing: {statement[:40]}... -> {e}")
        cnx.commit()
    cursor.close()
    cnx.close()


class ConexionBD:
    """Gestor de contexto para una conexión MySQL."""

    def __init__(self, config: dict):
        self.config = config
        self.cnx = None

    def __enter__(self) -> mysql.connector.MySQLConnection:
        try:
            self.cnx = mysql.connector.connect(**self.config)
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                raise RuntimeError("Usuario o contraseña incorrectos") from err
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                raise RuntimeError(
                    f"La base de datos '{self.config.get('database')}' no existe. "
                    "¿Has cargado ciclistas.sql?"
                ) from err
            raise
        return self.cnx

    def __exit__(self, exc_type, exc_value, traceback) -> None:
        if self.cnx is not None and self.cnx.is_connected():
            self.cnx.close()
