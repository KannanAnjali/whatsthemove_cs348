from flask import Flask,render_template,request,redirect,url_for
import pymysql

application = Flask(__name__)


#made db connection
conn = pymysql.connect(
            host ="awseb-e-qc6idp2hcz-stack-awsebrdsdatabase-zkebuinx4tlr.cq087g9hv6sl.us-east-2.rds.amazonaws.com",
            user ="AnjaliK",
            passwd ="cs3481234!",
            db='ebdb'
        )
      
cur = conn.cursor()


@application.route('/',methods=["POST","GET"])
def hello():
    if request.method == 'POST':
        name = request.form.get('nm')
        print(name)
        return redirect(url_for('insert'))
    return render_template("index.html")


@application.route('/insert')
def insert():
    return '<h1>attempting to insert </h1>'

if __name__ == '__main__':
    application.run(debug=True)