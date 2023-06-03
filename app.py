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
    query = request.args.get("customquery", "select * from vacancies", type=str)
    minWeight = request.args.get("min", 0, type=float)
    cur.execute(query)
    job = cur.fetchall()
    allJob = []
    for data in job:
        temp = []
        temp.append( data[0])
        temp.append( data[2])
        temp.append( data[3])
        allJob.append(temp)
    jobWeight = ai.search(allJob,keyword)
    sortedJob = jobWeight[0].argsort()[::-1]
    # eliminate minimum weight
    x =0
    for val in sortedJob:
        print(jobWeight[0][x])
        if(jobWeight[0][val] < minWeight):
            print("ini x")
            print(jobWeight[0][val])
            print(x)
            sortedJob = sortedJob[0:x]
            break
        x = x+1
    print(sortedJob)
    itemPerPage = 5
    pages = math.ceil(len(sortedJob)/itemPerPage)
    page = request.args.get("page", 0, type=int)
    data = []
    for x in sortedJob[0 if page == 0 else (page-1)*itemPerPage:len(sortedJob) if page == 0 else len(sortedJob) if page >= pages else page*itemPerPage]:
        temp = {}
        temp["id"] = allJob[x][0]
        temp["score"] = jobWeight[0][x]
        data.append(temp)

    res = {"pages":pages,"data":data}
    return jsonify(res)
@app.route('/recomendation')
def bar():
    return 'bar!'