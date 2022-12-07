from flask import Flask, render_template, request, redirect, url_for
import pymysql
from datetime import datetime
import itertools

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
        #i = i.replace(' ', '')
        i = i.split(',')
        i[0] = int(i[0])
        lists.append(i)
    lists.append([-1, 'starting city', 'starting state',
                 'destination city', 'destination state'])
    lists.sort(key=lambda y: y[0])
    # print(lists)
    values = []
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
        select_statement = 'select * from city where name = ' + \
            '\''+str(select_dest[2])+'\''
        cur.execute(select_statement)
        city_info = cur.fetchall()
        city_info = list(city_info)
        select_statement = 'select * from state where name = ' + \
            '\''+str(select_dest[3])+'\''
        cur.execute(select_statement)
        state_info = cur.fetchall()
        state_info = list(state_info)
        city_info = city_info + state_info
        city_info = str(city_info)
        city_info = city_info.replace('(', '')
        city_info = city_info.replace(')', '')
        city_info = city_info.replace('\'', '')
        city_info = city_info.replace('[', ',')
        city_info = city_info.replace(']', ',')
        city_info = city_info.split(',')
        print(city_info)
        # vals = []
        index = 0
        for i in city_info:
            print(index)
            print(i)
            index = index + 1
        # print(vals)
        values = [city_info[4], city_info[1],
                  city_info[3], city_info[5], city_info[6]]
        # print(values)
    return render_template('index.html', city_state_lists=lists, selected=selected, city_info=values)


@application.route('/flight', methods=["POST", "GET"])
def flight():
    print('inside flights')
    print(select_dest)

    sc = '\''+str(select_dest[0])+'\''
    ss = '\''+str(select_dest[1])+'\''
    dc = '\''+str(select_dest[2])+'\''
    ds = '\''+str(select_dest[3])+'\''
    select_statement = 'select * from flights '
    where_statement = 'where startCity=' + sc + ' and startState=' + \
        ss+' and destCity=' + dc + ' and destState=' + ds
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
    return render_template('activities.html', activities_info=activities_info)


@application.route("/index-activities", methods=['POST', 'GET'])
def activities_add():
    print('add activities!')
    cur.execute('select name, state_name from city')
    city_dropdown = cur.fetchall()
    if request.form != None:
        print('request form is not null')
        name = request.form.get('activity_name')
        category = request.form.get('category')
        price = request.form.get('price')
        length_of_time = request.form.get('length')
        city = request.form.get('citystate')
        state = ""
        city_id = ""
        state_id = ""
        if (city != None):
            city_and_state = city.split(',')
            city = city_and_state[0]
            if (city_and_state[1][0] == ' '):
                state = city_and_state[1][1:]
            else:
                state = city_and_state[1]
            cur.execute('select count(*) from activities')
            activity_id = cur.fetchone()[0] + 1
            cur.execute(
                "select city.city_id from city where city.name = '{0}'".format(city, state))
            city_id_test = cur.fetchone()
            cur.execute(
                "select state.state_id from state where state.name = '{0}'".format(state))
            state_id_test = cur.fetchone()
            if (city_id_test != None and state_id_test != None):
                city_id = city_id_test[0]
                state_id = state_id_test[0]
                cur.execute("INSERT INTO activities (activity_id, name, category, city_id, state_id, price, length_of_time, destCity, destState) VALUES ({0}, '{1}', '{2}', {3}, {4}, {5}, {6}, '{7}', '{8}')".format(
                    activity_id, name, category, city_id, state_id, price, length_of_time, city, state))
                print("added entry in database")
                conn.commit()

        #cur.execute('select state.name from city, state where city.state_name = state.name and city.name = {0}'.format(city))
        #state = cur.fetchall
        print(name, category, price, length_of_time)
    return render_template('index-activities.html', city_dropdown=city_dropdown)


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
    cur.execute('select name, state_name from city')
    city_dropdown = cur.fetchall()
    if request.form != None:
        print('request form is not null')
        # print(request.form.getList())
        name = request.form.get('restaurant_name')
        rest_type = request.form.get('restaurant_type')
        cuisine = request.form.get('cuisine')
        price = request.form.get('price')
        stars = request.form.get('stars')
        city = request.form.get('citystate')
        state = ""
        if (city != None):
            city_and_state = city.split(',')
            city = city_and_state[0]
            if (city_and_state[1][0] == ' '):
                state = city_and_state[1][1:]
            else:
                state = city_and_state[1]
            cur.execute('select count(*) from restaurants')
            restaurant_id = cur.fetchone()[0] + 1
            city_id = ""
            state_id = ""
            cur.execute(
                "select city.city_id from city where city.name = '{0}'".format(city, state))
            city_id_test = cur.fetchone()
            cur.execute(
                "select state.state_id from state where state.name = '{0}'".format(state))
            state_id_test = cur.fetchone()
            if (city_id_test != None and state_id_test != None):
                city_id = city_id_test[0]
                state_id = state_id_test[0]
                cur.execute("INSERT INTO restaurants (restaurant_id, type, cuisine, price, state_id, city_id, name, stars, destCity, destState) VALUES ({0}, '{1}', '{2}', {3}, {4}, {5}, '{6}', {7}, '{8}', '{9}')".format(
                    restaurant_id, rest_type, cuisine, price, state_id, city_id, name, stars, city, state))
                print("added entry in database")
                conn.commit()
            print(restaurant_id, city_id, state_id)
            # cur.execute("INSERT INTO restaurants (state_id, name, time_zone, popularity, best_season, affordability) VALUES ({0}, '{1}', '{2}', {3}, '{4}','{5}')".format
            #        (val, name, time_zone, int(popularity), best_season, affordability))
        #cur.execute('select state.name from city, state where city.state_name = state.name and city.name = {0}'.format(city))
        #state = cur.fetchall
        print(name, rest_type, cuisine, price, stars, city, state)
        # print(city)
    return render_template('index-restaurants.html', city_dropdown=city_dropdown)


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
    # print(restaurants_info)

    return render_template('restaurant.html', restaurants_info=restaurants_info)


@application.route("/state", methods=['POST', 'GET'])
def state():
    message = ''
    name = request.form.get('name')
    time_zone = request.form.get('time_zone')
    popularity = (request.form.get('popularity'))
    best_season = request.form.get('best_season')
    affordability = request.form.get('affordability')

    cur.execute('CALL GetAllStates()')
    states = cur.fetchall()
    states = str(states)
    states = states.replace('(', '')
    states = states.strip()
    states = states.replace(')', '')
    states = states.replace('\'', '')
    # states = states.replace(',','')
    states = states.replace('\'', '')
    states = states.rstrip()
    states = states.split(',,')
    vals = []
    for i in states:
        i = i.strip()
        vals.append(i)
    states = vals
    if name in states:
        message = 'This state already exists'
    if name not in states and name != None:
        name = name.capitalize()
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
        cur.execute("set transaction  ISOLATION LEVEL READ COMMITTED;")
        cur.execute("INSERT INTO state (state_id, name, time_zone, popularity, best_season, affordability) VALUES ({0}, '{1}', '{2}', {3}, '{4}','{5}')".format
                    (val, name, time_zone, int(popularity), best_season, affordability))
        conn.commit()

    cur.execute('select name from state')
    states = cur.fetchall()
    return render_template('state.html', states=states, message=message)


@application.route('/cities', methods=['POST', 'GET'])
def city():
    message = ''
    #cur.execute('select * from city')
    #cities_info = cur.fetchall()
    values = []
    cities_names = []
    states_names = []
    # executing stored procedure to get all the cities in the database
    cur.execute('CALL GetAllCities()')
    cities_info = cur.fetchall()
    print(cities_info)
    for i in cities_info:
        i = str(i)
        i = i.replace('(', '')
        i = i.replace(')', '')
        i = i.replace('\'', '')
        i = i.replace(' ', '')
        i = i.split(',')
        values.append(i)
    for v in values:
        cities_names.append(v[1])
    cities_info = values
    # print(cities_info)
    if request.method == 'POST':
        city_name = request.form['city_name']
        cur.execute('select count(*) from city')
        city_id = cur.fetchone()[0] + 1
        print(city_id)
        state_name = request.form['state_name']
        population = request.form['population']
        safety = request.form['safety']
        city_name = city_name.capitalize()
        state_name = state_name.capitalize()
        cur.execute('select name from state')
        states = cur.fetchall()
        if not city_name in cities_names:
            query = "INSERT INTO city (city_id, name, state_name, population, safety) VALUES ({0}, '{1}', '{2}', {3}, {4})".format(
                city_id, city_name, state_name, population, safety)
            cur.execute(query)
            conn.commit()
        else:
            message = 'This city already exisits'
    return render_template("cities.html", cities_info=cities_info, message=message)


@application.route('/showCities', methods=['POST', 'GET'])
def showCity():
    values = []
    cities_names = []
    cur.execute('CALL GetAllCities()')
    cities_info = cur.fetchall()
    print(cities_info)
    for i in cities_info:
        i = str(i)
        i = i.replace('(', '')
        i = i.replace(')', '')
        i = i.replace('\'', '')
        #i = i.replace(' ', '')
        i = i.split(',')
        values.append(i)
    for v in values:
        cities_names.append(v[1])
    cities_info = values
    print(cities_info)
    return render_template("ShowCities.html", cities_info=cities_info)


@application.route('/groupByState', methods=['POST', 'GET'])
def groupByState():
    values = []
    cities_names = []
    cur.execute("Select * From city order by city.state_name")
    cities_info = cur.fetchall()
    print(cities_info)
    for i in cities_info:
        i = str(i)
        i = i.replace('(', '')
        i = i.replace(')', '')
        i = i.replace('\'', '')
        #i = i.replace(' ', '')
        i = i.split(',')
        values.append(i)
    for v in values:
        cities_names.append(v[1])
    cities_info = values
    print(cities_info)
    return render_template("ShowCities.html", cities_info=cities_info)


@application.route('/orderBySafety', methods=['POST', 'GET'])
def orderBySafety():
    values = []
    cities_names = []
    cur.execute("Select * From city order by city.safety")
    cities_info = cur.fetchall()
    print(cities_info)
    for i in cities_info:
        i = str(i)
        i = i.replace('(', '')
        i = i.replace(')', '')
        i = i.replace('\'', '')
        #i = i.replace(' ', '')
        i = i.split(',')
        values.append(i)
    for v in values:
        cities_names.append(v[1])
    cities_info = values
    print(cities_info)
    return render_template("ShowCities.html", cities_info=cities_info)


if __name__ == '__main__':
    application.run(debug=True)
