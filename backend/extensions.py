from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()

print(bcrypt.generate_password_hash("teste").decode('utf-8'))