from ast import arg
from tokenize import group
from flask import Flask, render_template, request, jsonify, redirect
from pymongo import MongoClient

client = MongoClient('mongodb+srv://RistanAA:admin@cluster0.xldtokf.mongodb.net/?retryWrites=true&w=majority')
db = client.dbsparta

app = Flask(__name__)

@app.route('/')
def home():
   return render_template('login.html')
   
@app.route('/index')
def index():
   args = request.args
   return render_template('index.html', userLogin = args.get('username'))
   
@app.route('/login' , methods=["POST"])
def login():
   username_receive = request.form["username_give"]
   password_receive = request.form["password_give"]

   user = list(db.users.find({'username':username_receive},{'_id':False}))
   if user :
      cek = list(db.users.find({'username':username_receive, 'password':password_receive},{'_id':False}))  
      if cek :
        return jsonify({'msg':"Login Success", 'status':True})
      else :
         return jsonify({'msg':"Wrong Password", 'status':False})
   else :
      return jsonify({'msg':"User Not Found", 'status':False})
      
@app.route('/vote', methods=["POST"])
def vote():
    list_id = request.form['list_id']
    username = request.form['username']

    data = list(db.bucket.find({'num': int(list_id)}, {'_id':0}).sort('_id', -1))
    user = db.users.find_one({'username':username},{'_id':0})
    # print(user['status'])
    # print(data,list_id, username)
   

    if user['voted'] == 0:
        if len(data) > 0:
            vote = data[0]['vote'] + 1
            db.bucket.update_one(
                {'num': int(list_id)},
                {'$set': {'vote': vote}}
            )
            db.users.update_one(
                {'username': username},
                {'$set': {'voted': int(list_id)}}
            )
            i = 0
            sortedList= list(db.bucket.find({},{'_id':0}).sort('vote', -1))
            # print(tesss)
            totalVote = list(db.bucket.aggregate([{ '$group': { '_id': i+1, 'TotalVote': { '$sum': '$vote' } } }]))
            # print(totalVote[0]['TotalVote'])
            total_vote = totalVote[0]['TotalVote']
            total_user = db.users.count_documents({})
            # print(total_vote, total_user)
            if total_vote >= total_user:
               db.bucket.delete_many({})
               db.bucket.update_one(
                    {'num': int(sortedList[0]['num'])},
                    {'$set': {'vote': 0}}
                )
               db.users.update_many({},{ "$set": { "voted": 0, 'idea':0 } })
               return jsonify({'msg':"Vote Success", 'status': 'finish', 'voted':sortedList[0]['bucket']})
            
            return jsonify({'msg':"Vote Success", 'status': 'voted', 'voted':list_id})

    return jsonify({'msg':"You already voted"})


    

@app.route("/bucket", methods=["POST"])
def bucket_post():
    # sample_receive = request.form['sample_give']
    bucket_receive = request.form['bucket_give']
    username = request.form['username']

    count = list(db.bucket.find({}, {'num': 1, '_id':0}).sort('_id', -1))
    print(count)
    if len(count) > 0:
        num = count[0]['num'] + 1
    else:
        num = 1

    doc = {
        'num': num,
        'bucket': bucket_receive,
        'done': 0,
        'vote': 0
    }
    db.bucket.insert_one(doc)

    db.users.update_one(
        {'username': username},
        {'$set': {'idea': int(num)}}
    )  
    return jsonify({'msg': 'data saved!'})

@app.route("/bucket/done", methods=["POST"])
def bucket_done():
    num_receive = request.form['num_give']
    db.bucket.update_one(
        {'num': int(num_receive)},
        {'$set': {'done': 1}}
    )
    return jsonify({'msg': 'update done!'})

@app.route("/delete", methods=["POST"])
def delete_bucket():
    num_receive = request.form['num_give']
    db.bucket.delete_one({'num': int(num_receive)})
    return jsonify({'msg': 'delete done!'})

@app.route("/cancel", methods=["POST"])
def cancel_bucket():
    username = request.form['username']
    list_id = request.form['list_id']

    data = db.bucket.find_one({'num':int(list_id)},{'_id':0})
    # print(data, list_id)
    vote = data['vote'] - 1
    db.users.update_one(
        {'username': username},
        {'$set': {'voted': 0}}
    )
    db.bucket.update_one(
        {'num': int(list_id)},
        {'$set': {'vote': vote}}
    )
    return jsonify({'msg': 'cancel done!'})

@app.route("/bucket", methods=["GET"])
def bucket_get():
    
    username = request.args.get('username')
    buckets_list = list(db.bucket.find({}, {'_id': False}))

    user = db.users.find_one({'username':username},{'_id':0})

    # return jsonify({'buckets': buckets_list,'user':user}) 

    total_user_idea = db.users.count_documents({'idea':{'$ne' : 0}})
    total_user = db.users.count_documents({})
    print(total_user, total_user_idea)
    if total_user_idea == total_user :
        return jsonify({'buckets': buckets_list,'user':user, 'status': 'true'})
    else :
        return jsonify({'buckets': buckets_list,'user':user, 'status' : 'false'})

if __name__ == '__main__':
   app.run('0.0.0.0', port=5000, debug=True)