# DeveloperBlog.com

Proyecto de un blog

## Requerimientos
* Python 3.5 o superior
* django 2.2.9 LTS
* psycopg2 2.8.4 o superior

## Installation

* Clonar el repositorio

```bash
git clone -b develop https://github.com/Reyloso/Blog.git
```

* Crear el entorno virtual

```bash
pip install virtualenv MiEntorno
```

* Iniciar el entorno virtual

```bash
#para windows
cd /miEntorno/scripts
activate

#para linux
cd /miEntorno/bin
source activate
```
* Instalar requerimientos desde el archivo requieriments.txt ubicado en la carpeta principal del proyecto 
 
```bash

pip install -r requirements.txt
```

* Configuración de la base de datos
 
```python
# crear un achivo .env 
# colocarlo en la carpeta blog donde se encuentra el settings.py
# pegar y configurar las siguientes lineas de codigo
# reemplazando las variables por las que haya definido en su base de datos
# para este ejemplo el archivo .env esta incluido en el repositorio
# por los tanto no es necesario crearlo, solo configurarlo

# como nota a tener en cuenta es que en el orm implementado en el proyecto se usan funciones
# que solo funcionan para postgres, por lo tanto la base de datos a configurar debe ser postgres

DEBUG=True
SECRET_KEY=Tukey
ALLOWED_HOSTS = ['*']
DB_NAME=tu_db_name
DB_USER=tu_db_user
DB_PASSWORD=tu_db_password
DB_HOST=tu_host
DB_PORT=tu_port

```
* Crear migraciones
 
```bash

python manage.py makemigrations posts users

```


Aplicar migraciones al base de datos
 
```bash

python manage.py migrate

```

Crear super usuario
 
```bash

python manage.py createsuperuser
```
Ejecutar script que crea grupos con permisos y crea un usuario administrador
 
```bash

# este script además crea algunas categorías de ejemplo,
# en el menú categorías en las opciones del usuario se pueden crear categorías
# las categorias solo pueden ser creadas por un usuario administrador

python manage.py runscript config

usuario administrador: administrador
password administradir : qwerty123
```

Ejecutar el proyecto

```bash

python manage.py runserver 
#tambien
#el puerto es opcional y se corre en la ip cero para poder acceder de una 
# ip externa
Python manage.py runserver 0:80

```