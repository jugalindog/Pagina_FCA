# create_hash.py
from werkzeug.security import generate_password_hash
import getpass

# Este script te ayuda a generar hashes de contraseñas de forma segura.
# Ejecútalo en tu terminal con: python create_hash.py

try:
    password = getpass.getpass("Ingresa la contraseña para generar su hash: ")
    password_confirm = getpass.getpass("Confirma la contraseña: ")

    if password != password_confirm:
        print("\n❌ Las contraseñas no coinciden. Inténtalo de nuevo.")
    elif not password:
        print("\n❌ La contraseña no puede estar vacía.")
    else:
        # Generamos el hash con un método seguro
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
        print("\n✅ Hash generado con éxito. Cópialo y pégalo en tu diccionario de usuarios:")
        print(f"   '{hashed_password}'")

except KeyboardInterrupt:
    print("\nOperación cancelada.")

