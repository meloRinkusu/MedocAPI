#from sqlalchemy import create_engine
#engine = create_engine("sqlite:///database.db")

import sqlite3
import csv

def create_patient():
    query = "CREATE TABLE IF NOT EXISTS Patient (\
      ID_PATIENT INTEGER PRIMARY KEY,\
      age INTEGER NOT NULL,\
      sexe INTEGER NOT NULL,\
      poids INTEGER NOT NULL,\
      allergies INTEGER,\
      prescriptions INTEGER,\
      FOREIGN KEY(allergies) REFERENCES Element(ID_ELEMENT),\
      FOREIGN KEY(prescriptions) REFERENCES Prescription(ID_PRESC)\
    );"
    return query

def create_medicament():
    query = "CREATE TABLE IF NOT EXISTS Medicament (\
      ID_MEDIC INTEGER PRIMARY KEY,\
      denomination TEXT NOT NULL,\
      voie TEXT NOT NULL\
    );"
    return query

def create_element():
    query = "CREATE TABLE IF NOT EXISTS Element (\
      ID_ELEMENT INTEGER PRIMARY KEY,\
      ID_MEDIC INTEGER NOT NULL,\
      designation TEXT,\
      dosage TEXT NOT NULL,\
      FOREIGN KEY (ID_MEDIC) REFERENCES Medicament(ID_MEDIC)\
    );"
    return query

def create_prescription():
    query = "CREATE TABLE IF NOT EXISTS Prescription (\
      ID_PRESC INTEGER PRIMARY KEY,\
      medicaments INTEGER NOT NULL,\
      date DATE NOT NULL,\
      FOREIGN KEY (medicaments) REFERENCES Medicament(ID_MEDIC)\
    );"
    return query


    
def drop_medicament():
    query = "DROP TABLE IF EXISTS Medicament;"
    return query

def drop_element():
    query = "DROP TABLE IF EXISTS Element;"
    return query

def get_data_Medicament():
    with open("CIS_bdpm.txt", "r") as source:
        reader = csv.reader(source, delimiter="\t")
        medicament_to_db = [(r[0], r[1], r[3]) for r in reader]
    return medicament_to_db

def number_of_lines():
    with open("CIS_COMPO_bdpm.txt", "r") as source:        
        reader = csv.reader(source, delimiter="\t")
        return sum(1 for line in reader)
    
def get_data_Element():
    row_count = number_of_lines()
    ID_ELEMENT = list(range(0,row_count,1))
    with open("CIS_COMPO_bdpm.txt", "r") as source:
        reader = csv.reader(source, delimiter="\t")
        elements = [([r[0], r[3], r[4]]) for r in reader]
    element_to_db = []
    for i in range(row_count):
        element_to_db.append((ID_ELEMENT[i], elements[i][0], elements[i][1], elements[i][2]))
    return element_to_db
    
    
def update_all():  
    medicament_to_db = get_data_Medicament()
    element_to_db = get_data_Element()
    con = sqlite3.connect('database.db')
    cur = con.cursor()
    con.execute(drop_medicament())
    con.execute(drop_element())
    con.execute(create_medicament())
    con.execute(create_element())
    #cur.execute("DELETE FROM Medicament;")
    #cur.execute("DELETE FROM Element;")
    cur.executemany("INSERT INTO Medicament ('ID_MEDIC', 'denomination', 'voie') VALUES (?, ?, ?);", medicament_to_db)
    #con.commit()
    cur.executemany("INSERT INTO Element ('ID_ELEMENT', 'ID_MEDIC', 'designation', 'dosage') VALUES (?, ?, ?, ?);", element_to_db)
    con.commit()
    con.close()

    
update_all()



