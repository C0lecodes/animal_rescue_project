from flask import Flask, render_template, request, redirect, url_for
import mysql.connector
from config import DB_CONFIG

app = Flask(__name__)

def get_db_connection():
    return mysql.connector.connect(**DB_CONFIG)

def sql_get_query(query, *vars) -> any:
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute(query, vars)

    results = cursor.fetchall()

    cursor.close()
    conn.close()

    return results

@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/animals')
def animals():

    query = """
    SELECT a.idanimal, a.animalName, s.animalSpecies, b.animalBreed, a.animalRescueDate,f.fosterCarerFirstName, f.fosterCarerLastName, ads.adoptionStatus
	FROM animal a
		INNER JOIN species s ON a.species_idspecies = s.idspecies
		INNER JOIN breed b ON a.breed_idbreed = b.idbreed
		INNER JOIN fosterCarer f ON a.fosterCarer_idfosterCarer = f.idfosterCarer
        INNER JOIN adoptionInfo ai ON a.adoptionStatus_idadoptionInfo = ai.idadoptionInfo
        INNER JOIN adoptionStatus ads ON ai.adoptionStatus_idadoptionStatus = ads.idadoptionStatus
    """
    animals = sql_get_query(query)

    if animals:
        return render_template("animals.html", animals=animals)
    
@app.route('/add_foster_carer', methods=['GET', 'POST'])
def add_foster_carer():
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        phone_number = request.form['phone_number']
        

        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            query = """
                INSERT INTO fosterCarer (fosterCarerFirstName, fosterCarerLastName, fosterCarerPhone)
                VALUES (%s, %s, %s);
                    """
            
            cursor.execute(query, (first_name, last_name, phone_number))
            conn.commit()
            cursor.close()
            conn.close()

            return redirect(request.referrer or url_for('home'))
        except Exception as e:
            error = str(e)
    return render_template('add_foster_carer.html')

@app.route('/add_animal', methods=['GET', 'POST'])
def add_animal():
    if request.method == 'POST':
        name = request.form['first_name']
        rescue_date = request.form['rescue_date']
        species = request.form['species']
        breed = request.form['breed']
        adoption_status = request.form['adoption_status']
        foster_carer = request.form['foster_carer']

        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            query = """
                INSERT INTO adoptionInfo (adoptionStatus_idadoptionStatus) 
                VALUE (%s);
                    """
            cursor.execute(query, (adoption_status,))

            adoption_info_id = cursor.lastrowid

            query = """
                INSERT INTO animal (animalName, animalRescueDate, species_idspecies, breed_idbreed, adoptionStatus_idadoptionInfo, fosterCarer_idfosterCarer) 
                VALUE (%s, %s, %s, %s, %s, %s);
                    """
            cursor.execute(query, (name, rescue_date, species, breed, adoption_info_id, foster_carer))

            conn.commit()
            cursor.close()
            conn.close()

            return redirect('/animals')
        except Exception as e:
            conn.rollback()
            print("DATABASE ERROR:", e)
            return str(e), 500

    breed_options = sql_get_query("SELECT * FROM breed")
    species_options = sql_get_query("SELECT * FROM species")
    status_options = sql_get_query("SELECT * FROM adoptionStatus")
    foster_options = sql_get_query("SELECT * FROM fosterCarer")

    return render_template(
        'add_animal.html',
        breed_options=breed_options,
        species_options=species_options,
        status_options=status_options,
        foster_options=foster_options
    )

@app.route('/add_breed', methods=['GET', 'POST'])
def add_breed():
    if request.method == 'POST':
        breed = request.form['breed']

        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            query = """
                INSERT INTO breed (animalBreed)
                VALUES (%s);
                    """
            
            cursor.execute(query, (breed,))
            conn.commit()
            cursor.close()
            conn.close()

            return redirect('/add_animal')
        except Exception as e:
            error = str(e)
            print(error)
    return render_template('add_breed.html')

@app.route('/add_species', methods=['GET', 'POST'])
def add_species():
    if request.method == 'POST':
        species = request.form['species']

        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            query = """
                INSERT INTO species (animalSpecies)
                VALUES (%s);
                    """
            
            cursor.execute(query, (species,))
            conn.commit()
            cursor.close()
            conn.close()

            return redirect('/add_animal')
        except Exception as e:
            error = str(e)
            print(error)
    return render_template('add_species.html')

@app.route('/delete_animal/<int:id>', methods=['POST'])
def delete_animal(id):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM animal WHERE idanimal = %s", (id,))
    conn.commit()

    cursor.close()
    conn.close()

    return redirect('/animals')


@app.route('/edit_animal/<int:id>', methods=['GET','POST'])
def edit_animal(id):

    if request.method == 'POST':
        animalid = id
        name = request.form['first_name']
        rescue_date = request.form['rescue_date']
        species = request.form['species']
        breed = request.form['breed']
        adoption_status = request.form['adoption_status']
        foster_carer = request.form['foster_carer']

        try:
            conn = get_db_connection()
            cursor = conn.cursor()

            query = """
                UPDATE animal 
                SET animalName = %s, 
                animalRescueDate = %s,
                species_idspecies = %s, 
                breed_idbreed = %s,
                fosterCarer_idfosterCarer = %s
                WHERE idanimal = %s;
                    """
            cursor.execute(query, (name, rescue_date, species, breed, foster_carer, animalid))
            conn.commit()

            query = """
            SELECT adoptionStatus_idadoptionInfo 
            FROM animal
            WHERE idanimal = %s
            """

            cursor.execute(query, (animalid,))
            adoption_info_id = cursor.fetchone()[0]

            query = """
            UPDATE adoptionInfo
            SET adoptionStatus_idadoptionStatus = %s
            WHERE idadoptionInfo = %s
            """
            cursor.execute(query, (adoption_status, adoption_info_id,))
            conn.commit()
            cursor.close()
            conn.close()

            return redirect('/animals')
        except Exception as e:
            conn.rollback()
            print("DATABASE ERROR:", e)
            return str(e), 500
    
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        
        query = """
        SELECT a.idanimal, a.animalName, s.animalSpecies, b.animalBreed, a.animalRescueDate,f.fosterCarerFirstName, f.fosterCarerLastName, ads.adoptionStatus
        FROM animal a
            INNER JOIN species s ON a.species_idspecies = s.idspecies
            INNER JOIN breed b ON a.breed_idbreed = b.idbreed
            INNER JOIN fosterCarer f ON a.fosterCarer_idfosterCarer = f.idfosterCarer
            INNER JOIN adoptionInfo ai ON a.adoptionStatus_idadoptionInfo = ai.idadoptionInfo
            INNER JOIN adoptionStatus ads ON ai.adoptionStatus_idadoptionStatus = ads.idadoptionStatus
        WHERE a.idanimal = %s;
        """

        cursor.execute(query, (id,))

        animal = cursor.fetchone()

    except Exception as e:
        error = str(e)
        print(error)

    breed_options = sql_get_query("SELECT * FROM breed")
    species_options = sql_get_query("SELECT * FROM species")
    status_options = sql_get_query("SELECT * FROM adoptionStatus")
    foster_options = sql_get_query("SELECT * FROM fosterCarer")

    return render_template(
        'edit_animal.html',
        breed_options=breed_options,
        species_options=species_options,
        status_options=status_options,
        foster_options=foster_options,
        current_attributes=animal
    )

if __name__ == "__main__":
    app.run(debug=True)
