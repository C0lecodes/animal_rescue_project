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

def get_animal_data(all=True, id=None):
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
    """
    if all == False:
        query += 'WHERE a.idanimal = %s;'

    if id:
        cursor.execute(query, (id,))
    else:
        cursor.execute(query)

    results = cursor.fetchall() if all else cursor.fetchone()

    cursor.close()
    conn.close()

    return results

@app.route('/')
def route_home():
    return redirect('/home')

@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/animals')
def animals():
    animals = get_animal_data()

    if animals:
        return render_template("animals.html", animals=animals)
    
@app.route('/animal/<int:id>', methods=['GET'])
def animal(id):
    animal = get_animal_data(False, id)

    try:
            conn = get_db_connection()
            cursor = conn.cursor(dictionary=True)
            query = """
                SELECT a.treatment, b.vetName
                FROM treatments t
                INNER JOIN treatment a ON t.treatment_idtreatment = a.idtreatment
                INNER JOIN vet b ON t.vet_idvet = b.idvet
                WHERE t.animal_idanimal = %s

                    """
            cursor.execute(query,(id,))
            treatments = cursor.fetchall()
            cursor.close()
            conn.close()
            return render_template('animal.html', animal=animal, treatments=treatments)

    except Exception as e:
            conn.rollback()
            print("DATABASE ERROR:", e)
            return str(e), 500

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

@app.route('/add_vet', methods=['GET', 'POST'])
def add_vet():
    if request.method == 'POST':
        vet = request.form['vet']

        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            query = """
                INSERT INTO vet (vetName)
                VALUES (%s);
                    """
            
            cursor.execute(query, (vet,))
            conn.commit()
            cursor.close()
            conn.close()

            return redirect('/home')
        except Exception as e:
            error = str(e)
            print(error)
    return render_template('add_vet.html')

@app.route('/add_treatment', methods=['GET', 'POST'])
def add_treatment():
    if request.method == 'POST':
        treatment = request.form['treatment']

        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            query = """
                INSERT INTO treatment (treatment)
                VALUES (%s);
                    """
            
            cursor.execute(query, (treatment,))
            conn.commit()
            cursor.close()
            conn.close()

            return redirect('/home')
        except Exception as e:
            error = str(e)
            print(error)
    return render_template('add_treatment.html')

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
        animal = get_animal_data(False, id)

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

@app.route('/add_animal_treatment/<int:id>', methods=['GET','POST'])
def add_animal_treatment(id):

    if request.method == "POST":
        treatment = request.form["treatment"]
        vet = request.form["vet"]
        animal_id = id
        print(treatment, vet, id)

        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            query = """
                INSERT INTO treatments (treatment_idtreatment, vet_idvet, animal_idanimal) 
                VALUE (%s, %s, %s);
                    """
            cursor.execute(query, (treatment, vet, animal_id,))

            conn.commit()
            cursor.close()
            conn.close()

            return redirect(f'/animal/{id}')
        except Exception as e:
            conn.rollback()
            print("DATABASE ERROR:", e)
            return str(e), 500

    treatments = sql_get_query("SELECT * FROM treatment")
    vets = sql_get_query("SELECT * FROM vet")
    print(treatments, vets)

    return render_template(
        'add_animal_treatment.html',
        treatments=treatments,
        vets=vets
    )

if __name__ == "__main__":
    app.run(debug=True)
