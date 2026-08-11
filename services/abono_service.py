from __future__ import annotations
from database.createDB import (
    createRow_ABONO, readABONO, update_abonos_chain, delete_abono_with_chain
)
from database.utils import readABONOS_ordered, readPATIENTS_with_remaining, readPATIENTS_paid


def _validate_amount(amount_text: str) -> float:
    if not amount_text:
        raise ValueError("El monto del abono es obligatorio.")
    try:
        amount = float(amount_text)
    except (TypeError, ValueError):
        raise ValueError("El monto debe ser un número.")
    if amount < 0:
        raise ValueError("El monto no puede ser negativo.")
    return amount


def add_abono(patient_id: int, amount_text: str, date: str, description: str) -> dict[str, float]:
    amount = _validate_amount(amount_text)

    abonos = readABONOS_ordered(patient_id)
    last_remaining = abonos[0].remaining if abonos and abonos[0].remaining is not None else 0.0
    treatment_cost = abonos[0].treatmentCost if abonos else 0.0
    new_remaining = last_remaining - amount

    if new_remaining < 0:
        raise ValueError("El abono excede el saldo pendiente.")

    createRow_ABONO(patient_id, date, description, treatment_cost, amount, new_remaining)
    return {"remaining": new_remaining}


def _get_abonos_asc(patient_id: int) -> list:
    return list(reversed(readABONOS_ordered(patient_id)))


def _recalculate_chain(rows: list) -> dict[int, float]:
    """Recalcula los saldos de la cadena (orden cronologico de insercion).
    Devuelve {abono_id: nuevo_remaining}. Lanza ValueError si algun saldo
    quedaria negativo."""
    prev_remaining = None
    result = {}
    for a in rows:
        base = a.treatmentCost if prev_remaining is None else prev_remaining
        new_remaining = base - a.amount
        if new_remaining < 0:
            raise ValueError("El cambio genera un saldo negativo en los abonos; revisa los montos.")
        result[a.id] = new_remaining
        prev_remaining = new_remaining
    return result


def update_abono(patient_id: int, abono_id: int, amount_text: str, date: str, description: str) -> dict[str, float]:
    """Edita un abono y recalcula los saldos posteriores en cascada."""
    amount = _validate_amount(amount_text)

    rows = _get_abonos_asc(patient_id)
    target = next((a for a in rows if a.id == abono_id), None)
    if target is None:
        raise ValueError("El abono no existe.")

    new_rows = [a._replace(amount=amount) if a.id == abono_id else a for a in rows]
    remaining_map = _recalculate_chain(new_rows)

    final_rows = []
    for a in new_rows:
        if a.id == abono_id:
            a = a._replace(date=date, description=description)
        final_rows.append(a._replace(remaining=remaining_map[a.id]))

    update_abonos_chain(final_rows)
    return {"remaining": final_rows[-1].remaining if final_rows else 0.0}


def delete_abono(patient_id: int, abono_id: int) -> dict[str, float]:
    """Elimina un abono y recalcula los saldos restantes en cascada."""
    rows = _get_abonos_asc(patient_id)
    if not any(a.id == abono_id for a in rows):
        raise ValueError("El abono no existe.")

    remaining_rows = [a for a in rows if a.id != abono_id]
    remaining_map = _recalculate_chain(remaining_rows)
    final_rows = [a._replace(remaining=remaining_map[a.id]) for a in remaining_rows]

    delete_abono_with_chain(abono_id, final_rows)
    return {"remaining": final_rows[-1].remaining if final_rows else 0.0}


def get_patient_abonos(patient_id: int) -> list[tuple]:
    return readABONOS_ordered(patient_id)


def get_patients_with_remaining() -> list[tuple]:
    return readPATIENTS_with_remaining()


def get_patients_paid() -> list[tuple]:
    return readPATIENTS_paid()


def get_patient_abono(patient_id: int) -> list[tuple]:
    return readABONO(patient_id)
