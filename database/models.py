from collections import namedtuple

Paciente = namedtuple('Paciente', [
    'id', 'name', 'lastName', 'age', 'CI', 'entryDate',
    'phoneNumber', 'home', 'representName', 'representCI',
    'consultReason', 'presentIssues'
])

PacienteConSaldo = namedtuple('PacienteConSaldo', [
    'id', 'name', 'lastName', 'age', 'CI', 'entryDate',
    'phoneNumber', 'home', 'representName', 'representCI',
    'consultReason', 'presentIssues', 'remaining'
])

Antecedentes = namedtuple('Antecedentes', [
    'id', 'patientID', 'earNoseThroat', 'respiratory', 'allergy',
    'cardiovascular', 'gastrointestinal', 'endocrine', 'renal',
    'hepatic', 'neurologic', 'neoplastic', 'blood', 'viral',
    'gynecologic', 'covid', 'hiv', 'surgeries', 'medications',
    'hepatitisVaccine', 'covidVaccine', 'familyHistory'
])

Examen = namedtuple('Examen', [
    'id', 'patientID', 'extraoral', 'intraoralTB', 'intraoralTD',
    'periodontal', 'PA'
])

Odontograma = namedtuple('Odontograma', ['id', 'patientID', 'notes'])

Abono = namedtuple('Abono', [
    'id', 'patientID', 'date', 'description', 'treatmentCost',
    'amount', 'remaining'
])
