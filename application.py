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
select_dest = None

@application.route('/', methods=['POST', 'GET'])
def main():
    cur.execute('select c1.city_id, c1.name, s1.name,c2.name, s2.name from city c1 join state s1 on c1.state_name = s1.name, city c2 join state s2 on c2.state_name = s2.name where c1.name <> c2.name')
    city_state_lists = cur.fetchall()
    city_state_lists = list(city_state_lists)
    city_state_lists.append((-1,'starting city', 'starting state', 'destination city','destination state'))
    city_state_lists.sort(key=lambda y: y[0])
    selected = (request.form.get('city_state'))
    print(selected)
    return render_template('index.html', city_state_lists = city_state_lists,selected =selected)

@application.route('/flight', methods=["POST", "GET"])
def flight():
    cur.execute('select * from flights')
    flights_info = cur.fetchall()
    return render_template('flights.html', flights_info = flights_info)


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

