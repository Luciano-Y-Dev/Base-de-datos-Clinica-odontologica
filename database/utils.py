from .createDB import getConnection
from .crypto import decrypt_field
from .models import Paciente, PacienteConSaldo, Antecedentes, Examen, Odontograma, Abono

def readTable_PACIENTES_ordered():
    conn = getConnection()
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM pacientes ORDER BY entryDate DESC")
        rows = cursor.fetchall()
        return [
            Paciente(r[0], r[1], r[2], r[3], decrypt_field(r[4]), r[5], r[6], r[7], r[8], decrypt_field(r[9]), r[10], r[11])
            for r in rows
        ]
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
        r = cursor.fetchone()
        if r:
            return Paciente(r[0], r[1], r[2], r[3], decrypt_field(r[4]), r[5], r[6], r[7], r[8], decrypt_field(r[9]), r[10], r[11])
        return None
    finally:
        conn.close()

def readANTECEDENTES(patientID):
    conn = getConnection()
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM antecedentes_personales WHERE patientID = ?", (patientID,))
        r = cursor.fetchone()
        if r:
            return Antecedentes(r[0], r[1], r[2], r[3], r[4], r[5], r[6], r[7], r[8], r[9], r[10], r[11], r[12], r[13], r[14], r[15], decrypt_field(r[16]), r[17], r[18], r[19], r[20], r[21])
        return None
    finally:
        conn.close()

def readEXAMEN(patientID):
    conn = getConnection()
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM examen_fisico WHERE patientID = ?", (patientID,))
        r = cursor.fetchone()
        if r:
            return Examen(r[0], r[1], r[2], r[3], r[4], r[5], r[6])
        return None
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
        r = cursor.fetchone()
        if r:
            return Odontograma(r[0], r[1], r[2])
        return None
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
        rows = cursor.fetchall()
        return [Abono(r[0], r[1], r[2], r[3], r[4], r[5], r[6]) for r in rows]
    finally:
        conn.close()

def readPATIENTS_with_remaining_all():
    conn = getConnection()
    try:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT p.*,
                   (SELECT remaining FROM abonos WHERE patientID = p.patientID ORDER BY ID DESC LIMIT 1) as remaining
            FROM pacientes p
            ORDER BY p.entryDate DESC
        """)
        rows = cursor.fetchall()
        return [
            PacienteConSaldo(r[0], r[1], r[2], r[3], decrypt_field(r[4]), r[5], r[6], r[7], r[8], decrypt_field(r[9]), r[10], r[11], r[12])
            for r in rows
        ]
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
            ORDER BY p.entryDate DESC
        """)
        rows = cursor.fetchall()
        return [
            PacienteConSaldo(r[0], r[1], r[2], r[3], decrypt_field(r[4]), r[5], r[6], r[7], r[8], decrypt_field(r[9]), r[10], r[11], r[12])
            for r in rows
        ]
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
               OR (SELECT remaining FROM abonos WHERE patientID = p.patientID ORDER BY ID DESC LIMIT 1) IS NULL
            ORDER BY p.entryDate DESC
        """)
        rows = cursor.fetchall()
        return [
            PacienteConSaldo(r[0], r[1], r[2], r[3], decrypt_field(r[4]), r[5], r[6], r[7], r[8], decrypt_field(r[9]), r[10], r[11], r[12])
            for r in rows
        ]
    finally:
        conn.close()
