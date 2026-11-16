# Usa o PyMySQL como driver do MySQL (mais fácil de instalar no Windows)
import pymysql

pymysql.version_info = (2, 2, 1, "final", 0)  # o Django exige essa versão mínima
pymysql.install_as_MySQLdb()
