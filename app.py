from flask import Flask, request
from flask_mysqldb import MySQL
import MySQLdb.cursors
from model.ai import ai
from flask import jsonify
import math


app = Flask(__name__)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'bkk'

mysql = MySQL(app)

@app.route('/search/<keyword>')
def foo(keyword):
    cur = mysql.connection.cursor()
    # tambahin parameter
    cur.execute("select * from vacancies")
    job = cur.fetchall()
    allJob = []
    for data in job:
        temp = []
        temp.append( data[0])
        temp.append( data[2])
        temp.append( data[3])
        allJob.append(temp)
    sortedJob = ai.search(allJob,keyword)
    itemPerPage = 5
    pages = math.ceil(len(sortedJob)/itemPerPage)
    page = request.args.get("page", 0, type=int)
    print((page-1)*itemPerPage)
    print(pages)
    data = []
    for x in sortedJob[0 if page == 0 else (page-1)*itemPerPage:-1 if page == 0 else -1 if page >= pages else page*itemPerPage]:
        data.append(allJob[x][0])
        print(x)

    res = {"pages":pages,"data":data}
    return jsonify(res)
@app.route('/recomendation')
def bar():
    return 'bar!'