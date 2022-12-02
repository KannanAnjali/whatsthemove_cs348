from flask import Flask, render_template, request, redirect, url_for
import pymysql
from datetime import datetime

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
    lists = []
    for i in city_state_lists:
        i = str(i)
        i = i.replace('(', '')
        i = i.replace(')', '')
        i = i.replace('\'', '')
        i = i.replace(' ', '')
        i = i.split(',')
        i[0] = int(i[0])
        lists.append(i)
    lists.append([-1, 'starting city', 'starting state', 'destination city', 'destination state'])
    lists.sort(key=lambda y: y[0])
    # print(lists)
    selected = (request.form.get('city_state'))
    if selected != None:
        select_dest = selected
        select_dest = select_dest.replace('(', '')
        select_dest = select_dest.replace(')', '')
        select_dest = select_dest.replace('\'', '')
        select_dest = select_dest.replace(' --> ', ',')
        select_dest = select_dest.split(',')
        vals = []
        for i in select_dest:
            vals.append(i.strip())
        select_dest = vals
    return render_template('index.html', city_state_lists=lists, selected=selected)


@application.route('/flight', methods=["POST", "GET"])
def flight():
    print('inside flights')
    print(select_dest)

    sc = '\''+str(select_dest[0])+'\''
    ss = '\''+str(select_dest[1])+'\''
    dc = '\''+str(select_dest[2])+'\''
    ds = '\''+str(select_dest[3])+'\''
    select_statement = 'select * from flights '
    where_statement = 'where startCity='+ sc +' and startState=' + ss+' and destCity=' + dc + ' and destState=' + ds
    statement = select_statement + where_statement
    print(statement)
    cur.execute(statement)
    flights_info = cur.fetchall()
    vals = []
    for i in flights_info:
        i = list(i)
        i[10] = i[10].strftime("%H:%M:%S")
        i[11] = i[11].strftime("%H:%M:%S")
        vals.append(i)
    flights_info = vals
    print(flights_info)
    return render_template('flights.html', flights_info=flights_info)


@application.route("/activities", methods=['POST', 'GET'])
def activities():
    print('inside activities')
    print(select_dest)
    dc = '\''+str(select_dest[2])+'\''
    ds = '\''+str(select_dest[3])+'\''
    select_statement = 'select * from activities '
    where_statement = 'where destCity=' + dc + ' and destState=' + ds
    statement = select_statement + where_statement
    print(statement)
    cur.execute(statement)
    activities_info = cur.fetchall()
    return render_template('activities.html', activities_info = activities_info)

@application.route("/index-activities", methods=['POST', 'GET'])
def activities_add():
    print('add activities!')
    cur.execute('select name from city')
    city_dropdown = cur.fetchall()
    if request.form != None:
        print('entered here')
        name = request.form.get('Activity_Name')
        category = request.form.get('category')
        price = request.form.get('price')
        length_of_time = request.form.get('length_of_time')
        #cur.execute('select state.name from city, state where city.state_name = state.name and city.name = {0}'.format(city))
        #state = cur.fetchall
        print(name, category, price, length_of_time)
    return render_template('index-activities.html', city_dropdown = city_dropdown)


@application.route("/accommodations", methods=['POST', 'GET'])
def accommodation():
    print('inside accommodations')
    print(select_dest)
    dc = '\''+str(select_dest[2])+'\''
    ds = '\''+str(select_dest[3])+'\''
    select_statement = 'select * from accommodations '
    where_statement = 'where destCity=' + dc + ' and destState=' + ds
    statement = select_statement + where_statement
    print(statement)
    cur.execute(statement)
    accommodations_info = cur.fetchall()
    return render_template('accommodations.html', accommodations_info=accommodations_info)

@application.route("/index-restaurant", methods=['POST', 'GET'])
def restaurants_add():
    print('add restaurants!')
    cur.execute('select name from city')
    city_dropdown = cur.fetchall()
    if request.form != None:
        print('entered here')
        name = request.form.get('Restaurant_Name')
        type = request.form.get('restaurant_type')
        cuisine = request.form.get('cuisine')
        price = request.form.get('price')
        stars = request.form.get('stars')
        city = request.form.get('city')
        #cur.execute('select state.name from city, state where city.state_name = state.name and city.name = {0}'.format(city))
        #state = cur.fetchall
        print(name, type, cuisine, price, stars, city, state)
    return render_template('index-restaurants.html', city_dropdown = city_dropdown)


@application.route("/restaurants", methods=['POST', 'GET'])
def restaurants_view():
    print('inside restaurant')
    print(select_dest)
    dc = '\''+str(select_dest[2])+'\''
    ds = '\''+str(select_dest[3])+'\''
    select_statement = 'select * from restaurants '
    where_statement = 'where destCity=' + dc + ' and destState=' + ds
    statement = select_statement + where_statement
    print(statement)
    cur.execute(statement)
    restaurants_info = cur.fetchall()
    #print(restaurants_info)

    return render_template('restaurant.html', restaurants_info = restaurants_info)


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
    states = states.replace('(', '')
    states = states.replace(')', '')
    # states = states.replace(',','')
    states = states.replace('\'', '')
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
        ids = ids.replace('(', '')
        ids = ids.replace(')', '')
        ids = ids.split(',,')
        ids = [int(i.replace(',', '')) for i in ids]
        print(ids)
        val = int(max(ids)) + 1
        print(val)
        print((val, name, time_zone, int(popularity), best_season, affordability))
        cur.execute("INSERT INTO state (state_id, name, time_zone, popularity, best_season, affordability) VALUES ({0}, '{1}', '{2}', {3}, '{4}','{5}')".format
                    (val, name, time_zone, int(popularity), best_season, affordability))
        conn.commit()

    cur.execute('select name from state')
    states = cur.fetchall()
    return render_template('state.html', states=states)


@application.route('/cities', methods=['POST', 'GET'])
def city():
    cur.execute('select * from city')
    cities_info = cur.fetchall()
    values = []
    for i in cities_info:
        i = str(i)
        i = i.replace('(', '')
        i = i.replace(')', '')
        i = i.replace('\'', '')
        i = i.replace(' ', '')
        i = i.split(',')
        values.append(i)
    cities_info = values
    print(cities_info)
    if request.method == 'POST':
        city_name = request.form['city_name']
        cur.execute('select count(*) from city')
        city_id = cur.fetchone()[0] + 1
        print(city_id)
        state_name = request.form['state_name']
        population = request.form['population']
        safety = request.form['safety']
        query = "INSERT INTO city (city_id, name, state_name, population, safety) VALUES ({0}, '{1}', '{2}', {3}, {4})".format(
            city_id, city_name, state_name, population, safety)
        cur.execute(query)
        conn.commit()
        cur.execute('select * from city')
        cities_info = cur.fetchall()

    return render_template("cities.html", cities_info = cities_info)


if __name__ == '__main__':
    application.run(debug=True)
