# Resumen

Se realizaron varios cambios a la estructura de las carpetas. Se coloco todo el codigo
python dentro de una carpeta src (source). 

Se dividio src en tests, utils y archivos del servidor.

Se creo archivos para los modelos, serializers, vistas, y sus respectivos tests.

A la lista de requerimientos se agrego flake8 para el linting y asegurarme de que se respete el PEP8.

# Tests

Solo se agregaron tests para los modelos y los serializers debido a que tests 
para las vistas requeria desarrollar un programa que simule los requests de bottle.

# Correr

Para correr el programa se puede hacer uso del siguiente comando:

$ python -m src.server

# 1. Funcionalidad basica

Se logro crear un sistema que liste y cree notas. Para ello se crearon clases utiles
de vistas, serializers y routing inspiradas en Django.
Tiene atributos, nombres de metodos y nombres de clase como los de Django, pero su funcionalidad puede variar
un poco por motivo de tiempo pero la apariencia del codigo resultara bastante familiar.

Los urls de las funcionalidades se pueden encontrar en src/urls.py.
Los urls de la funcionalidad basica son:

notes/create/
notes/list/

# 2. Funcionalidades adicionales

## 2.1. Serializacion y validacion

Para esto se crearon las clases src/utils/serializers.py.

La funcionalidad del serializer se asemeja bastante al ModelSerializer de Django.

Permite setear una subclase Meta, fields, modelo y kwargs extra para cada field.
A pesar que se llama ModelSerializer por estar inspirado en la version homonima de Django, 
este puede ser ejecutado sin un modelo, como es demostrado por el TokenSerializer.
El Token no es un modelo ni se guarda en la base de datos.

## 2.2. Usuario y autenticacion
## 2.3. JWT

Urls de usuario:

users/token/
users/create/

Esta funcion chequea el password de usuario haciendo uso de su funcion de clase y
le otorga al usuario un JWT.

Como bottle solo usa wrappers para controlar la autenticacion, decidi hacer 
la autenticacion como parte de una lista de permisos en las vistas, al igual que Django,
solo que se trata de una funcion simple (has_permission) en vez de un motor
de autenticacion.

## 2.4. Autorizacion

Se extendio el mismo sistema de permisos para revisar los permisos generales de la vista
y los permisos por objeto para saber si un usuario tiene permiso de obtener o modificar un 
objeto o lista de objetos.


## 2.5. Cliente del API

Para esto hice un cliente en ReactJS.  
Tenia planeado usar la libreria bottle-react para correr el componente principal
pero solo funcionaba con una version antigua de react y descarte el proceso por completo.

El link del repositorio del cliente es este:

https://github.com/WalterCM/technical-test-backend-react

Se corre con 

$ npm start


# Enunciado Original

# Creación de un API REST

La prueba consistirá en crear un simple API REST para un único recurso, la prueba se dividirá en una funcionalidad básica y en funcionalidades adicionales que sumarán puntos a la evaluación. 

Este repositorio contiene los archivos base, los cambios realizados deben subirse en un repositorio propio, el link de ese repositorio debe enviarse por email.

## 1. Funcionalidad básica
Se desea un endpoint para poder administrar **notas** (crear y listar), los datos se guardará en una base de datos **sqlite**. Para ello se utilizarán los siguientes paquetes de Python.
* [peewee](http://docs.peewee-orm.com/en/latest/ "peewee") (ORM)
* [bottle](https://bottlepy.org/docs/dev/ "bottle") (miniframework web)

Los campos que tendrá el modelo no son relevantes.

## 2. Funcionalidades adicionales
Las siguientes funcionalidades se construirán sobre la funcionalidad base.

**Serialización y validación**

Se desea validar los datos que se reciben via POST y mostrar los errores al usuario que usa el API, serializar la lista de objetos para enviarlas como json. Para ello se utilizará la librería [marshmallow](https://marshmallow.readthedocs.io/en/latest/ "marshmallow").

**Usuario y Autentificación**

Se desea que el API sea restringido mediante algún método de autenficación.

**JWT**

Se desea que el usuario se autentifique mediante json web tokens, para ello se utializará la librería [pyjwt](https://github.com/jpadilla/pyjwt "pyjwt")

**Autorización**

Se desea asociar una **nota** con un **usuario**, de tal manera que cada usuario solo pueda ver sus propias notas.

**Cliente del API**

Se desea tener un cliente web que haga uso del API desde frontend (html y javascript). Ver siguiente sección.

# Estructura de archivos
El repositorio contiene archivos que sirven como guia, pero se deja la libertad de hacer los cambios que se consideren necesarios.
* **.gitignore** - Archivos ignorados por git, añadir la base de datos sqlite que se genere.
* **requirements.txt** - Los paquetes python que se utilizarán para la prueba. Se recomienda usar un entorno virtual (ejem. [virtualenv](https://virtualenv.pypa.io/en/stable/ "virtualenv")) para instalarlos.
* **server.py** - Contendrá tóda la lógica del api, este correrá en el puerto 8000.
* **client.py** - Un pequeño servidor que corre en el puerto 5000 y sirve el archivo index.html, aquí no se necesita hacer ninguna modificación.
* **index.html** - Donde idealmente deberá estar toda la lógica para loguearse y mostrar los datos del api.

# Objetivos de la prueba
* Evaluar el conocimiento general del lenguaje Python.
* Evaluar el conocimiento en arquitecturas web (MVC, REST).
* Comprobar el conocimiento independientemente de la herramienta / framework.
* Evaluar buenas prácticas en el código relacionadas con Python (pep8).
* Evaluar conocimientos basicos de frontend.
* Evaluar el modelo mental que se tiene para la organización de classes, funciones, módulos.
