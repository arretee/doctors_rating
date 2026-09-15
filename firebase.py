# The Firebase Admin SDK to access Cloud Firestore.
import firebase_admin

from firebase_admin import initialize_app, firestore, credentials, db
import google.cloud.firestorer


export = "/home/pinqwiny/doctors_rating/doctor-rating-token.json"
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
def create_doctor(name, gender, area, specialization, start_work_year, ratings):
    doc_ref.add({
        "name": name,
        "gender": gender,
        "area": area,
        "specialization": specialization,
        "start_work_year": start_work_year,
        "ratings": ratings
    })


#Read a doctor by ID
def get_doctor(doctor_id):
    doc = doc_ref.document(doctor_id).get()
    if doc.exists:
        return doc.to_dict()
    else:
        return None


#Read all doctors in collection
def get_all_doctors():
    docs = doc_ref.get()
    return [doc.to_dict() for doc in docs]


#Update a doctor by ID
def update_doctor(doctor_id, name, gender, area, specialization, start_work_year, ratings):
    doc_ref.document(doctor_id).update({
        "name": name,
        "gender": gender,
        "area": area,
        "specialization": specialization,
        "start_work_year": start_work_year,
        "ratings": ratings
    })


#Delete a doctor by ID
def delete_doctor(doctor_id):
    doc_ref.document(doctor_id).delete()



#CRUD for users collection

#Create a new user
def create_user(name, password):
    user_ref.add({
        "name": name,
        "password": password
    })

#Read a user by ID
def get_user(user_id):
    user = user_ref.document(user_id).get()
    if user.exists:
        return user.to_dict()
    else:
        return None

#Read users in collection
def get_users():
    users = user_ref.get()
    return [user.to_dict() for user in users]

#Update a user by ID
def update_user(user_id, name, password):
    user_ref.document(user_id).update({
        "name": name,
        "password": password
    })

#Delete a user by ID
def delete_user(user_id):
    user_ref.document(user_id).delete()


def find_user_by_name(name):
    user = user_ref.where("name", "==", name).get()
    return user


def is_user_rated(user_name, doctor_id):
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


def get_doctor_by_specialization(specialization):
    doctors = doc_ref.where("specialization", "==", specialization).get()
    if doctors:
        return [doctor.to_dict() for doctor in doctors]
    return None
