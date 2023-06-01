#!/usr/bin/env python3

from flask import Flask, render_template
app = Flask(__name__)

@app.route('/')
def main():
    return render_template('index_slam.html')

if __name__ == '__main__':
    app.run(host='192.168.0.141', port=8880)#, debug=True)
    #app.run(host='192.168.70.200', port=8880)#, debug=True)
