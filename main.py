from flask import Flask, render_template, request, redirect
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
import mysql.connector
from config import DB_CONFIG

app = Flask(__name__)

def get_db_connection():
    return mysql.connector.connect(**DB_CONFIG)

def sql_query(query, *vars) -> any:
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute(query, (vars))

    results = cursor.fetchall()

    cursor.close()
    conn.close()

    return results

@app.route('/animals')
def animals():

    query = """
    SELECT a.animalName, s.animalSpecies, b.animalBreed, a.animalRescueDate,f.fosterCarerFirstName, f.fosterCarerLastName, ads.adoptionStatus
	FROM animal a
		INNER JOIN species s ON a.idanimal = s.idspecies
		INNER JOIN breed b ON a.idanimal = b.idbreed
		INNER JOIN fosterCarer f ON a.idanimal = f.idfosterCarer
        INNER JOIN adoptionInfo ai ON a.adoptionStatus_idadoptionInfo = ai.idadoptionInfo
        INNER JOIN adoptionStatus ads ON ai.adoptionStatus_idadoptionStatus = ads.idadoptionStatus
    """
    animals = sql_query(query)

    if animals:
        return render_template("animals.html", animals=animals)


@app.route('/home')
def home():
    return render_template('home.html')

if __name__ == "__main__":
    app.run(debug=True)
