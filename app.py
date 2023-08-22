import math
import pandas as pd
from model.ai import ai
from flask_mysqldb import MySQL
from flask import Flask, request, jsonify

app = Flask(__name__)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'bkk'

mysql = MySQL(app)


@app.route('/search/<keyword>')
def recommendationBySearch(keyword):
    # obtain data from database
    query = request.args.get("customquery")
    # tambahin parameter
    # query = request.args.get(
    #     "customquery", "select preprocessed_text from vacancies where preprocessed_text_id is not null", type=str)

    cur = mysql.connection.cursor()
    cur.execute(query)
    vacancies = []
    for vacancy in cur.fetchall():
        # vacancy[0] is id
        # vacancy[2] is position
        # vacancy[4] is description
        vacancies.append([vacancy[0], vacancy[5]])

    dframeKeyword = pd.DataFrame([keyword], columns=["text"])
    dframeVacancies = pd.DataFrame(vacancies, columns=["id", "text"])
    dframeVacancies = dframeVacancies.dropna()

    vacanciesWeighted = ai.search(dframeVacancies, dframeKeyword)
    sortedIndexVacancies = vacanciesWeighted.argsort()[::-1]

    # eliminate minimum weight
    minWeight = request.args.get("min", 0, type=float)
    for index, vacancyScore in enumerate(vacanciesWeighted[sortedIndexVacancies]):
        if(vacancyScore < minWeight):
            # delete element from index 0 to index (but not including this index less than minWeight)
            sortedIndexVacancies = sortedIndexVacancies[0:index]
            break

    data = []
    itemPerPage = 5
    page = request.args.get("page", 0, type=int)
    pages = math.ceil(len(sortedIndexVacancies) / itemPerPage)
    if page == 1 or page == 0:
        start_index = 0
        end_index = itemPerPage
    else:
        start_index = (page - 1) * itemPerPage
        if page >= pages:
            end_index = len(sortedIndexVacancies)
        else:
            end_index = page * itemPerPage

    for index in sortedIndexVacancies[start_index:end_index]:
        data.append({
            "id": vacancies[index][0],
            "score": vacanciesWeighted[index]
        })

    return jsonify({
        "pages": pages,
        "data": data
    })


@app.route('/preprocessing', methods=['POST', 'GET'])
def preprocessingRun():
    # query = "select id, position, description, preprocessed_text_id from vacancies where preprocessed_text_id is null and deleted_at is null"
    vacancyId = request.get_json()['vacancy']
    query = "SELECT id, position, description FROM vacancies WHERE deleted_at is null AND id = '" + \
        str(vacancyId) + "'"
    cur = mysql.connection.cursor()
    cur.execute(query)
    vacancies = []
    for vacancy in cur.fetchall():
        # vacancy[0] is id
        # vacancy[1] is position
        # vacancy[2] is description
        text = vacancy[1] + ' ' + vacancy[2]
        vacancies.append([vacancy[0], text])

    df = pd.DataFrame(vacancies, columns=["id", "text"])
    df = df.dropna()

    preprocessed = ai.preprocessing(df)

    for i, kalimat in enumerate(preprocessed.iterrows()):
        updateQuery = "UPDATE vacancies SET preprocessed_text_id = '" + \
            str(preprocessed.loc[i, 'text']) + "' WHERE id = '" + \
            str(preprocessed.loc[i, 'id']) + "'"
        cur.execute(updateQuery)
        mysql.connection.commit()

    # preprocessedEng = ai.preprocessingEng(preprocessed)

    # for i, kalimat in enumerate(preprocessed.iterrows()):
    #     updateQuery = "UPDATE vacancies SET preprocessed_text_id_eng = '" + \
    #         str(preprocessedEng.loc[i, 'text']) + "' WHERE id = '" + \
    #         str(preprocessedEng.loc[i, 'id']) + "'"
    #     cur.execute(updateQuery)
    #     mysql.connection.commit()

    return jsonify({
        "status": True
    })
