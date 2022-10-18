from flask import Flask, render_template, request, jsonify
from pymongo import MongoClient

client = MongoClient("mongodb+srv://RistanAA:admin@cluster0.xldtokf.mongodb.net/?retryWrites=true&w=majority")
db = client.dbsparta

app = Flask(__name__)

@app.route('/')
def home():
   return render_template('login.html')
   
@app.route('/vote')
def vote():
   return render_template('index.html')
   
@app.route('/login' , methods=["POST"])
def login():
   username_receive = request.form["username_give"]
   password_receive = request.form["password_give"]

   user = list(db.users.find({'username':username_receive, 'password':password_receive},{'_id':False}))
   if user :
      return jsonify({'msg':"Login Berhasil", 'status':True})
   else :
      return jsonify({'msg':"user tidak ada", 'status':False})
      
   

@app.route("/bucket", methods=["POST"])
def bucket_post():
    bucket_receive = request.form["bucket_give"]
    count = db.bucket.count_documents({})
    num = count + 1
    doc = {
        'num':num,
        'bucket': bucket_receive,
        'done':0
    }
    db.bucket.insert_one(doc)
    return jsonify({'msg':'data saved!'})

@app.route("/bucket/done", methods=["POST"])
def bucket_done():
    num_receive = request.form["num_give"]
    db.bucket.update_one(
        {'num': int(num_receive)},
        {'$set': {'done': 1}})
    return jsonify({'msg': 'Update done!'})

@app.route("/bucket/cancel", methods=["POST"])
def bucket_cancel():
    num_receive = request.form["num_give"]
    db.bucket.update_one(
        {'num': int(num_receive)},
        {'$set': {'done': 0}})
    return jsonify({'msg': 'Update done!'})

@app.route("/bucket", methods=["GET"])
def bucket_get():
    buckets_list = list(db.bucket.find({},{'_id':False}))
    return jsonify({'buckets':buckets_list})

if __name__ == '__main__':
   app.run('0.0.0.0', port=5000, debug=True)