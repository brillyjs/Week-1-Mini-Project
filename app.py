from flask import Flask, render_template, request, jsonify
from pymongo import MongoClient

client = MongoClient("mongodb+srv://RistanAA:admin@cluster0.xldtokf.mongodb.net/?retryWrites=true&w=majority")
db = client.dbsparta

app = Flask(__name__)

@app.route('/')
def home():
   return render_template('login.html')

if __name__ == '__main__':
   app.run('0.0.0.0', port=5000, debug=True)