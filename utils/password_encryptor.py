import bcrypt

class PasswordEncryptor:
    
    @staticmethod
    def hash_password(password_plana):
        print(f"Encriptando '{password_plana}'")
        bytes_pass = password_plana.encode('utf-8')
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(bytes_pass, salt)
        return hashed.decode('utf-8')

    @staticmethod
    def verify_password(password_plana, password_hashed):
        print(f"Verificando contraseña")
        bytes_pass = password_plana.encode('utf-8')
        bytes_hash = password_hashed.encode('utf-8')
        
        return bcrypt.checkpw(bytes_pass, bytes_hash)