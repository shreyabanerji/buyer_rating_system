from flask import Flask, request , jsonify
import requests
import re
import datetime
import json
import pymysql

def connection():
    config = pymysql.connect (
            user = 'root',
           password = 'vand@mysql',
           host = 'localhost',
           database =  'brs',
            )
    
    return config


config = connection()

app = Flask(__name__)

# ---------------------------------------------------------------------------------------------------------------------------------------------------------

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
			query += col1[i] + "=" + '\'' + str(val1[i]) + '\'' + ","
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
	
	#getting category, price and rating :
	 
	cond1 = "p_id =" + str(data['p_id'])
	reply1 = list(requests.get("http://127.0.0.1:5000/brs/db/read",json = {"table":"products","columns":["category","price"],"where": cond1 }).json())
	category1 = reply1[0][0]
	price1 = reply1[0][1]
	cond2 = "user_id =" + str(data['user_id'])
	reply2 = list(requests.get("http://127.0.0.1:5000/brs/db/read",json = {"table":"User","columns":["rating"],"where": cond2 }).json())
	rating1 = reply2[0][0]
    
	
	#populating order details table :
	book_d = datetime.datetime.now()
	exp_d = book_d + datetime.timedelta(days=5)
	
	ans1 = requests.post("http://127.0.0.1:5000/brs/db/write",json ={"op":"Insert","table":"order_details","column":["o_id","order_status","book_date","exp_del_date"],"value":[str(data['o_id']),data['order_status'],str(book_d),str(exp_d)]})
	
	#populating payment_info:
	ans2= requests.post("http://127.0.0.1:5000/brs/db/write",json ={"op":"Insert","table":"payment_info","column":["o_id","pay_id","pay_method"],"value":[str(data['o_id']),data['pay_id'],data['pay_method']]})
	ans3 = requests.post("http://127.0.0.1:5000/brs/rules/book",json ={"user_id":data["user_id"],"pay_method":data["pay_method"],"category":category1,"price":price1,"rating":rating1})
    

	reply3 = list(requests.get("http://127.0.0.1:5000/brs/db/read",json = {"table":"User","columns":["rating"],"where": cond2 }).json())
	rating11 = reply3[0][0];
	ans4 = requests.post("http://127.0.0.1:5000/brs/rules/offer",json ={"user_id":data["user_id"],"order_status":data["order_status"],"pay_method":data["pay_method"],"category":category1,"price":price1,"rating":rating11})
	ans5 = requests.post("http://127.0.0.1:5000/brs/rules/reject",json ={"user_id":data["user_id"],"order_status":data["order_status"],"pay_method":data["pay_method"],"category":category1,"price":price1,"rating":rating11})
    
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
	cond1 = "o_id =" + str(data['o_id'])
	reply1 = list(requests.get("http://127.0.0.1:5000/brs/db/read",json = {"table":"order_details","columns":["order_status"],"where": cond1 }).json())
	order_status2 = reply1[0][0]
	reply2 = list(requests.get("http://127.0.0.1:5000/brs/db/read",json = {"table":"payment_info","columns":["pay_method"],"where": cond1 }).json())
	pay_method2 = reply2[0][0]
	reply3 = list(requests.get("http://127.0.0.1:5000/brs/db/read",json = {"table":"orders","columns":["p_id"],"where": cond1 }).json())
	p_id2 = reply3[0][0]

	cond2 = "p_id =" + str(p_id2)
	reply4 = list(requests.get("http://127.0.0.1:5000/brs/db/read",json = {"table":"products","columns":["category","price"],"where": cond2 }).json())
	category2 = reply4[0][0]
	price2 = reply4[0][1]

	cond3 = "user_id =" + str(data['user_id'])
	reply5 = list(requests.get("http://127.0.0.1:5000/brs/db/read",json = {"table":"User","columns":["rating"],"where": cond3 }).json())
	rating2 = reply5[0][0]
    
	ans2 = requests.post("http://127.0.0.1:5000/brs/rules/cancel",json ={"user_id":data["user_id"],"order_status":order_status2,"pay_method":pay_method2,"category":category2,"price":price2,"rating":rating2})

	reply6 = list(requests.get("http://127.0.0.1:5000/brs/db/read",json = {"table":"User","columns":["rating"],"where": cond3 }).json())
	rating22 = reply6[0][0];
	ans4 = requests.post("http://127.0.0.1:5000/brs/rules/offer",json ={"user_id":data["user_id"],"order_status":order_status2,"pay_method":pay_method2,"category":category2,"price":price2,"rating":rating22})
	ans5 = requests.post("http://127.0.0.1:5000/brs/rules/reject",json ={"user_id":data["user_id"],"order_status":order_status2,"pay_method":pay_method2,"category":category2,"price":price2,"rating":rating22})
	ans6 = requests.post("http://127.0.0.1:5000/brs/db/write",json ={"op":"Update","table":"order_details","column":["order_status"],"value":["cancelled"],"where": cond1})
          
    


	return jsonify({}),200



# -------------------------------------------------------------------------------------------------------------------------------

# Dynamically updation of 'rules' table :
    
@app.route('/brs/rules/update',methods=['POST'])
def update_rules():
	#{"rule_id":"R101","fact":"category","operator":"equal","value":"Electronics","type":"booking","message":"increment 0.25 star"}
	data = request.get_json()

	# Writing into the cancel details table :
	ans = requests.post("http://127.0.0.1:5000/brs/db/write",json ={"op":"Insert","table":"rules","column":["rule_id","fact","operator","value","type","message"],"value":[data['rule_id'],data['fact'],data['operator'],data['value'],data['type'],data['message']]})
 
	return jsonify({}),200
	   
# --------------------------------------------------------------------------------------------------------------------------------

# Calculate the rating (for messages from 'booking' topic):

@app.route('/brs/rules/book',methods=['POST'])
def calc_star_booking():
    if request.method != 'POST':
        return jsonify({}),405
    input = request.get_json()
    #input = {"user_id":"100006","pay_method":"COD","category":"Electronics","price":"70000","rating":"3"}
    cond1 = "type =" + "booking" 
    rule = list(requests.get("http://127.0.0.1:5000/brs/db/read",json = {"table":"rules","columns":["fact","operator","value","message"],"where": cond1 }).json())
    #rule = [["category","equal","Electronics","increment 0.25 star"],["pay_method","not equal","COD","increment 0.25 star"],["price","greater Than Inclusive","30000","increment 0.25 star"]]
    for r in rule:    
        if (r[1].lower() == "equal" and input[r[0]] == str(r[2])) or (r[1].lower() == "not equal" and input[r[0]] != str(r[2])) or (r[1].lower() == "greater than inclusive" and input[r[0]] >= r[2]) or (r[1].lower() == "greater than exclusive" and input[r[0]] > r[2]) or (r[1].lower() == "lesser than inclusive" and input[r[0]] <= r[2]) or (r[1].lower() == "lesser than exclusive" and input[r[0]] < r[2]):
            val = float(r[3].split(" ")[1])
            input["rating"] = str(float(input["rating"]) + val)
    if input["rating"] <= "5" and input["rating"] >= "0" :
        cond2 = "user_id=" + str(input["user_id"]) 
        ans1 = requests.post("http://127.0.0.1:5000/brs/db/write",json ={"op":"Update","table":"User","column":["rating"],"value":[input["rating"]],"where": cond2})
            
    return jsonify({}),200


# Calculate the rating (for messages from 'cancellation' topic):

@app.route('/brs/rules/cancel',methods=['POST'])
def calc_star_cancellation():
    if request.method != 'POST':
        return jsonify({}),405
    input = request.get_json()
    #input = {"user_id":"100006","order_status":"delivered","pay_method":"COD","category":"Electronics","price":"70000","rating":"3"}
    cond1 = "type =" + "cancellation" 
    rule = list(requests.get("http://127.0.0.1:5000/brs/db/read",json = {"table":"rules","columns":["fact","operator","value","message"],"where": cond1 }).json())
    #rule = [["category","equal","Electronics","decrement 0.5 star"],["order_status","equal","delivered","decrement 0.5 star"],["order_status","equal","in_progress","decrement 0.25 star"]]
    for r in rule:    
        if (r[1].lower() == "equal" and input[r[0]] == str(r[2])) or (r[1].lower() == "not equal" and input[r[0]] != str(r[2])) or (r[1].lower() == "greater than inclusive" and input[r[0]] >= r[2]) or (r[1].lower() == "greater than exclusive" and input[r[0]] > r[2]) or (r[1].lower() == "lesser than inclusive" and input[r[0]] <= r[2]) or (r[1].lower() == "lesser than exclusive" and input[r[0]] < r[2]):
            val = float(r[3].split(" ")[1])
            input["rating"] = str(float(input["rating"]) - val)
    if input["rating"] <= "5" and input["rating"] >= "0" :
        cond2 = "user_id=" + str(input["user_id"]) 
        ans1 = requests.post("http://127.0.0.1:5000/brs/db/write",json ={"op":"Update","table":"User","column":["rating"],"value":[input["rating"]],"where": cond2})
            
    return jsonify({}),200


# Calculate the rating (for messages from both topics):

@app.route('/brs/rules/offer',methods=['POST'])           
def offer():
    if request.method != 'POST':
        return jsonify({}),405
    input = request.get_json()
    #input = {"user_id":"100006","order_status":"delivered","pay_method":"COD","category":"Electronics","price":"70000","rating":"3"}
    cond1 = "type =" + "offer" 
    rule = list(requests.get("http://127.0.0.1:5000/brs/db/read",json = {"table":"rules","columns":["fact","operator","value","message"],"where": cond1 }).json())
    #rule = [["rating","greater Than Inclusive","4","offer coupon"],["rating","greater Than Inclusive","2","offer cod"]]
    output = []
    for r in rule:    
        if (r[1].lower() == "equal" and input[r[0]] == str(r[2])) or (r[1].lower() == "not equal" and input[r[0]] != str(r[2])) or (r[1].lower() == "greater than inclusive" and input[r[0]] >= r[2]) or (r[1].lower() == "greater than exclusive" and input[r[0]] > r[2]) or (r[1].lower() == "lesser than inclusive" and input[r[0]] <= r[2]) or (r[1].lower() == "lesser than exclusive" and input[r[0]] < r[2]):
            output.append(r[3])
            
    cond2 = "user_id=" + str(input["user_id"]) 
    print("rules:---------------------------------", output)
    for mes in output:
        if "cod" in mes.lower():
            ans1 = requests.post("http://127.0.0.1:5000/brs/db/write",json ={"op":"Update","table":"User","column":["cod"],"value":["yes"],"where": cond2})
        if "coupon" in mes.lower():
            ans2 = requests.post("http://127.0.0.1:5000/brs/db/write",json ={"op":"Update","table":"User","column":["coupon"],"value":["yes"],"where": cond2})
            
    return jsonify({}),200 


# Calculate the rating (for messages from both topics):

@app.route('/brs/rules/reject',methods=['POST'])
def reject():
    if request.method != 'POST':
        return jsonify({}),405
    input = request.get_json()
    #input = {"user_id":"100006","order_status":"delivered","pay_method":"COD","category":"Electronics","price":"70000","rating":"3"}
    cond1 = "type =" + "reject" 
    rule = list(requests.get("http://127.0.0.1:5000/brs/db/read",json = {"table":"rules","columns":["fact","operator","value","message"],"where": cond1 }).json())
    #rule = [["rating","lesser Than Exclusive","2","reject coupon and cod"]]
    output = []
    for r in rule:    
        if (r[1].lower() == "equal" and input[r[0]] == str(r[2])) or (r[1].lower() == "not equal" and input[r[0]] != str(r[2])) or (r[1].lower() == "greater than inclusive" and input[r[0]] >= r[2]) or (r[1].lower() == "greater than exclusive" and input[r[0]] > r[2]) or (r[1].lower() == "lesser than inclusive" and input[r[0]] <= r[2]) or (r[1].lower() == "lesser than exclusive" and input[r[0]] < r[2]):
            output.append(r[3])
    cond2 = "user_id=" + str(input["user_id"]) 
    print("rules:---------------------------------", output)
    for mes in output:
        if "cod" in mes.lower():
            ans1 = requests.post("http://127.0.0.1:5000/brs/db/write",json ={"op":"Update","table":"User","column":["cod"],"value":["no"],"where": cond2})
        if "coupon" in mes.lower():
            ans2 = requests.post("http://127.0.0.1:5000/brs/db/write",json ={"op":"Update","table":"User","column":["coupon"],"value":["no"],"where": cond2})
            
            
    return jsonify({}),200  

    
if __name__ == '__main__':
    app.run()
