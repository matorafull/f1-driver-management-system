import os
from flask import Flask, render_template, request, redirect, url_for, session, flash
from database import get_db_connection, execute_query
from psycopg2.extras import RealDictCursor

base_dir = os.path.abspath(os.path.dirname(__file__))
root_dir = os.path.dirname(base_dir)
app = Flask(
    __name__,
    template_folder=os.path.join(root_dir, 'templates')
)
app.secret_key = 'f1_secret_key'


@app.route('/')
def drivers_list():
    search = request.args.get('search', '')
    team_id = request.args.get('team_id', '')

    query = "SELECT d.*, t.team_name FROM drivers d LEFT JOIN teams t ON d.team_id = t.team_id WHERE 1=1"
    params = []

    if search:
        query += " AND d.full_name ILIKE %s"
        params.append(f'%{search}%')
    if team_id:
        query += " AND d.team_id = %s"
        params.append(team_id)

    drivers = execute_query(query, params, fetch=True)
    teams = execute_query("SELECT * FROM teams", fetch=True)
    return render_template('drivers.html', drivers=drivers, teams=teams)


@app.route('/dashboard')
def dashboard():
    stats = execute_query("SELECT * FROM view_team_standings", fetch=True)

    top_drivers = execute_query("""
        SELECT d.full_name, SUM(rr.points_earned) as total_points 
        FROM drivers d 
        JOIN race_results rr ON d.driver_id = rr.driver_id 
        GROUP BY d.full_name ORDER BY total_points DESC LIMIT 5
    """, fetch=True)

    return render_template('dashboard.html', stats=stats, top_drivers=top_drivers)



@app.route('/submit_result', methods=['POST'])
def submit_result():
    race_id = request.form.get('race_id')
    driver_id = request.form.get('driver_id')
    position = request.form.get('position')
    points = request.form.get('points')

    car_data = execute_query(
        "SELECT car_id FROM cars WHERE team_id = (SELECT team_id FROM drivers WHERE driver_id = %s)", (driver_id,),
        fetch=True)
    car_id = car_data[0]['car_id'] if car_data else None

    try:
        query = """
                INSERT INTO race_results (race_id, driver_id, car_id, position, points_earned)
                VALUES (%s, %s, %s, %s, %s)
                """
        execute_query(query, (race_id, driver_id, car_id, position, points))
        flash(f'Результат успешно добавлен!')
    except Exception as e:
        flash(f'Ошибка: {e}')

    return redirect(url_for('race_results_history'))


@app.route('/admin/add_result')
def add_result_page():
    races = execute_query("SELECT race_id, race_name FROM races ORDER BY race_date DESC", fetch=True)

    drivers = execute_query("""
        SELECT d.driver_id, d.full_name, d.driver_number, c.car_id 
        FROM drivers d 
        JOIN cars c ON d.team_id = c.team_id
    """, fetch=True)

    return render_template('results_entry.html', races=races, drivers=drivers)


@app.route('/admin/circuits', methods=['GET', 'POST'])
def circuits():
    if request.method == 'POST':
        name = request.form.get('name')
        country = request.form.get('country')
        length = request.form.get('length')

        if name and country and length:
            execute_query("""
                INSERT INTO circuits (circuit_name, country, length_km) 
                VALUES (%s, %s, %s)
            """, (name, country, length))
            flash(f'Трасса {name} добавлена в календарь!')
        return redirect(url_for('circuits'))

    all_circuits = execute_query("SELECT * FROM circuits ORDER BY circuit_name", fetch=True)
    return render_template('circuits.html', circuits=all_circuits)


@app.route('/admin/races', methods=['GET', 'POST'])
def manage_races():
    if request.method == 'POST':
        race_name = request.form.get('race_name')
        circuit_id = request.form.get('circuit_id')
        race_date = request.form.get('race_date')

        if race_name and circuit_id and race_date:
            execute_query("""
                INSERT INTO races (race_name, circuit_id, race_date) 
                VALUES (%s, %s, %s)
            """, (race_name, circuit_id, race_date))
            flash(f'Гонка {race_name} добавлена в календарь!')
        return redirect(url_for('manage_races'))

    circuits = execute_query("SELECT circuit_id, circuit_name FROM circuits", fetch=True)
    races = execute_query("""
        SELECT r.race_name, r.race_date, c.circuit_name 
        FROM races r 
        JOIN circuits c ON r.circuit_id = c.circuit_id 
        ORDER BY r.race_date DESC
    """, fetch=True)

    return render_template('races.html', circuits=circuits, races=races)

@app.route('/admin/teams', methods=['GET', 'POST'])
def manage_teams():
    if request.method == 'POST':
        data = (request.form['name'], request.form['city'], request.form['budget'])
        execute_query("INSERT INTO teams (team_name, base_city, budget_cap) VALUES (%s, %s, %s)", data)
        flash('Команда добавлена!')

    teams = execute_query("SELECT * FROM teams", fetch=True)
    return render_template('teams.html', teams=teams)


@app.route('/admin/drivers', methods=['GET', 'POST'])
def manage_drivers():
    if request.method == 'POST':
        data = (request.form['name'], request.form['team_id'], request.form['number'], request.form['salary'])
        execute_query("INSERT INTO drivers (full_name, team_id, driver_number, salary) VALUES (%s, %s, %s, %s)", data)
        flash('Пилот зарегистрирован!')

    drivers = execute_query("""
        SELECT d.*, t.team_name 
        FROM drivers d 
        JOIN teams t ON d.team_id = t.team_id
    """, fetch=True)
    teams = execute_query("SELECT * FROM teams", fetch=True)
    return render_template('drivers_admin.html', drivers=drivers, teams=teams)

@app.route('/results')
def race_results_history():
    query = """
        SELECT 
            r.race_name, 
            r.race_date,
            d.full_name as driver_name, 
            d.driver_number,
            t.team_name,
            c.model_name as car_model,
            rr.position, 
            rr.points_earned
        FROM race_results rr
        JOIN races r ON rr.race_id = r.race_id
        JOIN drivers d ON rr.driver_id = d.driver_id
        JOIN teams t ON d.team_id = t.team_id
        JOIN cars c ON rr.car_id = c.car_id
        ORDER BY r.race_date DESC, rr.position ASC
    """
    results = execute_query(query, fetch=True)
    return render_template('race_results.html', results=results)

@app.route('/driver/<int:driver_id>')
def driver_stats(driver_id):
    driver_info = execute_query("""
        SELECT d.*, t.team_name, c.model_name as car_model
        FROM drivers d
        JOIN teams t ON d.team_id = t.team_id
        LEFT JOIN cars c ON c.team_id = t.team_id
        WHERE d.driver_id = %s
    """, (driver_id,), fetch=True)

    if not driver_info:
        flash("Пилот не найден")
        return redirect(url_for('shop'))

    race_history = execute_query("""
        SELECT r.race_name, r.race_date, rr.position, rr.points_earned
        FROM race_results rr
        JOIN races r ON rr.race_id = r.race_id
        WHERE rr.driver_id = %s
        ORDER BY r.race_date DESC
    """, (driver_id,), fetch=True)

    summary = execute_query("""
        SELECT 
            COUNT(*) as total_starts,
            SUM(points_earned) as total_points,
            COUNT(CASE WHEN position = 1 THEN 1 END) as wins,
            COUNT(CASE WHEN position <= 3 THEN 1 END) as podiums
        FROM race_results
        WHERE driver_id = %s
    """, (driver_id,), fetch=True)

    return render_template('driver_stats.html',
                           driver=driver_info[0],
                           history=race_history,
                           summary=summary[0])



if __name__ == '__main__':
    app.run(debug=True, port=5001)