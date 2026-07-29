import sqlite3 as sql
from contextlib import contextmanager

@contextmanager
def get_connection():
    conn = sql.connect("Clinica.db")
    conn.execute("PRAGMA foreign_keys = ON;")
    try:
        yield conn
    finally:
        conn.close()

def getConnection():
    conn = sql.connect("Clinica.db")
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn

def createTable_PACIENTES():
    conn = getConnection()
    cursor = conn.cursor()
    cursor.execute(
        """CREATE TABLE IF NOT EXISTS pacientes (
    patientID INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    lastName TEXT,
    age INTEGER,
    CI INTEGER UNIQUE,
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

def createRow_PACIENTES(name, lastName, age, CI, entryDate, phoneNumber, home, representName, representCI, consultReason, presentIssues):
    conn = getConnection()
    try:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO pacientes (name, lastName, age, CI, entryDate, phoneNumber, home, representName, representCI, consultReason, presentIssues) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                        (name, lastName, age, CI, entryDate, phoneNumber, home, representName, representCI, consultReason, presentIssues)
                        )
        conn.commit()
        return cursor.lastrowid
    except sql.Error as e:
        conn.rollback()
        raise e
    finally:
        conn.close()

def readTable_PACIENTES():
    conn = getConnection()
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM pacientes")
        rows = cursor.fetchall()
        return rows
    finally:
        conn.close()

def updateRow_PACIENTES(patientID, name, lastName, age, CI, entryDate, phoneNumber, home, representName, representCI, consultReason, presentIssues):
    conn = getConnection()
    try:
        cursor = conn.cursor()
        cursor.execute("UPDATE pacientes SET name = ?, lastName = ?, age = ?, CI = ?, entryDate = ?, phoneNumber = ?, home = ?, representName = ?, representCI = ?, consultReason = ?, presentIssues = ? WHERE patientID = ?",
                        (name, lastName, age, CI, entryDate, phoneNumber, home, representName, representCI, consultReason, presentIssues, patientID))
        conn.commit()
    except sql.Error as e:
        conn.rollback()
        raise e
    finally:
        conn.close()

def deleteRow_PACIENTES(patientID):
    conn = getConnection()
    try:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM pacientes WHERE patientID = ?", (patientID,))
        conn.commit()
    except sql.Error as e:
        conn.rollback()
        raise e
    finally:
        conn.close()

def createTable_ANTECEDENTES():
    conn = getConnection()
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
    FOREIGN KEY (patientID) REFERENCES pacientes(patientID) ON DELETE CASCADE
)
        """
    )
    conn.commit()
    conn.close()

def createRow_ANTECEDENTES(patientID, earNoseThroat, respiratory, allergy, cardiovascular, gastrointestinal, endocrine, renal, hepatic, neurologic, neoplastic, blood, viral, gynecologic, covid, hiv, surgeries, medications, hepatitisVaccine, covidVaccine, familyHistory):
    conn = getConnection()
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
    conn = getConnection()
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM antecedentes_personales")
        rows = cursor.fetchall()
        return rows
    finally:
        conn.close()

def updateRow_ANTECEDENTES(patientID, earNoseThroat, respiratory, allergy, cardiovascular, gastrointestinal, endocrine, renal, hepatic, neurologic, neoplastic, blood, viral, gynecologic, covid, hiv, surgeries, medications, hepatitisVaccine, covidVaccine, familyHistory):
    conn = getConnection()
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
    conn = getConnection()
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
    conn = getConnection()
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
    FOREIGN KEY (patientID) REFERENCES pacientes(patientID) ON DELETE CASCADE
)
        """
    )
    conn.commit()
    conn.close()

def createRow_EXAMEN(patientID, extraoral, intraoralTB, intraoralTD, periodontal, PA):
    conn = getConnection()
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
    conn = getConnection()
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM examen_fisico")
        rows = cursor.fetchall()
        return rows
    finally:
        conn.close()

def updateRow_EXAMEN(patientID, extraoral, intraoralTB, intraoralTD, periodontal, PA):
    conn = getConnection()
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
    conn = getConnection()
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
    conn = getConnection()
    cursor = conn.cursor()
    cursor.execute(
        """CREATE TABLE IF NOT EXISTS odontograms (
    ID INTEGER PRIMARY KEY AUTOINCREMENT,
    patientID INTEGER,
    notes TEXT,
    FOREIGN KEY (patientID) REFERENCES pacientes(patientID) ON DELETE CASCADE
)
        """
    )
    conn.commit()
    conn.close()

# >>> NO USADO ACTUALMENTE - Pendiente de implementar en UI <<<
def createRow_ODONTOGRAMA(patientID, notes):
    conn = getConnection()
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
    conn = getConnection()
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM odontograms")
        rows = cursor.fetchall()
        return rows
    finally:
        conn.close()

def updateRow_ODONTOGRAMA(id, notes):
    conn = getConnection()
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
    conn = getConnection()
    try:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM odontograms WHERE ID = ?", (id,))
        conn.commit()
    except sql.Error as e:
        conn.rollback()
        raise e
    finally:
        conn.close()

def createTable_ODONTOGRAMA_DETAILS():
    conn = getConnection()
    cursor = conn.cursor()
    cursor.execute(
        """CREATE TABLE IF NOT EXISTS odontogram_details (
    ID INTEGER PRIMARY KEY AUTOINCREMENT,
    odontogramID INTEGER,
    tooth INTEGER,
    face TEXT,
    affected TEXT NOT NULL,
    description TEXT,
    FOREIGN KEY (odontogramID) REFERENCES odontograms(ID) ON DELETE CASCADE
)
        """
    )
    conn.commit()
    conn.close()

def createRow_ODONTOGRAMA_DETAILS(odontogramID, tooth, face, affected, description):
    conn = getConnection()
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
    conn = getConnection()
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM odontogram_details")
        rows = cursor.fetchall()
        return rows
    finally:
        conn.close()

# >>> NO USADO ACTUALMENTE - Pendiente de implementar en UI <<<
def readODONTOGRAMA_DETAILS(odontogramID):
    conn = getConnection()
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM odontogram_details WHERE odontogramID = ?", (odontogramID,))
        rows = cursor.fetchall()
        return rows
    finally:
        conn.close()

def updateRow_ODONTOGRAMA_DETAILS(id, tooth, face, affected, description):
    conn = getConnection()
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
    conn = getConnection()
    try:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM odontogram_details WHERE ID = ?", (id,))
        conn.commit()
    except sql.Error as e:
        conn.rollback()
        raise e
    finally:
        conn.close()

def createTable_TRATAMIENTO():
    conn = getConnection()
    cursor = conn.cursor()
    cursor.execute(
        """CREATE TABLE IF NOT EXISTS tratamiento (
    ID INTEGER PRIMARY KEY AUTOINCREMENT,
    patientID INTEGER,
    diagnosis TEXT,
    treatmentPlan TEXT,
    FOREIGN KEY (patientID) REFERENCES pacientes(patientID) ON DELETE CASCADE
)
        """
    )
    conn.commit()
    conn.close()

# >>> NO USADO ACTUALMENTE - Pendiente de implementar en UI <<<
def createRow_TRATAMIENTO(patientID, diagnosis, treatmentPlan):
    conn = getConnection()
    try:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO tratamiento (patientID, diagnosis, treatmentPlan) VALUES (?, ?, ?)",
                        (patientID, diagnosis, treatmentPlan)
                        )
        conn.commit()
    except sql.Error as e:
        conn.rollback()
        raise e
    finally:
        conn.close()

def readTable_TRATAMIENTO():
    conn = getConnection()
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM tratamiento")
        rows = cursor.fetchall()
        return rows
    finally:
        conn.close()

def readTRATAMIENTO(patientID):
    conn = getConnection()
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM tratamiento WHERE patientID = ?", (patientID,))
        rows = cursor.fetchall()
        return rows
    finally:
        conn.close()

def updateRow_TRATAMIENTO(id, diagnosis, treatmentPlan):
    conn = getConnection()
    try:
        cursor = conn.cursor()
        cursor.execute("UPDATE tratamiento SET diagnosis = ?, treatmentPlan = ? WHERE ID = ?",
                        (diagnosis, treatmentPlan, id))
        conn.commit()
    except sql.Error as e:
        conn.rollback()
        raise e
    finally:
        conn.close()

def deleteRow_TRATAMIENTO(id):
    conn = getConnection()
    try:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM tratamiento WHERE ID = ?", (id,))
        conn.commit()
    except sql.Error as e:
        conn.rollback()
        raise e
    finally:
        conn.close()

def createTable_ABONO():
    conn = getConnection()
    cursor = conn.cursor()
    cursor.execute(
        """CREATE TABLE IF NOT EXISTS abonos (
    ID INTEGER PRIMARY KEY AUTOINCREMENT,
    patientID INTEGER,
    date TEXT,
    description TEXT,
    treatmentCost REAL,
    amount REAL,
    remaining REAL,
    FOREIGN KEY (patientID) REFERENCES pacientes(patientID) ON DELETE CASCADE
)
        """
    )
    conn.commit()
    conn.close()

# >>> NO USADO ACTUALMENTE - Pendiente de implementar en UI <<<
def createRow_ABONO(patientID, date, description, treatmentCost, amount, remaining):
    conn = getConnection()
    try:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO abonos (patientID, date, description, treatmentCost, amount, remaining) VALUES (?, ?, ?, ?, ?, ?)",
                        (patientID, date, description, treatmentCost, amount, remaining)
                        )
        conn.commit()
    except sql.Error as e:
        conn.rollback()
        raise e
    finally:
        conn.close()

def readTable_ABONO():
    conn = getConnection()
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM abonos")
        rows = cursor.fetchall()
        return rows
    finally:
        conn.close()

def readABONO(patientID):
    conn = getConnection()
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM abonos WHERE patientID = ?", (patientID,))
        rows = cursor.fetchall()
        return rows
    finally:
        conn.close()

def updateRow_ABONO(id, date, description, treatmentCost, amount, remaining):
    conn = getConnection()
    try:
        cursor = conn.cursor()
        cursor.execute("UPDATE abonos SET date = ?, description = ?, treatmentCost = ?, amount = ?, remaining = ? WHERE ID = ?",
                        (date, description, treatmentCost, amount, remaining, id))
        conn.commit()
    except sql.Error as e:
        conn.rollback()
        raise e
    finally:
        conn.close()

def deleteRow_ABONO(id):
    conn = getConnection()
    try:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM abonos WHERE ID = ?", (id,))
        conn.commit()
    except sql.Error as e:
        conn.rollback()
        raise e
    finally:
        conn.close()



if __name__ == "__main__":
    createTable_PACIENTES()
    createTable_ANTECEDENTES()
    createTable_EXAMEN()
    createTable_ODONTOGRAMA()
    createTable_ODONTOGRAMA_DETAILS()
    createTable_TRATAMIENTO()
    createTable_ABONO()
