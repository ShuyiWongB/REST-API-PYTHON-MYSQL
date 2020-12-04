# API REST
Trabajo de Computación Paralela, 2do Semestre 2020

### Lenguaje y Librerias necesarias

#### Lenguaje

* Python 3.8

_Descargar python desde la pagina oficial o desde su terminal y revisar la version_

```
python --version
```

#### Librerias

* Flask

```
pip install flask
```

* Flask_HTTPAuth

```
pip install flask-httpauth
```

* PyMySQL

```
pip install PyMySQL
```

* Flask-MySQL (extension de Flask para acceder a una base de datos MYSQL)

```
pip install flask-mysql
```

#### Base de datos, MySQL

```
pip install mysql-server
```


### Rutas y Metodos

_Ruta que obtiene todos los datos de los paises del sistema_
```
/api/countries/all
METODO GET
```

_Ruta para obtener la información de un pais especifico_
```
 /api/countries/<code>/info
METODO GET
```

_Ruta para obtener la información de un indicador_
```
 /api/indicators/<countryCode>/<indicatorCode>/<year>/info
METODO GET
```

_Ruta para obtener la información de un indicador en una cierta cantidad de años_
```
 /api/indicators/info
METODO POST - Request Body formato JSON
{"indicatorCode" : "", "endYear" : "", "countryYear" : "", "starYear" : ""}
```

### Como conectar la base de datos a la API con la configuración especifica
1. Entrar al entorno mysql en la terminal con el usuario: Root y contraseña: 123
```
mysql -u root -p
```
2. Crear una base de datos llamada "rest" y luego de creada salir con "exit"
```
CREATE DATABASE rest;
```
3. Agregar la base de datos .sql adjunta a la base de datos en el mysql
```
mysql -u root -p rest < database rest.sql
```
