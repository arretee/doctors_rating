# The Firebase Admin SDK to access Cloud Firestore.
import firebase_admin

from firebase_admin import initialize_app, firestore, credentials, db

export = "doctor-rating-token.json"
cred = credentials.Certificate(export)
firebase_admin.initialize_app(cred)

# Initialize Firestore DB
db = firestore.client()

#Initialize Collection Reference for doctors
doc_ref = db.collection("doctors")
docs = doc_ref.get()

# Initialize Collection Reference for users
user_ref = db.collection("users")
users = user_ref.get()


#CRUD for doctors

#Create a new doctor
def create_doctor(doc):
    """Create a new doctor document in a collection of doctors in firestore

    Args:
        name (string): name of a doctor
        gender (boolean): True - male, False - female
        area (string): (North, South, West, East) of a country
        specialization (string): get spec from a list of doctors_specs
        start_work_year (int): start year of job
        ratings (dict): dictionary of users and their ratings for a doctor. {"user_name": array of ratings (from 0 - 3)}
    """
    doc_ref.add({
        "name": doc["name"],
        "gender": doc["gender"],
        "area": doc["area"],
        "specialization": doc["specialization"],
        "start_work_year": doc["start_work_year"],
        "ratings": doc["ratings"]
    })


#Read a doctor by ID
def get_doctor(doctor_id):
    """find doctor by his id in firestore

    Args:
        doctor_id (int): doctor id in firestore

    Returns:
        dict: The doctor document as a dictionary, or None if not found
    """
    doc = doc_ref.document(doctor_id).get()
    if doc.exists:
        return doc.to_dict()
    else:
        return None


def get_all_doctors():
    """get all doctors from firestore

    Returns:
        list: A list of all doctor documents as dictionaries
    """
    docs = doc_ref.get()
    return [doc.to_dict() for doc in docs]


#Read all doctors in collection
def get_all_doctors_rates():
    """get all doctors from firestore

    Returns:
        list: A list of all doctor documents as dictionaries
    """
    docs_list = []

    docs = doc_ref.get()
    for doc in docs:
        len_rates = 0
        avg_feeling = 0
        avg_professionalism = 0
        avg_price = 0
        avg_wait_time = 0

        doc_ratings = doc.to_dict().get("ratings")
        user_rates = doc_ratings.values()

        for rate in user_rates:
            avg_feeling += rate[0]
            avg_professionalism += rate[1]
            avg_price += rate[2]
            avg_wait_time += rate[3]
            len_rates += 1
            
        avg_feeling = round(avg_feeling / len_rates, 1)
        avg_professionalism = round(avg_professionalism / len_rates, 1)
        avg_price = round(avg_price / len_rates, 1)
        avg_wait_time = round(avg_wait_time / len_rates, 1)
        

        if len_rates > 0:
            docs_list.append({
                "name" : doc.to_dict().get("name"),
                "specialization": doc.to_dict().get("specialization"),
                "overall_rating": round((avg_feeling + avg_wait_time + avg_professionalism + avg_price) / 4, 1),
                "feeling": avg_feeling,
                "professionalism": avg_professionalism,
                "price": avg_price,
                "time_wait": avg_wait_time
            })
            
        else:
            docs_list.append({
                "name" : doc["name"],
                "specialization": doc["specialization"],
                "overall_rating": "N/R",
                "feeling": "N/R",
                "professionalism": "N/R",
                "price": "N/R",
                "time_wait": "N/R"
            })

    return docs_list



#Update a doctor by ID
def update_doctor(doctor_id, name, gender, area, specialization, start_work_year, ratings):
    """update doctor`s data

     Args:
            name (string): name of a doctor
            gender (boolean): True - male, False - female
            area (string): (North, South, West, East) of a country
            specialization (string): get spec from a list of doctors_specs
            start_work_year (int): start year of job
            ratings (dict): dictionary of users and their ratings for a doctor. {"user_name": array of ratings (from 0 - 3)}
        """
    doc_ref.document(doctor_id).update({
        "name": name,
        "gender": gender,
        "area": area,
        "specialization": specialization,
        "start_work_year": start_work_year,
        "ratings": ratings
    })


def add_doctor_votes(doctor_name, user_name, rates):
    doc = find_doctor_by_name(doctor_name).to_dict()
    doc["ratings"][user_name] = rates
    delete_doctor(doc_ref.where("name", "==", doctor_name).get()[0].id)
    create_doctor(doc)


def find_doctor_by_name(doctor_name):
    doc = doc_ref.where("name", "==", doctor_name).get()
    if not doc:
        return None
    return doc[0]


#Delete a doctor by ID
def delete_doctor(doctor_id):
    """delete doctor by his id

    Args:
        doctor_id (int): doctor id
    """
    doc_ref.document(doctor_id).delete()




#CRUD for users collection

#Create a new user
def create_user(name, password):
    """create new user in firestore

    Args:
        name (string): user name
        password (string): user password
    """
    user_ref.add({
        "name": name,
        "password": password
    })

#Read a user by ID
def get_user(user_id):
    """get user from firestore by his id

    Args:
        user_id (int): user id in firestore

    Returns:
        dict: The user document as a dictionary, or None if not found
    """
    user = user_ref.document(user_id).get()
    if user.exists:
        return user.to_dict()
    else:
        return None

#Read users in collection
def get_users():
    """get all users from firestore

    Returns:
        list: A list of user documents from firestore
    """
    users = user_ref.get()
    return [user.to_dict() for user in users]

#Update a user by ID
def update_user(user_id, name, password):
    """Update user id by his id

    Args:
        user_id (int): user id in firestore
        name (string): user name
        password (string): user password
    """
    user_ref.document(user_id).update({
        "name": name,
        "password": password
    })

#Delete a user by ID
def delete_user(user_id):
    """delete user by his id

    Args:
        user_id (int): user id in firestore
    """
    user_ref.document(user_id).delete()

#Find user by name
def find_user_by_name(name):
    """Find user by his name in firestore

    Args:
        name (string): user name

    Returns:
        dict: user document as dict, None if not found
    """
    user = user_ref.where("name", "==", name).get()
    if not user:
        return None
    return user[0].to_dict()


#Check if user has rated a doctor
def is_user_rated(user_name, doctor_id):
    """Check if user rated some specific doctor

    Args:
        user_name (string): user name
        doctor_id (int): need to find doctor

    Returns:
        bool: if user rated some doctor returns True, else False
    """
    user = find_user_by_name(user_name)
    if len(user) == 0:
        return False
    user_name = user[0].get("name")

    doctor = get_doctor(doctor_id)
    doctor_ratings = doctor.get("ratings")

    for rating in doctor_ratings.keys():
        print(f"User ID: {user_name}, Rating: {rating}")
        if user_name == rating:
            return True
        
    return False


#Find doctors by specialization
def get_doctor_by_specialization(specialization):
    """Find user by his spec

    Args:
        specialization (string): doctor specialization

    Returns:
        list: A list of doctor documents from firestore, else None if no doctors found
    """
    doctors = doc_ref.where("specialization", "==", specialization).get()
    if doctors:
        return [doctor.to_dict() for doctor in doctors]
    return None
