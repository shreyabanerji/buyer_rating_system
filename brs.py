from flask import Flask, request , jsonify
import requests
import re
import datetime
import json
import pymysql

def connection():
    config = pymysql.connect (
            user = 'root',
           password = 'password123',
           host = 'localhost',
           database =  'brs',
            )
    
    return config


config = connection()

app = Flask(__name__)


#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# API to Read Database :

@app.route('/brs/db/read',methods = ['GET'])
def read_from_db():
	if request.method != 'GET':
		return jsonify({}),405

	# MAKING OF THE QUERY :------------------------------------------

	''' 
	Queries handled :
		1. SELECT list_of_cols FROM table_name [WHERE condition]

		-> where, condition can be single or multiple equality expressions.
	'''

	data = request.get_json()
	tab1=data['table']
	col1 = data['columns']
	query = "SELECT "
	for i in range(len(col1)):
		query += col1[i] + ","
	query = query.strip(",")
	try:
		conds = data['where'].split(',')
		query += " FROM " + tab1 + " WHERE "
		for i in conds:
			x = i.split('=')
			query += x[0] +'='+'\''+x[1]+'\''+" AND "
		query = query.strip(" AND ")

	except:
		query += " FROM " + tab1 + " "

	db = config.cursor()
	db.execute(query)
	read = db.fetchall()

	return jsonify(read)


#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# API to Write Database :

@app.route('/brs/db/write',methods = ['POST'])
def write_to_db():
	if request.method != 'POST':
		return jsonify({}),405

	# MAKING OF THE QUERY :---------------------------------

	''' 
	Queries handled :
		1. INSERT INTO table_name (columns) VALUES (values)
		2. DELETE FROM table_name WHERE condition
		3. UPDATE table_name SET c1=v1,c2=v2.. [ WHERE condition ]

		-> where, condition can be single or multiple equality expressions.
	'''

	query=""

	data = request.get_json()
	op1 = data['op']
	tab1=data['table']
	if (op1=='Insert'):
		col1 = data['column']
		val1 = data['value']
		l = len(col1)
		query += "INSERT INTO " + tab1 + " ("
		for i in range(l):
			query += col1[i] + ","
		query = query.strip(",")
		query += ") VALUES ("
		for i in range(l):
			query += '\'' + val1[i] + '\'' + ","
		query = query.strip(",")
		query += ")"

	elif(op1=="Delete"):
		conds = data['where'].split(',')
		query += "DELETE FROM " + tab1 + " WHERE "
		for i in conds:
			x = i.split('=')
			query += x[0] +'='+'\''+x[1]+'\'' + " AND "
		query = query.strip(" AND ")

	elif(op1=="Update"):
		col1 = data['column']
		val1 = data['value']
		l = len(col1)
		query += "UPDATE " + tab1 + " SET "
		for i in range(l):
			query += col1[i] + "=" + '\'' + val1[i] + '\'' + ","
		query = query.strip(",")
		try :
			conds = data['where'].split(',')
			query += " WHERE "
			for i in conds:
				x = i.split('=')
				query += x[0] +'='+'\''+x[1]+'\''+" AND "
			query = query.strip(" AND ")

		except:
			query = query
		#print(query)


	# Executing the query -------------------------------------

	db = config.cursor()
	db.execute(query)
	config.commit()

	return jsonify({"done":"writing"})



#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# API to Order a product :

@app.route('/brs/book',methods=['POST'])
def book():
	data = request.get_json()
	#{"o_id":"A102","user_id":"100006","p_id":"P103","order_status":"in_progress","pay_method":"COD","pay_id":"1113"}
	{}
	
	#populating orders table :
	ans = requests.post("http://127.0.0.1:5000/brs/db/write",json ={"op":"Insert","table":"orders","column":["o_id","u_id","p_id"],"value":[data["o_id"],data['user_id'],data['p_id']]})
	
	#getting order id :
	'''
	cond1 = "u_id =" +"\"" +str(data['user_id'])+ "\""+ ',' + "p_id =" + "\""+str(data['p_id']+"\"")
	print(cond1)
	reply1 = list(requests.post("http://127.0.0.1:5000/brs/db/read",json = {"table":"orders","columns":["o_id"],"where": cond1 }).json())
	o_id = reply1[0][0]
	'''
	#populating order details table :
	book_d = datetime.datetime.now()
	exp_d = book_d + datetime.timedelta(days=5)
	
	ans1 = requests.post("http://127.0.0.1:5000/brs/db/write",json ={"op":"Insert","table":"order_details","column":["o_id","order_status","book_date","exp_del_date"],"value":[str(data['o_id']),data['order_status'],str(book_d),str(exp_d)]})
	
	#populating payment_info:
	ans2= requests.post("http://127.0.0.1:5000/brs/db/write",json ={"op":"Insert","table":"payment_info","column":["o_id","pay_id","pay_method"],"value":[str(data['o_id']),data['pay_id'],data['pay_method']]})
	
	return jsonify({}),200

#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# API to cancel a order :

@app.route('/brs/cancel',methods=['POST'])
def cancel():
	#{"user_id":"100006","o_id":"A102","reason":"1"}
	data = request.get_json()

	# Writing into the cancel details table :
	canceld = datetime.datetime.now()
	ans1 = requests.post("http://127.0.0.1:5000/brs/db/write",json ={"op":"Insert","table":"cancel_details","column":["o_id","cancel_date","reason"],"value":[data['o_id'],str(canceld),data['reason']]})
	
	
	
	# --- code for updating the user rating ------- 


	return jsonify({}),200





if __name__ == '__main__':
    app.run()
