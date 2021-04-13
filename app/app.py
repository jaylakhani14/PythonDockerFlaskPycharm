from typing import List, Dict
import simplejson as json
from flask import Flask, request, Response, redirect
from flask import render_template
from flaskext.mysql import MySQL
from pymysql.cursors import DictCursor

app = Flask(__name__)
mysql = MySQL(cursorclass=DictCursor)

app.config['MYSQL_DATABASE_HOST'] = 'db'
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'root'
app.config['MYSQL_DATABASE_PORT'] = 3306
app.config['MYSQL_DATABASE_DB'] = 'peopleData'
mysql.init_app(app)


@app.route('/', methods=['GET'])
def index():
    user = {'username': 'People Project'}
    cursor = mysql.get_db().cursor()
    cursor.execute('SELECT * FROM tblPeopleImport')
    result = cursor.fetchall()
    return render_template('index.html', title='Home', user=user, People=result)


@app.route('/view/<int:people_id>', methods=['GET'])
def record_view(people_id):
    cursor = mysql.get_db().cursor()
    cursor.execute('SELECT * FROM tblPeopleImport WHERE id=%s', people_id)
    result = cursor.fetchall()
    return render_template('view.html', title='View Form', People=result[0])


@app.route('/edit/<int:people_id>', methods=['GET'])
def form_edit_get(people_id):
    cursor = mysql.get_db().cursor()
    cursor.execute('SELECT * FROM tblPeopleImport WHERE id=%s', people_id)
    result = cursor.fetchall()
    return render_template('edit.html', title='Edit Form', People=result[0])


@app.route('/edit/<int:people_id>', methods=['POST'])
def form_update_post(people_id):
    cursor = mysql.get_db().cursor()
    inputData = (request.form.get('fldName'), request.form.get('fldSex'), request.form.get('fldAge'),
                 request.form.get('fldHeight'), request.form.get('fldWeight'), people_id)
    sql_update_query = """UPDATE tblPeopleImport t SET t.fldName = %s, t.fldSex = %s, t.fldAge = %s, t.fldHeight = 
    %s, t.fldWeight = %s, WHERE t.id = %s """
    cursor.execute(sql_update_query, inputData)
    mysql.get_db().commit()
    return redirect("/", code=302)

@app.route('/people/new', methods=['GET'])
def form_insert_get():
    return render_template('new.html', title='New People')


@app.route('/people/new', methods=['POST'])
def form_insert_post():
    cursor = mysql.get_db().cursor()
    inputData = (request.form.get('fldName'), request.form.get('fldSex'), request.form.get('fldAge'),
                 request.form.get('fldHeight'), request.form.get('fldWeight'))
    sql_insert_query = """INSERT INTO tblPeopleImport (fldName,fldSex,fldAge,fldHeight,fldWeight) VALUES (%s, %s,%s, %s,%s) """
    cursor.execute(sql_insert_query, inputData)
    mysql.get_db().commit()
    return redirect("/", code=302)

@app.route('/delete/<int:people_id>', methods=['POST'])
def form_delete_post(people_id):
    cursor = mysql.get_db().cursor()
    sql_delete_query = """DELETE FROM tblPeopleImport WHERE id = %s """
    cursor.execute(sql_delete_query, people_id)
    mysql.get_db().commit()
    return redirect("/", code=302)


@app.route('/api/v1/people', methods=['GET'])
def api_browse() -> str:
    cursor = mysql.get_db().cursor()
    cursor.execute('SELECT * FROM tblPeopleImport')
    result = cursor.fetchall()
    json_result = json.dumps(result);
    resp = Response(json_result, status=200, mimetype='application/json')
    return resp


@app.route('/api/v1/people/<int:people_id>', methods=['GET'])
def api_retrieve(people_id) -> str:
    cursor = mysql.get_db().cursor()
    cursor.execute('SELECT * FROM tblPeopleImport WHERE id=%s', people_id)
    result = cursor.fetchall()
    json_result = json.dumps(result);
    resp = Response(json_result, status=200, mimetype='application/json')
    return resp


@app.route('/api/v1/people/<int:people_id>', methods=['PUT'])
def api_edit(people_id) -> str:
    cursor = mysql.get_db().cursor()
    content = request.json
    inputData = (content['fldName'], content['fldSex'], content['fldAge'],
                 content['fldHeight'], content['fldWeight'], people_id)
    sql_update_query = """UPDATE tblPeopleImport t SET t.fldName = %s, t.fldSex = %s, t.fldAge = %s, t.fldHeight = 
        %s, t.fldWeight = %s WHERE t.id = %s """
    cursor.execute(sql_update_query, inputData)
    mysql.get_db().commit()
    resp = Response(status=200, mimetype='application/json')
    return resp

@app.route('/api/v1/people', methods=['POST'])
def api_add() -> str:

    content = request.json

    cursor = mysql.get_db().cursor()
    inputData = (content['fldName'], content['fldSex'], content['fldAge'],
                 content['fldHeight'], content['fldWeight'] )
    sql_insert_query = """INSERT INTO tblPeopleImport (fldName,fldSex,fldAge,fldHeight,fldWeight) VALUES (%s, %s,%s, %s,%s) """
    cursor.execute(sql_insert_query, inputData)
    mysql.get_db().commit()
    resp = Response(status=201, mimetype='application/json')
    return resp

@app.route('/api/v1/people/<int:people_id>', methods=['DELETE'])
def api_delete(people_id) -> str:
    cursor = mysql.get_db().cursor()
    sql_delete_query = """DELETE FROM tblPeopleImport WHERE id = %s """
    cursor.execute(sql_delete_query, people_id)
    mysql.get_db().commit()
    resp = Response(status=200, mimetype='application/json')
    return resp


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)