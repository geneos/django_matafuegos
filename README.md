# django_matafuegos
 Sistema de Matafuegos en DJANGO para Seguridad Fenix

#### Pasos para la instalacion

Crear un archivo '.env' en la carpeta 'django_matafuegos/matafuegos_fenix/matafuegos_fenix'.

Copiar el contenido del archivo '.env_template' en el nuevo '.env' y completar los datos. La secret_key la generamos a continuacion.

Obtener la 'secret_key' con el comando: python -c 'from django.core.management.utils import get_random_secret_key; \
            print(get_random_secret_key())'

Copiar el resultado del comando y pegarlo en el archivo '.env'.

Instalar los requerimientos con el comando: pip install -r requirementes.txt 

Correr el comando migrate: python manage.py migrate
