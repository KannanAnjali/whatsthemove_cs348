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
    global select_dest
    cur.execute('select c1.city_id, c1.name, s1.name,c2.name, s2.name from city c1 join state s1 on c1.state_name = s1.name, city c2 join state s2 on c2.state_name = s2.name where c1.name <> c2.name')
    city_state_lists = cur.fetchall()
    city_state_lists = list(city_state_lists)
    city_state_lists.append((-1,'starting city', 'starting state', 'destination city','destination state'))
    city_state_lists.sort(key=lambda y: y[0])
    selected = (request.form.get('city_state'))
    if selected != None:
        selected = selected.replace('(','')
        selected = selected.replace(')','')
        selected = selected.replace('\'','')
        select_dest = selected.split(',')
    return render_template('index.html', city_state_lists = city_state_lists, selected = selected)

@application.route('/flight', methods=["POST", "GET"])
def flight():
    print('inside flights')
    print(select_dest)
    
    cur.execute('select * from flights')
    flights_info = cur.fetchall()
    return render_template('flights.html', flights_info = flights_info)


@application.route("/activities", methods=['POST', 'GET'])
def activities():
    cur.execute('select * from activities')
    activities_info = cur.fetchall()
    return render_template('activities.html', activities_info = activities_info)


@application.route("/accomodations", methods=['POST', 'GET'])
def accomodation():
    return render_template('accomodations.html')

@application.route("/state", methods=['POST', 'GET'])
def state():
    name = request.form.get('name')
    time_zone = request.form.get('time_zone')
    popularity = (request.form.get('popularity'))
    best_season = request.form.get('best_season')
    affordability = request.form.get('affordability')

    cur.execute('select name from state')
    states = cur.fetchall()
    states = str(states)
    states = states.replace('(','')
    states = states.replace(')','')
    # states = states.replace(',','')
    states = states.replace('\'','')
    states = states.split(',,')
    
    if name not in states and name != None:
        popularity = int(popularity)
        print(type(name))
        print(type(time_zone))
        print(type(popularity))
        print(type(best_season))
        print(type(affordability))
        cur.execute('select state_id from state')
        ids = cur.fetchall()
        ids = str(ids)
        ids = ids.replace('(','')
        ids = ids.replace(')','')
        ids = ids.split(',,')
        ids = [int(i.replace(',','')) for i in ids]
        print(ids)
        val = int(max(ids)) + 1
        print(val)
        print((val, name, time_zone, int(popularity), best_season, affordability))
        cur.execute("INSERT INTO state (state_id, name, time_zone, popularity, best_season, affordability) VALUES ({0}, '{1}', '{2}', {3}, '{4}','{5}')".format
                (val, name, time_zone, int(popularity), best_season, affordability))
        conn.commit()

    cur.execute('select name from state')
    states = cur.fetchall()
    return render_template('state.html', states = states)



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

