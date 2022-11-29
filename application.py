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


@application.route('/', methods=['POST', 'GET'])
def main():
    cur.execute(
        'select c.city_id, c.name, s.name from city c join state s on c.state_name = s.name')
    city_state_lists = cur.fetchall()
    return render_template('index.html', city_state_lists=city_state_lists)


@application.route('/select_first_location', methods=["POST", "GET"])
def starting_location():
    return request.form['city_state']


@application.route('/destination_location', methods=["POST", "GET"])
def destination_location():
    return request.form['dcity_state']


@application.route("/starting_date", methods=["POST", "GET"])
def starting_date():
    return request.form['starting_date']


@application.route("/returning_date", methods=["POST", "GET"])
def returning_date():
    return request.form['returning_date']


@application.route("/restaurants", methods=['POST', 'GET'])
def restaurant():
    return render_template('restaurant.html')


@application.route("/flights", methods=['POST', 'GET'])
def flight():
    return render_template('flights.html')


@application.route("/activities", methods=['POST', 'GET'])
def activities():
    return render_template('activities.html')


@application.route("/accomodations", methods=['POST', 'GET'])
def accomodation():
    return render_template('accomodations.html')


@application.route('/cities', methods=['POST', 'GET'])
def city():
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
    return render_template("cities.html")


if __name__ == '__main__':
    application.run(debug=True)
