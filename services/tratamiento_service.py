from __future__ import annotations
from database.createDB import createRow_TRATAMIENTO, updateRow_TRATAMIENTO, deleteRow_TRATAMIENTO
from database.utils import readTRATAMIENTO_by_patient


def add_tratamiento(patient_id: int, text: str, date: str) -> int:
    if not text or not text.strip():
        raise ValueError("El texto del tratamiento es obligatorio.")
    return createRow_TRATAMIENTO(patient_id, text.strip(), "", date)


def update_tratamiento(tratamiento_id: int, text: str, date: str) -> None:
    if not text or not text.strip():
        raise ValueError("El texto del tratamiento es obligatorio.")
    updateRow_TRATAMIENTO(tratamiento_id, text.strip(), "", date)


def delete_tratamiento(tratamiento_id: int) -> None:
    deleteRow_TRATAMIENTO(tratamiento_id)


def get_patient_tratamientos(patient_id: int) -> list:
    return readTRATAMIENTO_by_patient(patient_id)
