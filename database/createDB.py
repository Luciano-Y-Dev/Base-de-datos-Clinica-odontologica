import sqlite3 as sql
import os
import shutil
import platformdirs
from .crypto import encrypt_field, decrypt_field

_APP_NAME = "clinica_odontologica"
_DATA_DIR = platformdirs.user_data_dir(_APP_NAME, appauthor=False)

DB_PATH = os.path.join(_DATA_DIR, "Clinica.db")
LEGACY_DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "Clinica.db")

def getConnection():
    os.makedirs(os.path.dirname(DB_PATH) or ".", exist_ok=True)
    conn = sql.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn

def migrate_legacy_db_if_needed():
    """Copia la DB de la ubicacion antigua (junto al codigo) a la carpeta de
    datos del usuario, solo si la nueva aun no existe. Devuelve True si migro."""
    if os.path.exists(DB_PATH) or not os.path.exists(LEGACY_DB_PATH):
        return False
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    shutil.copy2(LEGACY_DB_PATH, DB_PATH)
    return True

def createTable_PACIENTES():
    conn = getConnection()
    cursor = conn.cursor()
    cursor.execute(
        """CREATE TABLE IF NOT EXISTS pacientes (
    patientID INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    lastName TEXT NOT NULL,
    age INTEGER NOT NULL,
    CI TEXT NOT NULL,
    entryDate TEXT NOT NULL,
    phoneNumber TEXT,
    home TEXT,
    representName TEXT,
    representCI TEXT,
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
                        (name, lastName, age, encrypt_field(str(CI)), entryDate, phoneNumber, home, representName, encrypt_field(str(representCI)) if representCI else "", consultReason, presentIssues)
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
        return [
            (r[0], r[1], r[2], r[3], decrypt_field(r[4]), r[5], r[6], r[7], r[8], decrypt_field(r[9]), r[10], r[11])
            for r in rows
        ]
    finally:
        conn.close()

def updateRow_PACIENTES(patientID, name, lastName, age, CI, entryDate, phoneNumber, home, representName, representCI, consultReason, presentIssues):
    conn = getConnection()
    try:
        cursor = conn.cursor()
        cursor.execute("UPDATE pacientes SET name = ?, lastName = ?, age = ?, CI = ?, entryDate = ?, phoneNumber = ?, home = ?, representName = ?, representCI = ?, consultReason = ?, presentIssues = ? WHERE patientID = ?",
                        (name, lastName, age, encrypt_field(str(CI)), entryDate, phoneNumber, home, representName, encrypt_field(str(representCI)) if representCI else "", consultReason, presentIssues, patientID))
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
    patientID INTEGER NOT NULL UNIQUE,
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
                        (patientID, earNoseThroat, respiratory, allergy, cardiovascular, gastrointestinal, endocrine, renal, hepatic, neurologic, neoplastic, blood, viral, gynecologic, covid, encrypt_field(hiv), surgeries, medications, hepatitisVaccine, covidVaccine, familyHistory)
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
        return [
            (r[0], r[1], r[2], r[3], r[4], r[5], r[6], r[7], r[8], r[9], r[10], r[11], r[12], r[13], r[14], r[15], decrypt_field(r[16]), r[17], r[18], r[19], r[20], r[21])
            for r in rows
        ]
    finally:
        conn.close()

def updateRow_ANTECEDENTES(patientID, earNoseThroat, respiratory, allergy, cardiovascular, gastrointestinal, endocrine, renal, hepatic, neurologic, neoplastic, blood, viral, gynecologic, covid, hiv, surgeries, medications, hepatitisVaccine, covidVaccine, familyHistory):
    conn = getConnection()
    try:
        cursor = conn.cursor()
        cursor.execute("UPDATE antecedentes_personales SET earNoseThroat = ?, respiratory = ?, allergy = ?, cardiovascular = ?, gastrointestinal = ?, endocrine = ?, renal = ?, hepatic = ?, neurologic = ?, neoplastic = ?, blood = ?, viral = ?, gynecologic = ?, covid = ?, hiv = ?, surgeries = ?, medications = ?, hepatitisVaccine = ?, covidVaccine = ?, familyHistory = ? WHERE patientID = ?",
                        (earNoseThroat, respiratory, allergy, cardiovascular, gastrointestinal, endocrine, renal, hepatic, neurologic, neoplastic, blood, viral, gynecologic, covid, encrypt_field(hiv), surgeries, medications, hepatitisVaccine, covidVaccine, familyHistory, patientID))
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
    patientID INTEGER NOT NULL UNIQUE,
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
    patientID INTEGER NOT NULL,
    notes TEXT,
    FOREIGN KEY (patientID) REFERENCES pacientes(patientID) ON DELETE CASCADE
)
        """
    )
    conn.commit()
    conn.close()

def createRow_ODONTOGRAMA(patientID, notes):
    conn = getConnection()
    try:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO odontograms (patientID, notes) VALUES (?, ?)",
                        (patientID, notes)
                        )
        conn.commit()
        return cursor.lastrowid
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
    odontogramID INTEGER NOT NULL,
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
    patientID INTEGER NOT NULL,
    diagnosis TEXT,
    treatmentPlan TEXT,
    date TEXT,
    FOREIGN KEY (patientID) REFERENCES pacientes(patientID) ON DELETE CASCADE
)
        """
    )
    conn.commit()
    conn.close()

def migrateTRATAMIENTO_add_date():
    conn = getConnection()
    cursor = conn.cursor()
    try:
        cursor.execute("PRAGMA table_info(tratamiento)")
        columns = [col[1] for col in cursor.fetchall()]
        if 'date' not in columns:
            cursor.execute("ALTER TABLE tratamiento ADD COLUMN date TEXT")
            conn.commit()
    except sql.Error:
        pass
    finally:
        conn.close()

def createRow_TRATAMIENTO(patientID, diagnosis, treatmentPlan, date=None):
    conn = getConnection()
    try:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO tratamiento (patientID, diagnosis, treatmentPlan, date) VALUES (?, ?, ?, ?)",
                        (patientID, diagnosis, treatmentPlan, date)
                        )
        conn.commit()
        return cursor.lastrowid
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

def updateRow_TRATAMIENTO(id, diagnosis, treatmentPlan, date=None):
    conn = getConnection()
    try:
        cursor = conn.cursor()
        cursor.execute("UPDATE tratamiento SET diagnosis = ?, treatmentPlan = ?, date = ? WHERE ID = ?",
                        (diagnosis, treatmentPlan, date, id))
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
    patientID INTEGER NOT NULL,
    date TEXT,
    description TEXT,
    treatmentCost REAL NOT NULL DEFAULT 0,
    amount REAL NOT NULL DEFAULT 0 CHECK (amount >= 0),
    remaining REAL NOT NULL DEFAULT 0 CHECK (remaining >= 0),
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

def update_abonos_chain(abonos):
    """Actualiza varias filas de abonos en una sola transaccion.
    Cada elemento debe tener: id, date, description, treatmentCost, amount, remaining."""
    conn = getConnection()
    try:
        cursor = conn.cursor()
        for a in abonos:
            cursor.execute("UPDATE abonos SET date = ?, description = ?, treatmentCost = ?, amount = ?, remaining = ? WHERE ID = ?",
                            (a.date, a.description, a.treatmentCost, a.amount, a.remaining, a.id))
        conn.commit()
    except sql.Error as e:
        conn.rollback()
        raise e
    finally:
        conn.close()

def delete_abono_with_chain(abono_id, abonos):
    """Elimina un abono y actualiza las filas restantes en una sola transaccion."""
    conn = getConnection()
    try:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM abonos WHERE ID = ?", (abono_id,))
        for a in abonos:
            cursor.execute("UPDATE abonos SET date = ?, description = ?, treatmentCost = ?, amount = ?, remaining = ? WHERE ID = ?",
                            (a.date, a.description, a.treatmentCost, a.amount, a.remaining, a.id))
        conn.commit()
    except sql.Error as e:
        conn.rollback()
        raise e
    finally:
        conn.close()


def save_patient_atomic(patient_id, name, lastName, age, CI, entryDate, phoneNumber, home, representName, representCI, consultReason, presentIssues, antecedentes_data, examen_data, odontogram_data, abono_data):
    # Validaciones basicas antes de abrir transaccion
    if not name or not str(name).strip():
        raise ValueError("El nombre es obligatorio")
    if not CI or not str(CI).strip():
        raise ValueError("La CI es obligatoria")
    try:
        int(age)
    except (TypeError, ValueError):
        raise ValueError("La edad debe ser un numero entero")

    conn = getConnection()
    conn.execute("PRAGMA foreign_keys = ON;")
    try:
        cursor = conn.cursor()

        # 1. Paciente
        if patient_id:
            cursor.execute("UPDATE pacientes SET name = ?, lastName = ?, age = ?, CI = ?, entryDate = ?, phoneNumber = ?, home = ?, representName = ?, representCI = ?, consultReason = ?, presentIssues = ? WHERE patientID = ?",
                (name, lastName, age, encrypt_field(str(CI)), entryDate, phoneNumber, home, representName, encrypt_field(str(representCI)) if representCI else "", consultReason, presentIssues, patient_id))
            cid = patient_id
        else:
            cursor.execute("INSERT INTO pacientes (name, lastName, age, CI, entryDate, phoneNumber, home, representName, representCI, consultReason, presentIssues) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                (name, lastName, age, encrypt_field(str(CI)), entryDate, phoneNumber, home, representName, encrypt_field(str(representCI)) if representCI else "", consultReason, presentIssues))
            cid = cursor.lastrowid

        # 2. Antecedentes
        ad = antecedentes_data
        cursor.execute("SELECT COUNT(*) FROM antecedentes_personales WHERE patientID = ?", (cid,))
        if cursor.fetchone()[0] > 0:
            cursor.execute("UPDATE antecedentes_personales SET earNoseThroat = ?, respiratory = ?, allergy = ?, cardiovascular = ?, gastrointestinal = ?, endocrine = ?, renal = ?, hepatic = ?, neurologic = ?, neoplastic = ?, blood = ?, viral = ?, gynecologic = ?, covid = ?, hiv = ?, surgeries = ?, medications = ?, hepatitisVaccine = ?, covidVaccine = ?, familyHistory = ? WHERE patientID = ?",
                (*ad[:14], encrypt_field(ad[14]), *ad[15:], cid))
        else:
            cursor.execute("INSERT INTO antecedentes_personales (patientID, earNoseThroat, respiratory, allergy, cardiovascular, gastrointestinal, endocrine, renal, hepatic, neurologic, neoplastic, blood, viral, gynecologic, covid, hiv, surgeries, medications, hepatitisVaccine, covidVaccine, familyHistory) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                (cid, *ad[:14], encrypt_field(ad[14]), *ad[15:]))

        # 3. Examen fisico
        ed = examen_data
        cursor.execute("SELECT COUNT(*) FROM examen_fisico WHERE patientID = ?", (cid,))
        if cursor.fetchone()[0] > 0:
            cursor.execute("UPDATE examen_fisico SET extraoral = ?, intraoralTB = ?, intraoralTD = ?, periodontal = ?, PA = ? WHERE patientID = ?",
                (*ed, cid))
        else:
            cursor.execute("INSERT INTO examen_fisico (patientID, extraoral, intraoralTB, intraoralTD, periodontal, PA) VALUES (?, ?, ?, ?, ?, ?)",
                (cid, *ed))

        # 4. Odontograma (reemplazo total: la ficha refleja el estado completo)
        if odontogram_data is not None:
            notes = odontogram_data.get("notes", "")
            cursor.execute("SELECT ID FROM odontograms WHERE patientID = ? ORDER BY ID DESC LIMIT 1", (cid,))
            row = cursor.fetchone()
            if row:
                odontogram_id = row[0]
                cursor.execute("UPDATE odontograms SET notes = ? WHERE ID = ?", (notes, odontogram_id))
            else:
                cursor.execute("INSERT INTO odontograms (patientID, notes) VALUES (?, ?)", (cid, notes))
                odontogram_id = cursor.lastrowid

            cursor.execute("DELETE FROM odontogram_details WHERE odontogramID = ?", (odontogram_id,))
            for aff in odontogram_data.get("affections", []):
                cursor.execute("INSERT INTO odontogram_details (odontogramID, tooth, face, affected, description) VALUES (?, ?, ?, ?, ?)",
                    (odontogram_id, aff["tooth"], aff["face"], aff["affected"], aff["description"]))

        # 5. Abono (solo se crea; el historial NUNCA se modifica al editar la ficha)
        if abono_data:
            cost = abono_data.get("cost", 0)
            amount = abono_data.get("amount", 0)
            remaining = cost - amount
            desc = abono_data.get("description", "")
            from datetime import date
            today = date.today().isoformat()
            cursor.execute("INSERT INTO abonos (patientID, date, description, treatmentCost, amount, remaining) VALUES (?, ?, ?, ?, ?, ?)",
                (cid, today, desc, cost, amount, remaining))

        conn.commit()
        return cid
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
    migrateTRATAMIENTO_add_date()
    createTable_ABONO()
