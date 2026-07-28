import sqlite3 as sql

def createDB_CLINICA():
    conn = sql.connect("Clinica.db")
    conn.commit()
    conn.close()

def createTable_CLINICA():
    conn = sql.connect("Clinica.db")
    cursor = conn.cursor()
    cursor.execute(
        """CREATE TABLE IF NOT EXISTS clinica (
        ID INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        lastName TEXT,
        age INTEGER,
        CI INTEGER,
        entryDate TEXT,
        phoneNumber TEXT,
        home TEXT,
        representName TEXT,
        representCI INTEGER,
        consultReason TEXT,
        presentIssues TEXT
        )
        """
    )
    conn.commit()
    conn.close()

def createRow_CLINICA(name, lastName, age, CI, entryDate, phoneNumber, home, representName, representCI, consultReason, presentIssues):
    conn = sql.connect("Clinica.db")
    try:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO clinica (name, lastName, age, CI, entryDate, phoneNumber, home, representName, representCI, consultReason, presentIssues) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                        (name, lastName, age, CI, entryDate, phoneNumber, home, representName, representCI, consultReason, presentIssues)
                        )
        conn.commit()
    except sql.Error as e:
        conn.rollback()
        raise e
    finally:
        conn.close()

def readTable_CLINICA():
    conn = sql.connect("Clinica.db")
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM clinica")
        rows = cursor.fetchall()
        return rows
    finally:
        conn.close()

def updateRow_CLINICA(id, name, lastName, age, CI, entryDate, phoneNumber, home, representName, representCI, consultReason, presentIssues):
    conn = sql.connect("Clinica.db")
    try:
        cursor = conn.cursor()
        cursor.execute("UPDATE clinica SET name = ?, lastName = ?, age = ?, CI = ?, entryDate = ?, phoneNumber = ?, home = ?, representName = ?, representCI = ?, consultReason = ?, presentIssues = ? WHERE ID = ?",
                        (name, lastName, age, CI, entryDate, phoneNumber, home, representName, representCI, consultReason, presentIssues, id))
        conn.commit()
    except sql.Error as e:
        conn.rollback()
        raise e
    finally:
        conn.close()

def deleteRow_CLINICA(id):
    conn = sql.connect("Clinica.db")
    try:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM clinica WHERE ID = ?", (id,))
        conn.commit()
    except sql.Error as e:
        conn.rollback()
        raise e
    finally:
        conn.close()

def createDB_ANTECEDENTES():
    conn = sql.connect("Clinica.db")
    conn.commit()
    conn.close()

def createTable_ANTECEDENTES():
    conn = sql.connect("Clinica.db")
    cursor = conn.cursor()
    cursor.execute(
        """CREATE TABLE IF NOT EXISTS antecedentes_personales (
    ID INTEGER PRIMARY KEY AUTOINCREMENT,
    patientID INTEGER UNIQUE,
    earNoseThroat TEXT,
    respiratory TEXT,
    allergy TEXT,
    cardiovascular TEXT,
    gastrointestinal TEXT,
    endocrine TEXT,
    renal TEXT,
    hepatic TEXT,
    neurologic TEXT,
    neoplastic TEXT,
    blood TEXT,
    viral TEXT,
    gynecologic TEXT,
    covid TEXT,
    hiv TEXT,
    surgeries TEXT,
    medications TEXT,
    hepatitisVaccine TEXT,
    covidVaccine TEXT,
    familyHistory TEXT,
    FOREIGN KEY (patientID) REFERENCES clinica(ID)
)
        """
    )
    conn.commit()
    conn.close()

def createRow_ANTECEDENTES(patientID, earNoseThroat, respiratory, allergy, cardiovascular, gastrointestinal, endocrine, renal, hepatic, neurologic, neoplastic, blood, viral, gynecologic, covid, hiv, surgeries, medications, hepatitisVaccine, covidVaccine, familyHistory):
    conn = sql.connect("Clinica.db")
    try:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO antecedentes_personales (patientID, earNoseThroat, respiratory, allergy, cardiovascular, gastrointestinal, endocrine, renal, hepatic, neurologic, neoplastic, blood, viral, gynecologic, covid, hiv, surgeries, medications, hepatitisVaccine, covidVaccine, familyHistory) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                        (patientID, earNoseThroat, respiratory, allergy, cardiovascular, gastrointestinal, endocrine, renal, hepatic, neurologic, neoplastic, blood, viral, gynecologic, covid, hiv, surgeries, medications, hepatitisVaccine, covidVaccine, familyHistory)
                        )
        conn.commit()
    except sql.Error as e:
        conn.rollback()
        raise e
    finally:
        conn.close()

def readTable_ANTECEDENTES():
    conn = sql.connect("Clinica.db")
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM antecedentes_personales")
        rows = cursor.fetchall()
        return rows
    finally:
        conn.close()

def updateRow_ANTECEDENTES(patientID, earNoseThroat, respiratory, allergy, cardiovascular, gastrointestinal, endocrine, renal, hepatic, neurologic, neoplastic, blood, viral, gynecologic, covid, hiv, surgeries, medications, hepatitisVaccine, covidVaccine, familyHistory):
    conn = sql.connect("Clinica.db")
    try:
        cursor = conn.cursor()
        cursor.execute("UPDATE antecedentes_personales SET earNoseThroat = ?, respiratory = ?, allergy = ?, cardiovascular = ?, gastrointestinal = ?, endocrine = ?, renal = ?, hepatic = ?, neurologic = ?, neoplastic = ?, blood = ?, viral = ?, gynecologic = ?, covid = ?, hiv = ?, surgeries = ?, medications = ?, hepatitisVaccine = ?, covidVaccine = ?, familyHistory = ? WHERE patientID = ?",
                        (earNoseThroat, respiratory, allergy, cardiovascular, gastrointestinal, endocrine, renal, hepatic, neurologic, neoplastic, blood, viral, gynecologic, covid, hiv, surgeries, medications, hepatitisVaccine, covidVaccine, familyHistory, patientID))
        conn.commit()
    except sql.Error as e:
        conn.rollback()
        raise e
    finally:
        conn.close()

def deleteRow_ANTECEDENTES(patientID):
    conn = sql.connect("Clinica.db")
    try:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM antecedentes_personales WHERE patientID = ?", (patientID,))
        conn.commit()
    except sql.Error as e:
        conn.rollback()
        raise e
    finally:
        conn.close()

def createTable_EXAMEN():
    conn = sql.connect("Clinica.db")
    cursor = conn.cursor()
    cursor.execute(
        """CREATE TABLE IF NOT EXISTS examen_fisico (
    ID INTEGER PRIMARY KEY AUTOINCREMENT,
    patientID INTEGER UNIQUE,
    extraoral TEXT,
    intraoralTB TEXT,
    intraoralTD TEXT,
    periodontal TEXT,
    PA TEXT,
    FOREIGN KEY (patientID) REFERENCES clinica(ID)
)
        """
    )
    conn.commit()
    conn.close()

def createRow_EXAMEN(patientID, extraoral, intraoralTB, intraoralTD, periodontal, PA):
    conn = sql.connect("Clinica.db")
    try:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO examen_fisico (patientID, extraoral, intraoralTB, intraoralTD, periodontal, PA) VALUES (?, ?, ?, ?, ?, ?)",
                        (patientID, extraoral, intraoralTB, intraoralTD, periodontal, PA)
                        )
        conn.commit()
    except sql.Error as e:
        conn.rollback()
        raise e
    finally:
        conn.close()

def readTable_EXAMEN():
    conn = sql.connect("Clinica.db")
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM examen_fisico")
        rows = cursor.fetchall()
        return rows
    finally:
        conn.close()

def updateRow_EXAMEN(patientID, extraoral, intraoralTB, intraoralTD, periodontal, PA):
    conn = sql.connect("Clinica.db")
    try:
        cursor = conn.cursor()
        cursor.execute("UPDATE examen_fisico SET extraoral = ?, intraoralTB = ?, intraoralTD = ?, periodontal = ?, PA = ? WHERE patientID = ?",
                        (extraoral, intraoralTB, intraoralTD, periodontal, PA, patientID))
        conn.commit()
    except sql.Error as e:
        conn.rollback()
        raise e
    finally:
        conn.close()

def deleteRow_EXAMEN(patientID):
    conn = sql.connect("Clinica.db")
    try:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM examen_fisico WHERE patientID = ?", (patientID,))
        conn.commit()
    except sql.Error as e:
        conn.rollback()
        raise e
    finally:
        conn.close()

def createTable_ODONTOGRAMA():
    conn = sql.connect("Clinica.db")
    cursor = conn.cursor()
    cursor.execute(
        """CREATE TABLE IF NOT EXISTS odontograms (
    ID INTEGER PRIMARY KEY AUTOINCREMENT,
    patientID INTEGER,
    notes TEXT,
    FOREIGN KEY (patientID) REFERENCES clinica(ID)
)
        """
    )
    conn.commit()
    conn.close()

def createRow_ODONTOGRAMA(patientID, notes):
    conn = sql.connect("Clinica.db")
    try:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO odontograms (patientID, notes) VALUES (?, ?)",
                        (patientID, notes)
                        )
        conn.commit()
    except sql.Error as e:
        conn.rollback()
        raise e
    finally:
        conn.close()

def readTable_ODONTOGRAMA():
    conn = sql.connect("Clinica.db")
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM odontograms")
        rows = cursor.fetchall()
        return rows
    finally:
        conn.close()

def updateRow_ODONTOGRAMA(id, notes):
    conn = sql.connect("Clinica.db")
    try:
        cursor = conn.cursor()
        cursor.execute("UPDATE odontograms SET notes = ? WHERE ID = ?",
                        (notes, id))
        conn.commit()
    except sql.Error as e:
        conn.rollback()
        raise e
    finally:
        conn.close()

def deleteRow_ODONTOGRAMA(id):
    conn = sql.connect("Clinica.db")
    try:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM odontogram_details WHERE odontogramID = ?", (id,))
        cursor.execute("DELETE FROM odontograms WHERE ID = ?", (id,))
        conn.commit()
    except sql.Error as e:
        conn.rollback()
        raise e
    finally:
        conn.close()

def createTable_ODONTOGRAMA_DETAILS():
    conn = sql.connect("Clinica.db")
    cursor = conn.cursor()
    cursor.execute(
        """CREATE TABLE IF NOT EXISTS odontogram_details (
    ID INTEGER PRIMARY KEY AUTOINCREMENT,
    odontogramID INTEGER,
    tooth INTEGER,
    face TEXT,
    affected TEXT NOT NULL,
    description TEXT,
    FOREIGN KEY (odontogramID) REFERENCES odontograms(ID)
)
        """
    )
    conn.commit()
    conn.close()

def createRow_ODONTOGRAMA_DETAILS(odontogramID, tooth, face, affected, description):
    conn = sql.connect("Clinica.db")
    try:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO odontogram_details (odontogramID, tooth, face, affected, description) VALUES (?, ?, ?, ?, ?)",
                        (odontogramID, tooth, face, affected, description)
                        )
        conn.commit()
    except sql.Error as e:
        conn.rollback()
        raise e
    finally:
        conn.close()

def readTable_ODONTOGRAMA_DETAILS():
    conn = sql.connect("Clinica.db")
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM odontogram_details")
        rows = cursor.fetchall()
        return rows
    finally:
        conn.close()

def readODONTOGRAMA_DETAILS(odontogramID):
    conn = sql.connect("Clinica.db")
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM odontogram_details WHERE odontogramID = ?", (odontogramID,))
        rows = cursor.fetchall()
        return rows
    finally:
        conn.close()

def updateRow_ODONTOGRAMA_DETAILS(id, tooth, face, affected, description):
    conn = sql.connect("Clinica.db")
    try:
        cursor = conn.cursor()
        cursor.execute("UPDATE odontogram_details SET tooth = ?, face = ?, affected = ?, description = ? WHERE ID = ?",
                        (tooth, face, affected, description, id))
        conn.commit()
    except sql.Error as e:
        conn.rollback()
        raise e
    finally:
        conn.close()

def deleteRow_ODONTOGRAMA_DETAILS(id):
    conn = sql.connect("Clinica.db")
    try:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM odontogram_details WHERE ID = ?", (id,))
        conn.commit()
    except sql.Error as e:
        conn.rollback()
        raise e
    finally:
        conn.close()



if __name__ == "__main__":
    createDB_CLINICA()
    createTable_CLINICA()
    createTable_ANTECEDENTES()
    createTable_EXAMEN()
    createTable_ODONTOGRAMA()
    createTable_ODONTOGRAMA_DETAILS()
