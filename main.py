from flask import Flask, render_template, request, redirect, url_for
import mysql.connector
from config import DB_CONFIG

app = Flask(__name__)

def get_db_connection():
    """Opens connection to the database."""
    return mysql.connector.connect(**DB_CONFIG)

def sql_get_query(query, *vars) -> any:
    """Conducts a basic SQL query and returns the result."""
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    query += " ORDER BY 2 ASC"
    cursor.execute(query, vars)

    results = cursor.fetchall()

    cursor.close()
    conn.close()

    return results

def get_animal_data(all=True, id=None):
    """Retrieves all animal data or one animals data."""
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
        query += 'WHERE a.idanimal = %s'
    else:
        query += "ORDER BY 2 ASC;"

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
    """Redirects to home automatically."""
    return redirect('/home')

@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/animals')
def animals():
    """All animals display route."""
    animals = get_animal_data()

    if animals:
        return render_template("animals.html", animals=animals)
    
@app.route('/animal/<int:id>', methods=['GET'])
def animal(id):
    """Displays one animals information."""
    animal = get_animal_data(False, id)

    try:
            conn = get_db_connection()
            cursor = conn.cursor(dictionary=True)
            query = """
                SELECT t.idtreatments, a.treatment, b.vetName
                FROM treatments t
                INNER JOIN treatment a ON t.treatment_idtreatment = a.idtreatment
                INNER JOIN vet b ON t.vet_idvet = b.idvet
                WHERE t.animal_idanimal = %s

                    """
            cursor.execute(query,(id,))
            treatments = cursor.fetchall()
            query = """
                SELECT adoptionStatus_idadoptionInfo
                FROM animal
                WHERE idanimal = %s
                    """
            cursor.execute(query, (id,))
            adoption_id = cursor.fetchone()
            print(adoption_id)

            query = """
                SELECT adoptionInfoAdopterName
                FROM adoptionInfo
                WHERE idadoptionInfo = %s
                    """
            cursor.execute(query, (adoption_id['adoptionStatus_idadoptionInfo'],))
            adopter_name = cursor.fetchone()

            cursor.close()
            conn.close()
            return render_template('animal.html', animal=animal, treatments=treatments, adopter_name=adopter_name)

    except Exception as e:
            conn.rollback()
            print("DATABASE ERROR:", e)
            return str(e), 500

@app.route('/add_foster_carer', methods=['GET', 'POST'])
def add_foster_carer():
    """Handles adding a foster carer to the database."""
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

            return redirect('/foster_carers')
        except Exception as e:
            error = str(e)
    return render_template('add_foster_carer.html')

@app.route('/add_animal', methods=['GET', 'POST'])
def add_animal():
    """Handles adding an animal to the database."""
    if request.method == 'POST':
        name = request.form['first_name']
        rescue_date = request.form['rescue_date']
        species = request.form['species']
        breed = request.form['breed']
        adoption_status = request.form['adoption_status']
        foster_carer = request.form['foster_carer']
        adopter_name = request.form['adopter_name']

        if not adopter_name:
            adopter_name = None

        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            query = """
                INSERT INTO adoptionInfo (adoptionStatus_idadoptionStatus, adoptionInfoAdopterName) 
                VALUE (%s, %s);
                    """
            cursor.execute(query, (adoption_status, adopter_name,))

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
    """Handles adding a new breed to the database."""
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
    """Handles adding a new species to the database."""
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
    """Handles adding a new vet to the database."""
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

@app.route('/add_treatment/<int:animal_id>', methods=['GET', 'POST'])
def add_treatment(animal_id):
    """Handles adding a treatment for an animal to the database."""
    if request.method == 'POST':
        treatment = request.form['treatment']
        animal_id = animal_id

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

            return redirect(
                url_for('add_animal_treatment', id=animal_id)
)

        except Exception as e:
            error = str(e)
            print(error)
    return render_template('add_treatment.html')

@app.route('/delete_animal/<int:id>', methods=['POST'])
def delete_animal(id):
    """Deletes an animal."""
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM animal WHERE idanimal = %s", (id,))
    conn.commit()

    cursor.close()
    conn.close()

    return redirect('/animals')

@app.route('/delete_animal_treatment/<int:id>/<int:post_id>', methods=['POST'])
def delete_animal_treatment(id, post_id):
    """Deletes a treatment attached to an animal."""
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM treatments WHERE idtreatments = %s", (id,))
    conn.commit()

    cursor.close()
    conn.close()

    return redirect(f'/animal/{post_id}')

@app.route('/edit_animal/<int:id>', methods=['GET','POST'])
def edit_animal(id):
    """Handles the edit animal process."""
    if request.method == 'POST':
        animalid = id
        name = request.form['first_name']
        rescue_date = request.form['rescue_date']
        species = request.form['species']
        breed = request.form['breed']
        adoption_status = request.form['adoption_status']
        foster_carer = request.form['foster_carer']
        adopter_name = request.form['adopter_name']

        if not adopter_name:
            adopter_name = None

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
            SET adoptionStatus_idadoptionStatus = %s,
            adoptionInfoAdopterName = %s
            WHERE idadoptionInfo = %s;
            """
            cursor.execute(query, (adoption_status, adopter_name, adoption_info_id,))
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

        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        query = """
            SELECT adoptionStatus_idadoptionInfo
            FROM animal
            WHERE idanimal = %s
                """
        cursor.execute(query, (id,))
        adoption_id = cursor.fetchone()

        query = """
            SELECT adoptionInfoAdopterName
            FROM adoptionInfo
            WHERE idadoptionInfo = %s
                """
        cursor.execute(query, (adoption_id['adoptionStatus_idadoptionInfo'],))
        adopter_name = cursor.fetchone()


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
        current_attributes=animal,
        adopter_name=adopter_name
    )

@app.route('/add_animal_treatment/<int:id>', methods=['GET','POST'])
def add_animal_treatment(id):
    """Allows an animal to be added to the database."""
    if request.method == "POST":
        treatment = request.form["treatment"]
        vet = request.form["vet"]
        animal_id = id

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

    return render_template(
        'add_animal_treatment.html',
        treatments=treatments,
        vets=vets,
        animal_id=id
    )

@app.route('/add_volunteer', methods=['GET', 'POST'])
def add_volunteer():
    """Allows a new volunteer to be added to the database."""
    if request.method == 'POST':
        first_name = request.form["first_name"]
        last_name = request.form["last_name"]
        shift_day = request.form["shift_day"]

        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            query = """
                INSERT INTO volunteer (volunteerFirstName, volunteerLastName, volunteerShiftDay) 
                VALUE (%s, %s, %s);
                    """
            cursor.execute(query, (first_name, last_name, shift_day,))

            conn.commit()
            cursor.close()
            conn.close()

            return redirect('/volunteers')
        except Exception as e:
            conn.rollback()
            print("DATABASE ERROR:", e)
            return str(e), 500
        
    return render_template('add_volunteer.html')

@app.route('/volunteers', methods=['GET'])
def volunteers():
    """Displays all the volunteer data."""
    volunteers = sql_get_query("SELECT * FROM volunteer")
    
    if volunteers:
        return render_template('volunteers.html', volunteers=volunteers)

@app.route('/foster_carers')
def foster_carers():
    """Displays all the foster carer data."""
    foster_carers = sql_get_query("SELECT * FROM fosterCarer")

    if foster_carers:
        return render_template('foster_carers.html', foster_carers=foster_carers)
    
@app.route('/vets')
def vets():
    """Displays all the vet data."""
    vets = sql_get_query("SELECT * FROM vet")

    if vets:
        return render_template('vets.html', vets=vets)

if __name__ == "__main__":
    app.run(debug=True)
