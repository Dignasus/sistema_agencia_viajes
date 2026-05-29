import mysql.connector 
from mysql.connector import errorcode
from utils.password_encryptor import PasswordEncryptor 

# Configuración de la Base de Datos
HOST = 'localhost'
USER = 'root'
PASSWORD = ''
DATABASE = 'agencia_viajes'

def conectar(database=None):
    config = {
        'host': HOST,
        'user': USER,
        'password': PASSWORD,
    }
    if database:
        config['database'] = database

    return mysql.connector.connect(**config)

def crear_bd():
    """Crea la base de datos si no existe."""
    conn = conectar() 
    cursor = conn.cursor()

    try:
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DATABASE} CHARACTER SET utf8mb4;")
        print(f"Base de datos '{DATABASE}' verificada.")
    except mysql.connector.Error as err:
        print(f"Error al crear BD: {err}")

    conn.commit()
    cursor.close()
    conn.close()

def crear_tablas():
    #Crea las tablas necesarias si no existen
    conn = conectar(DATABASE) 
    cursor = conn.cursor()

    tablas = [
        # 1. Tabla Usuarios
        """
        CREATE TABLE IF NOT EXISTS usuarios (
            id INT AUTO_INCREMENT PRIMARY KEY,
            nombre VARCHAR(100) NOT NULL,
            apellido VARCHAR(100) NOT NULL,
            email VARCHAR(120) NOT NULL UNIQUE,
            telefono VARCHAR(30),
            direccion VARCHAR(200),
            contraseña_hash VARCHAR(255) NOT NULL,
            rol ENUM('cliente','admin') NOT NULL
        );
        """,
        # 2. Tabla Destinos
        """
        CREATE TABLE IF NOT EXISTS destinos (
            id_destino INT AUTO_INCREMENT PRIMARY KEY,
            nombre VARCHAR(100) NOT NULL,
            descripcion TEXT,
            actividades TEXT,
            costo_base DECIMAL(10,2) NOT NULL
        );
        """,
        # 3. Tabla Paquetes
        """
        CREATE TABLE IF NOT EXISTS paquetes (
            id_paquete INT AUTO_INCREMENT PRIMARY KEY,
            tipo ENUM('oficial', 'personalizado') NOT NULL,
            fecha_inicio DATE NOT NULL,
            fecha_fin DATE NOT NULL,
            precio_total DECIMAL(10,2),
            id_admin_creador INT NULL,
            id_cliente_creador INT NULL,
            nombre_paquete VARCHAR(120),
            FOREIGN KEY (id_admin_creador) REFERENCES usuarios(id),
            FOREIGN KEY (id_cliente_creador) REFERENCES usuarios(id)
        );
        """,
        # 4. Tabla Intermedia Paquetes-Destinos
        """
        CREATE TABLE IF NOT EXISTS paquetes_destinos (
            id_paquete INT NOT NULL,
            id_destino INT NOT NULL,
            PRIMARY KEY (id_paquete, id_destino),
            FOREIGN KEY (id_paquete) REFERENCES paquetes(id_paquete) ON DELETE CASCADE,
            FOREIGN KEY (id_destino) REFERENCES destinos(id_destino) ON DELETE CASCADE
        );
        """,
        # 5. Tabla Reservas
        """
        CREATE TABLE IF NOT EXISTS reservas (
            id_reserva INT AUTO_INCREMENT PRIMARY KEY,
            id_cliente INT NOT NULL,
            id_paquete INT NOT NULL,
            fecha_reserva DATE NOT NULL,
            estado VARCHAR(50) NOT NULL,
            FOREIGN KEY (id_cliente) REFERENCES usuarios(id),
            FOREIGN KEY (id_paquete) REFERENCES paquetes(id_paquete)
        );
        """,
        # 6. Tabla Logs (Auditoría)
        """
        CREATE TABLE IF NOT EXISTS logs (
            id_log INT AUTO_INCREMENT PRIMARY KEY,
            id_usuario INT NULL,
            accion VARCHAR(200) NOT NULL,
            fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            detalle TEXT,
            FOREIGN KEY (id_usuario) REFERENCES usuarios(id)
        );
        """
    ]

    for sql in tablas:
        cursor.execute(sql)
        conn.commit()

    cursor.close()
    conn.close()
    print("Tablas verificadas correctamente.")


def crear_admin_por_defecto():
    #Inserta un usuario administrador si no existe ninguno
    conn = conectar(DATABASE)
    cursor = conn.cursor()
    
    # Verificamos si ya existe el admin específico
    email_admin = "admin@agencia.com"
    cursor.execute("SELECT id FROM usuarios WHERE email = %s", (email_admin,))
    
    if cursor.fetchone():
        print("El usuario Admin ya existe. Omitiendo creación.")
    else:
        print("Creando usuario Administrador por defecto...")
        
        # Datos del Admin
        nombre = "Administrador"
        apellido = "Principal"
        password_plana = "admin123"
        telefono = "000000000"
        direccion = "Sede Central"
        rol = "admin"
        
        # Encriptación
        hashed_pass = PasswordEncryptor.hash_password(password_plana)
        
        sql = """
        INSERT INTO usuarios (nombre, apellido, email, telefono, direccion, contraseña_hash, rol)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        cursor.execute(sql, (nombre, apellido, email_admin, telefono, direccion, hashed_pass, rol))
        conn.commit()
        print(f"Usuario Admin creado: {email_admin} (Pass: {password_plana})")

    cursor.close()
    conn.close()

def crear_paquetes_iniciales():
    #Creamos 3 paquetes que se carguen automaticamente con la base de datos
    conn = conectar(DATABASE)
    cursor = conn.cursor()

    # 1. Verificar si ya hay paquetes (para no duplicar cada vez que inicias)
    cursor.execute("SELECT COUNT(*) FROM paquetes")
    cantidad = cursor.fetchone()[0]
    
    if cantidad > 0:
        print("Ya existen paquetes en la BD. Omitiendo creación automática.")
    else:
        print("Creando 3 paquetes iniciales...")

        # 2. Necesitamos el ID del Admin para ponerlo como creador
        cursor.execute("SELECT id FROM usuarios WHERE email = 'admin@agencia.com'")
        admin_row = cursor.fetchone()
        
        # Si por alguna razón no está el admin, usamos ID 1 a la fuerza o abortamos
        id_admin = admin_row[0] if admin_row else 1

        # 3. Datos de los 3 Paquetes
        paquetes_demo = [
            (
                "Escapada Torres del Paine", 450000, "2024-02-10", "2024-02-15", 
                #"Incluye trekking base torres, alojamiento en refugio y comidas.", 
                "oficial", id_admin
            ),
            (
                "Desierto Florido Full", 280000, "2024-03-01", "2024-03-05", 
                #"Recorrido por el desierto de Atacama y Valle de la Luna.", 
                "oficial", id_admin
            ),
            (
                "Ruta del Vino Colchagua", 150000, "2024-04-12", "2024-04-14", 
                #"Fin de semana de degustaciones y hotel boutique.", 
                "oficial", id_admin
            )
        ]

        sql = """
        INSERT INTO paquetes (
            nombre_paquete, precio_total, fecha_inicio, fecha_fin, 
            tipo, id_admin_creador
        ) 
        VALUES (%s, %s, %s, %s, %s, %s)
        """

        try:
            cursor.executemany(sql, paquetes_demo)
            conn.commit()
            print("Paquetes iniciales creados.")
        except Exception as e:
            print(f"Error creando paquetes iniciales: {e}")

    cursor.close()
    conn.close()

def crear_destinos_iniciales():
    #Creamos 5 destinos que se carguen automaticamente con la base de datos
    conn = conectar(DATABASE)
    cursor = conn.cursor()

    # 1. Verificar si ya hay paquetes (para no duplicar cada vez que inicias)
    cursor.execute("SELECT COUNT(*) FROM destinos")
    cantidad = cursor.fetchone()[0]
    
    if cantidad > 0:
        print("Ya existen destinos en la BD. Omitiendo creación automática.")
    else:
        print("Creando 5 destinos iniciales...")

        # Datos de los 5 Destinos
        destinos_demo = [
            (
                "Londres", "Capital del Reino Unido", "Conocer el palacio de Buckingham, el Big Ben, entre otros.",
                800000
            ),
            (
                "Paris", "Capital de Francia", "Conocer la torre Eiffel, el museo de Louvre, entre otros.",
                830000
            ),
            (
                "Barcelona", "Capital de Cataluña", "Conocer la Sagrada Familia, la cultura catalana, entre otros.",
                700000
            ),
            (
                "Berlin", "Capital de Alemania", "Conocer el muro de Berlín, la Puerta de Brandeburgo, entre otros.",
                900000
            ),
            (
                "Lisboa", "Capital de Portugal", "Conocer la torre de Belén, el Monasterio de los Jerónimos, entre otros.",
                850000
            )
        ]

        sql = """
        INSERT INTO destinos (
            nombre, descripcion, actividades, costo_base
        ) 
        VALUES (%s, %s, %s, %s)
        """

        try:
            cursor.executemany(sql, destinos_demo)
            conn.commit()
            print("Destinos iniciales creados.")
        except Exception as e:
            print(f"Error creando destinos iniciales: {e}")

    cursor.close()
    conn.close()

if __name__ == "__main__":
    # Si ejecutamos este archivo directo, hace todo el proceso
    crear_bd()
    crear_tablas()
    crear_admin_por_defecto()
    print("--- Base de datos inicializada completa ---")