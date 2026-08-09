from __future__ import annotations
from database.createDB import createRow_ABONO, readABONO
from database.utils import readABONOS_ordered, readPATIENTS_with_remaining, readPATIENTS_paid


def add_abono(patient_id: int, amount_text: str, date: str, description: str) -> dict[str, float]:
    if not amount_text:
        raise ValueError("El monto del abono es obligatorio.")

    try:
        amount = float(amount_text)
    except (TypeError, ValueError):
        raise ValueError("El monto debe ser un número.")

    if amount < 0:
        raise ValueError("El monto no puede ser negativo.")

    abonos = readABONOS_ordered(patient_id)
    last_remaining = abonos[0].remaining if abonos and abonos[0].remaining is not None else 0.0
    treatment_cost = abonos[0].treatmentCost if abonos else 0.0
    new_remaining = last_remaining - amount

    if new_remaining < 0:
        raise ValueError("El abono excede el saldo pendiente.")

    createRow_ABONO(patient_id, date, description, treatment_cost, amount, new_remaining)
    return {"remaining": new_remaining}


def get_patient_abonos(patient_id: int) -> list[tuple]:
    return readABONOS_ordered(patient_id)


def get_patients_with_remaining() -> list[tuple]:
    return readPATIENTS_with_remaining()


def get_patients_paid() -> list[tuple]:
    return readPATIENTS_paid()


def get_patient_abono(patient_id: int) -> list[tuple]:
    return readABONO(patient_id)
