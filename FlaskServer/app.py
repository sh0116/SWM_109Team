
from flask import Flask, request, Response, jsonify, render_template


app = Flask(__name__)
app.debug = True
 
import json
import pymysql
import mysql.connector


 
# MySQL connect

db = mysql.connector.connect(host = "db109.cpehjs7hbg19.ap-northeast-2.rds.amazonaws.com",port = 3306,user = "admin",passwd = "admin109",db = "robot1")
curs = db.cursor()
app.config['JSON_AS_ASCII'] = False
 

@app.route('/search')
def item_search():
    return render_template('test.html')
    
@app.route('/item_request', methods =['POST'])
def item_query():
    value1 = request.form['item_id']
    item_sql = "select * from addresstest where name ='"+value1+"'"
    curs.execute(item_sql)
    row_headers=[x[0] for x in curs.description]
    rows=curs.fetchall()            
    json_data=[]                                        #list
    for result in rows:
        json_data.append(dict(zip(row_headers,result)))
    
    json_return=json.dumps(json_data[0],ensure_ascii=False)   #string #json
 
    return jsonify(json_return)
 
    curs.close()
 
if __name__=='__main__':
    app.run(host='0.0.0.0',port=5000, debug=True)
