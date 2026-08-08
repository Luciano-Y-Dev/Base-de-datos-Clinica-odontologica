from .createDB import getConnection

def readTable_PACIENTES_ordered():
    conn = getConnection()
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM pacientes ORDER BY entryDate DESC")
        return cursor.fetchall()
    finally:
        conn.close()

def readREMAINING(patientID):
    conn = getConnection()
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT remaining FROM abonos WHERE patientID = ? ORDER BY ID DESC LIMIT 1", (patientID,))
        result = cursor.fetchone()
        return result[0] if result else 0.0
    finally:
        conn.close()

def readPACIENTE(patientID):
    conn = getConnection()
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM pacientes WHERE patientID = ?", (patientID,))
        return cursor.fetchone()
    finally:
        conn.close()

def readANTECEDENTES(patientID):
    conn = getConnection()
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM antecedentes_personales WHERE patientID = ?", (patientID,))
        return cursor.fetchone()
    finally:
        conn.close()

def readEXAMEN(patientID):
    conn = getConnection()
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM examen_fisico WHERE patientID = ?", (patientID,))
        return cursor.fetchone()
    finally:
        conn.close()

def existANTECEDENTES(patientID):
    conn = getConnection()
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM antecedentes_personales WHERE patientID = ?", (patientID,))
        return cursor.fetchone()[0] > 0
    finally:
        conn.close()

def existEXAMEN(patientID):
    conn = getConnection()
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM examen_fisico WHERE patientID = ?", (patientID,))
        return cursor.fetchone()[0] > 0
    finally:
        conn.close()

def readODONTOGRAMA_by_patient(patientID):
    conn = getConnection()
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM odontograms WHERE patientID = ? ORDER BY ID DESC LIMIT 1", (patientID,))
        return cursor.fetchone()
    finally:
        conn.close()

def existODONTOGRAMA(patientID):
    conn = getConnection()
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM odontograms WHERE patientID = ?", (patientID,))
        return cursor.fetchone()[0] > 0
    finally:
        conn.close()

def readABONOS_ordered(patientID):
    conn = getConnection()
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM abonos WHERE patientID = ? ORDER BY ID DESC", (patientID,))
        return cursor.fetchall()
    finally:
        conn.close()

def readPATIENTS_with_remaining():
    conn = getConnection()
    try:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT p.*, 
                   (SELECT remaining FROM abonos WHERE patientID = p.patientID ORDER BY ID DESC LIMIT 1) as remaining
            FROM pacientes p
            WHERE (SELECT remaining FROM abonos WHERE patientID = p.patientID ORDER BY ID DESC LIMIT 1) > 0
               OR (SELECT remaining FROM abonos WHERE patientID = p.patientID ORDER BY ID DESC LIMIT 1) IS NULL
            ORDER BY p.entryDate DESC
        """)
        return cursor.fetchall()
    finally:
        conn.close()


def readPATIENTS_paid():
    conn = getConnection()
    try:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT p.*, 
                   (SELECT remaining FROM abonos WHERE patientID = p.patientID ORDER BY ID DESC LIMIT 1) as remaining
            FROM pacientes p
            WHERE (SELECT remaining FROM abonos WHERE patientID = p.patientID ORDER BY ID DESC LIMIT 1) = 0
            ORDER BY p.entryDate DESC
        """)
        return cursor.fetchall()
    finally:
        conn.close()
