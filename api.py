import pymysql
from flask import jsonify
from flask import Flask, flash, request, make_response
from flaskext.mysql import MySQL
		
app = Flask(__name__)

mysql = MySQL()
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = '123'
app.config['MYSQL_DATABASE_DB'] = 'databaseparalela'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)

@app.route('/api/countries/all', methods=['GET'])
def all():
	try:
		conn = mysql.connect()
		cursor = conn.cursor(pymysql.cursors.DictCursor)
		cursor.execute("SELECT alpha3 as abbr, alpha2 as code, codigo_pais_moneda as currencyCode, moneda as currencyName, lengua as lang, nombre as name FROM info")
		empRows = cursor.fetchall()
		respone = jsonify(empRows)
		respone.status_code = 200
		return respone
	except Exception as e:
		print(e)
	finally:
		cursor.close() 
		conn.close()

@app.route('/api/countries/<code>/info', methods=['GET'])
def code(code):
	try:
		conn = mysql.connect()
		cursor = conn.cursor(pymysql.cursors.DictCursor)
		cursor.execute("SELECT alpha3 as abbr, alpha2 as code, codigo_pais_moneda as currencyCode, moneda as currencyName, lengua as lang, nombre as name FROM info WHERE alpha2 =%s", code)
		empRow = cursor.fetchone()
		respone = jsonify(empRow)
		respone.status_code = 200
		return respone
	except Exception as e:
		print(e)
	finally:
		cursor.close() 
		conn.close()


@app.route('/api/indicators/<countryCode>/<indicatorCode>/<year>/info', methods=['GET'])
def indicador(countryCode,indicatorCode,year):
    try:
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT alpha3 as abbr, alpha2 as code, codigo_pais_moneda as currencyCode, moneda as currencyName, lengua as lang, nombre as name FROM info WHERE alpha2 =%s", countryCode)
        empRow = cursor.fetchone()
        if (indicatorCode == 'PIB'):
            cursor.execute("SELECT indicador_pib as value, anno as year FROM pib where anno =%s", year)
            cosa = cursor.fetchone()
            L = {
                "code" : "PIB",
                "name" : "Producto Intero Bruto",
                "unit" : "$US",
                "country" : empRow,
            }
            L.update(cosa)
        if (indicatorCode == 'TDA'):
            cursor.execute("SELECT indicador_tda as value, anno as year FROM tda where anno =%s", year)
            cosa = cursor.fetchone()
            L = {
                "code" : "TDA",
                "name" : "Tasa de desempleo anual",
                "unit" : "%",
                "country" : empRow,
            }
            L.update(cosa)
        if (indicatorCode == 'IFL'):
            cursor.execute("SELECT indicador_ifl as value, anno as year FROM ifl where anno =%s", year)
            cosa = cursor.fetchone()
            L = {
                "code" : "IFL",
                "name" : "Inflación",
                "unit" : "%",
                "country" : empRow,
            }
            L.update(cosa)
        if (indicatorCode == 'IVA'):
            cursor.execute("SELECT indicador_iva as value, anno as year FROM iva where anno =%s", year)
            cosa = cursor.fetchone()
            L = {
                "code" : "IVA",
                "name" : "Impuesto de Valor Añadido",
                "unit" : "%",
                "country" : empRow,
            }
            L.update(cosa)
        if (indicatorCode == 'PRF'):
            cursor.execute("SELECT indicador_prf as value, anno as year FROM prf where anno =%s", year)
            cosa = cursor.fetchone()
            L = {
                "code" : "PRF",
                "name" : "Presión Fiscal",
                "unit" : "%",
                "country" : empRow,
            }
            L.update(cosa)
        if (indicatorCode == 'TSC'):
            cursor.execute("SELECT indicador_tsc as value, anno as year FROM tsc where anno =%s", year)
            cosa = cursor.fetchone()
            L = {
                "code" : "TSC",
                "name" : "Tasa de cambio",
                "unit" : "US$",
                "country" : empRow,
            }
            L.update(cosa)
        if (indicatorCode == 'DBI'):
            cursor.execute("SELECT indicador_dbi as value, anno as year FROM dbi where anno =%s", year)
            cosa = cursor.fetchone()
            L = {
                "code" : "DBI",
                "name" : "Doing Business Index",
                "unit" : "Posición en el ranking (menor es mejor)",
                "country" : empRow,
            }
            L.update(cosa)
        return jsonify(L)
    except Exception as e:
        print(e)
    finally:
        cursor.close() 
        conn.close()

@app.route('/api/indicators/info', methods=['POST'])
def indicators_info():
    try:
        datos = {
        "indicatorCode" : request.json['indicatorCode'],
        "endYear" : request.json['endYear'],
        "countryCode" : request.json['countryCode'],
        "startYear" : request.json['startYear'],
        }
        conn = mysql.connect()
        query = "INSERT INTO indicators(indicatorCode, endYear, countryCode, startYear) VALUES(%s, %s, %s, %s)"
        datos = (datos['indicatorCode'], datos['endYear'], datos['countryCode'], datos['startYear'])
        cursor = conn.cursor()
        cursor.execute(query, datos)
        conn.commit()
        respone = jsonify('Employee added successfully!')
        respone.status_code = 200
        return respone
    except Exception as e:
            print(e)
    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    app.run()