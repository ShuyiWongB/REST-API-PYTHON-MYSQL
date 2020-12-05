import pymysql
import datetime
from flask import jsonify
from flask import Flask, flash, request, make_response, abort
from flaskext.mysql import MySQL
from flask_httpauth import HTTPBasicAuth
from werkzeug.exceptions import HTTPException
from werkzeug.security import generate_password_hash, check_password_hash
		
app = Flask(__name__) #Instancia flask

#Configuracion de la base de datos para su lectura
mysql = MySQL()
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = '123'
app.config['MYSQL_DATABASE_DB'] = 'rest'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)

#Definicion de las variables date para los errores y auth para la identificacion
date = datetime.datetime.now()
auth = HTTPBasicAuth()

#Usuarios y sus contraseñas
users = {
    'usuario1': generate_password_hash("123"),
    'usuario2': generate_password_hash("456"),
    'usuario3': generate_password_hash("789"),
}

#Autentificador
@auth.verify_password
def verify_password(username, password):
    if username in users and check_password_hash(users.get(username), password):
        return username
    else:
        abort(401)

#Definicion de los diferentes errores
@app.errorhandler(400)
def bad_request(error=None):
    message = {
        'ok': False,
        'date' : date,
        'message': 'Petición invalida'
    }
    resp = jsonify(message)
    resp.status_code = 400
    return resp

@app.errorhandler(404)
def not_found(error=None):
    message = {
        'ok': False,
        'date' : date,
        'message': 'No encontrado'
    }
    resp = jsonify(message)
    resp.status_code = 404
    return resp

@app.errorhandler(401)
def not_authorized(error=None):
    message = {
        'ok': False,
        'date' : date,
        'message': 'No tiene autorización'
    }
    resp = jsonify(message)
    resp.status_code = 401
    return resp

@app.errorhandler(403)
def not_method(error=None):
    message = {
        'ok': False,
        'date' : date,
        'message': 'Las credenciales no permiten consumir este servicio'
    }
    resp = jsonify(message)
    resp.status_code = 403
    return resp

@app.errorhandler(500)
def server_error(error=None):
    message = {
        'ok': False,
        'date' : date,
        'message': 'Error interno del servidor'
    }
    resp = jsonify(message)
    resp.status_code = 500
    return resp

@app.errorhandler(405)
def method_error(error=None):
    message = {
        'ok': False,
        'date' : date,
        'message': 'Metodo Incorrecto'
    }
    resp = jsonify(message)
    resp.status_code = 405
    return resp

#Ruta que entrega la informacion de todos los paises
@app.route('/api/countries/all', methods=['GET'])
@auth.login_required
def all():
        try:
            conn = mysql.connect()
            cursor = conn.cursor(pymysql.cursors.DictCursor)
            cursor.execute("SELECT alpha3 as abbr, alpha2 as code, codigo_pais_moneda as currencyCode, moneda as currencyName, lengua as lang, nombre as name FROM info") #Query de la busqueda de los datos en la base de datos
            country = cursor.fetchall()
            respone = jsonify(country)
            respone.status_code = 200
            return respone
        except Exception as e:
            print(e)
        finally:
            cursor.close() 
            conn.close()

#Ruta que encuentra la informacion de un pais en especifico
@app.route('/api/countries/<code>/info', methods=['GET'])
@auth.login_required
def code(code):
    try:
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT alpha3 as abbr, alpha2 as code, codigo_pais_moneda as currencyCode, moneda as currencyName, lengua as lang, nombre as name FROM info WHERE alpha2 =%s", code)
        country = cursor.fetchone()
        if not country:
            return not_found()
        else:
            respone = jsonify(country)
            respone.status_code = 200
            return respone
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()

#ruta que encuentra los datos de un indicador en un pais en un año especifico
@app.route('/api/indicators/<countryCode>/<indicatorCode>/<year>/info', methods=['GET'])
@auth.login_required
def indicador(countryCode,indicatorCode,year):
    try:
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT alpha3 as abbr, alpha2 as code, codigo_pais_moneda as currencyCode, moneda as currencyName, lengua as lang, nombre as name FROM info WHERE alpha2 =%s", countryCode)
        country = cursor.fetchone()
        if not country:
            return not_found()
        else:
            if (indicatorCode == 'PIB'):
                cursor.execute("SELECT indicador_pib as value, anno as year FROM pib where anno =%s", year) #Se buscan los valores de cada indicador a su año correspondiente
                cosa = cursor.fetchone()
                if not cosa:
                    return not_found()
                else:
                    L = {
                        "code" : "PIB",
                        "name" : "Producto Interno Bruto",
                        "unit" : "$US",
                        "country" : country,
                    }
                    L.update(cosa)
            elif (indicatorCode == 'TDA'):
                cursor.execute("SELECT indicador_tda as value, anno as year FROM tda where anno =%s", year)
                cosa = cursor.fetchone()
                if not cosa:
                    return not_found()
                else:
                    L = {
                        "code" : "TDA",
                        "name" : "Tasa de desempleo anual",
                        "unit" : "%",
                        "country" : country,
                    }
                    L.update(cosa)
            elif (indicatorCode == 'IFL'):
                cursor.execute("SELECT indicador_ifl as value, anno as year FROM ifl where anno =%s", year)
                cosa = cursor.fetchone()
                if not cosa:
                    return not_found()
                else:
                    L = {
                        "code" : "IFL",
                        "name" : "Inflación",
                        "unit" : "%",
                        "country" : country,
                    }
                    L.update(cosa)
            elif (indicatorCode == 'IVA'):
                cursor.execute("SELECT indicador_iva as value, anno as year FROM iva where anno =%s", year)
                cosa = cursor.fetchone()
                if not cosa:
                    return not_found()
                else:
                    L = {
                        "code" : "IVA",
                        "name" : "Impuesto de Valor Añadido",
                        "unit" : "%",
                        "country" : country,
                    }
                    L.update(cosa)
            elif (indicatorCode == 'PRF'):
                cursor.execute("SELECT indicador_prf as value, anno as year FROM prf where anno =%s", year)
                cosa = cursor.fetchone()
                if not cosa:
                    return not_found()
                else:
                    L = {
                        "code" : "PRF",
                        "name" : "Presión Fiscal",
                        "unit" : "%",
                        "country" : country,
                    }
                    L.update(cosa)
            elif (indicatorCode == 'TSC'):
                cursor.execute("SELECT indicador_tsc as value, anno as year FROM tsc where anno =%s", year)
                cosa = cursor.fetchone()
                if not cosa:
                    return not_found()
                else:
                    L = {
                        "code" : "TSC",
                        "name" : "Tasa de cambio",
                        "unit" : "US$",
                        "country" : country,
                    }
                    L.update(cosa)
            elif (indicatorCode == 'DBI'):
                cursor.execute("SELECT indicador_dbi as value, anno as year FROM dbi where anno =%s", year)
                cosa = cursor.fetchone()
                if not cosa:
                    return not_found()
                else:
                    L = {
                        "code" : "DBI",
                        "name" : "Doing Business Index",
                        "unit" : "Posición en el ranking (menor es mejor)",
                        "country" : country,
                    }
                    L.update(cosa)
            elif (indicatorCode == 'SMI'):
                cursor.execute("SELECT indicador_smi as value, anno as year FROM smi where anno =%s", year)
                cosa = cursor.fetchone()
                if not cosa:
                    return not_found()
                else:
                    L = {
                        "code" : "SMI",
                        "name" : "Salario Minimo",
                        "unit" : "US$",
                        "country" : country,
                    }
                    L.update(cosa)
            else:
                return not_found()
            respone = jsonify(L)
            respone.status_code = 200
            return respone
    except Exception as e:
        print(e)
    finally:
        cursor.close() 
        conn.close()

#Ruta que se ingresan datos y entrega la informacion referente
@app.route('/api/indicators/info', methods=['POST'])
@auth.login_required
def indicators_info():
    try: #Ingresa los datos
        indicatorCode = request.json['indicatorCode']
        endYear = request.json['endYear']
        countryCode = request.json['countryCode']
        startYear = request.json['startYear']
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT alpha3 as abbr, alpha2 as code, codigo_pais_moneda as currencyCode, moneda as currencyName, lengua as lang, nombre as name FROM info WHERE alpha2 =%s", countryCode)
        country = cursor.fetchone()
        if not country:
            return not_found() #Si el pais esta mal, lo rechaza
        else:
            annos = [] #Lista para guardar todos los datos
            if (startYear > endYear):
                return not_found() #Si los años estan al contrario, lo rechaza
            else:
                while (startYear != endYear+1 and startYear <= endYear):
                    if (indicatorCode == 'PIB'):
                        cursor.execute("SELECT indicador_pib as value, anno as year FROM pib where anno =%s", startYear)
                        cosa = cursor.fetchone()
                        if not cosa:
                            return not_found() #Si no encuentra el año, lo rechaza
                        else:
                            L = {
                                'code' : "PIB",
                                'name' : "Producto Interno Bruto",
                                'unit' : "$US",
                                'country' : country
                            }
                            L.update(cosa)
                    elif (indicatorCode == 'TDA'):
                        cursor.execute("SELECT indicador_tda as value, anno as year FROM tda where anno =%s", startYear)
                        cosa = cursor.fetchone()
                        if not cosa:
                            return not_found()
                        else:                    
                            L = {
                                "code" : "TDA",
                                "name" : "Tasa de desempleo anual",
                                "unit" : "%",
                                "country" : country,
                            }
                            L.update(cosa)
                    elif (indicatorCode == 'IFL'):
                        cursor.execute("SELECT indicador_ifl as value, anno as year FROM ifl where anno =%s", startYear)
                        cosa = cursor.fetchone()
                        if not cosa:
                            return not_found()
                        else:
                            L = {
                                "code" : "IFL",
                                "name" : "Inflación",
                                "unit" : "%",
                                "country" : country,
                            }
                    elif (indicatorCode == 'IVA'):
                        cursor.execute("SELECT indicador_iva as value, anno as year FROM iva where anno =%s", startYear)
                        cosa = cursor.fetchone()
                        if not cosa:
                            return not_found()
                        else:
                            L = {
                                "code" : "IVA",
                                "name" : "Impuesto de Valor Añadido",
                                "unit" : "%",
                                "country" : country,
                            }
                            L.update(cosa)
                    elif (indicatorCode == 'PRF'):
                        cursor.execute("SELECT indicador_prf as value, anno as year FROM prf where anno =%s", startYear)
                        cosa = cursor.fetchone()
                        if not cosa:
                            return not_found()
                        else:
                            L = {
                                "code" : "PRF",
                                "name" : "Presión Fiscal",
                                "unit" : "%",
                                "country" : country,
                            }
                            L.update(cosa)
                    elif (indicatorCode == 'TSC'):
                        cursor.execute("SELECT indicador_tsc as value, anno as year FROM tsc where anno =%s", startYear)
                        cosa = cursor.fetchone()
                        if not cosa:
                            return not_found()
                        else:
                            L = {
                                "code" : "TSC",
                                "name" : "Tasa de cambio",
                                "unit" : "US$",
                                "country" : country,
                            }
                            L.update(cosa)
                    elif (indicatorCode == 'DBI'):
                        cursor.execute("SELECT indicador_dbi as value, anno as year FROM dbi where anno =%s", startYear)
                        cosa = cursor.fetchone()
                        if not cosa:
                            return not_found()
                        else:
                            L = {
                                "code" : "DBI",
                                "name" : "Doing Business Index",
                                "unit" : "Posición en el ranking (menor es mejor)",
                                "country" : country,
                            }
                            L.update(cosa)
                    elif (indicatorCode == 'SMI'):
                        cursor.execute("SELECT indicador_smi as value, anno as year FROM smi where anno =%s", startYear)
                        cosa = cursor.fetchone()
                        if not cosa:
                            return not_found()
                        else:
                            L = {
                                "code" : "SMI",
                                "name" : "Salario Minimo",
                                "unit" : "US$",
                                "country" : country,
                            }
                    else:
                        return not_found()
                    startYear = startYear+1
                    annos.append(L)
                respone = jsonify(annos) #Convierte la lista en un json para su entrega
                respone.status_code = 200
                return respone
    except Exception as e:
            print(e)
    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    app.run(host='127.0.0.1', port=8080, debug=True) #IP y puerto definido
