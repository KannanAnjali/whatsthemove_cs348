from select import select
from flask import Flask, render_template, request, redirect, url_for
import pymysql

application = Flask(__name__)


# made db connection

conn = pymysql.connect(
    host="awseb-e-qc6idp2hcz-stack-awsebrdsdatabase-zkebuinx4tlr.cq087g9hv6sl.us-east-2.rds.amazonaws.com",
    user="AnjaliK",
    passwd="cs3481234!",
    db='ebdb'
)

cur = conn.cursor()


@application.route('/', methods=["POST", "GET"])
def city():
    '''
    conn = pymysql.connect(
        host="awseb-e-qc6idp2hcz-stack-awsebrdsdatabase-zkebuinx4tlr.cq087g9hv6sl.us-east-2.rds.amazonaws.com",
        user="AnjaliK",
        passwd="cs3481234!",
        db='ebdb'
    )

    cur = conn.cursor()
    '''
    if request.method == 'POST':

        city_name = request.form['city_name']
        cur.execute('select count(*) from city')
        city_id = cur.fetchone()[0]
        print(city_id)
        state_name = request.form['state_name']
        population = request.form['population']
        safety = request.form['safety']
        query = "INSERT INTO city (city_id, name, state_name, population, safety) VALUES ({0}, '{1}', '{2}', {3}, {4})".format(
            city_id, city_name, state_name, population, safety)
        print(query)
        cur.execute(query)
        conn.commit()
    return render_template("index.html")

#


#
if __name__ == '__main__':
    application.run(debug=True)
