from flask import Flask, render_template, request, jsonify

app = Flask(_name_)

@app.route('/')
def home():
   return render_template('index.html')

if _name_ == '_main_':
   app.run('0.0.0.0', port=5000, debug=True)