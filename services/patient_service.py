from __future__ import annotations
from typing import Any, Protocol
from database.createDB import save_patient_atomic, deleteRow_PACIENTES, readODONTOGRAMA_DETAILS
from database.utils import (
    readPACIENTE, readANTECEDENTES, readEXAMEN,
    readODONTOGRAMA_by_patient, readREMAINING, readTable_PACIENTES_ordered,
    readPATIENTS_with_remaining_all
)


class CheckBox(Protocol):
    def isChecked(self) -> bool: ...
    def toPlainText(self) -> str: ...


class OdontogramWidget(Protocol):
    def get_data(self) -> dict[str, Any]: ...


def _validate_required(value: str | None, field_name: str) -> None:
    if not value or not str(value).strip():
        raise ValueError(f"El campo '{field_name}' es obligatorio.")


def _validate_int(value: str | None, field_name: str) -> int:
    try:
        return int(value)
    except (TypeError, ValueError):
        raise ValueError(f"El campo '{field_name}' debe ser un número entero.")


def _validate_float(value: str | None, field_name: str) -> float:
    try:
        return float(value)
    except (TypeError, ValueError):
        raise ValueError(f"El campo '{field_name}' debe ser un número.")


def _prepare_antecedentes(ant_checks: list[tuple[Any, CheckBox, CheckBox]]) -> list[str | None]:
    ad: list[str | None] = [None] * 20
    for idx, (fname, cb, tf) in enumerate(ant_checks):
        if cb.isChecked():
            ad[idx] = f"Si - {tf.toPlainText()}" if tf.toPlainText() else "Si"
    return ad


def _prepare_odontogram(odontogram_widget: OdontogramWidget) -> dict[str, Any] | None:
    data = odontogram_widget.get_data()
    if data.get("affections"):
        return {"notes": "", "affections": data["affections"]}
    return None


def _prepare_abono(cost_text: str, amount_text: str, desc_text: str) -> dict[str, Any] | None:
    if not cost_text:
        return None
    cost = _validate_float(cost_text, "Costo")
    amount = _validate_float(amount_text, "Abono") if amount_text else 0.0
    return {"cost": cost, "amount": amount, "description": desc_text}


def save_patient(
    patient_id: int | None,
    form_data: dict[str, str],
    ant_checks: list[tuple[Any, CheckBox, CheckBox]],
    odontogram_widget: OdontogramWidget,
) -> int:
    _validate_required(form_data.get("name"), "Nombre")
    _validate_required(form_data.get("CI"), "CI")

    age = _validate_int(form_data.get("age"), "Edad")
    ci = _validate_int(form_data.get("CI"), "CI")
    rep_ci = _validate_int(form_data.get("representCI"), "CI Representante") if form_data.get("representCI") else 0

    ad = _prepare_antecedentes(ant_checks)
    ed = [form_data.get("extraoral", ""), form_data.get("intraoralTB", ""),
          form_data.get("intraoralTD", ""), form_data.get("periodontal", ""),
          form_data.get("PA", "")]
    od = _prepare_odontogram(odontogram_widget)
    ab = _prepare_abono(form_data.get("cost", ""), form_data.get("abono", ""),
                        form_data.get("descAbono", ""))

    return save_patient_atomic(
        patient_id, form_data["name"], form_data["lastName"], age, ci,
        form_data.get("entryDate", ""), form_data.get("phoneNumber", ""),
        form_data.get("home", ""), form_data.get("representName", ""),
        rep_ci, form_data.get("consultReason", ""),
        form_data.get("presentIssues", ""),
        ad, ed, od, ab
    )


def delete_patient(patient_id: int) -> bool:
    deleteRow_PACIENTES(patient_id)
    return True


def get_patient(patient_id: int):
    return readPACIENTE(patient_id)


def get_patient_antecedentes(patient_id: int):
    return readANTECEDENTES(patient_id)


def get_patient_examen(patient_id: int):
    return readEXAMEN(patient_id)


def get_patient_odontogram(patient_id: int):
    return readODONTOGRAMA_by_patient(patient_id)


def get_odontogram_details(odontogram_id: int):
    return readODONTOGRAMA_DETAILS(odontogram_id)


def get_patient_remaining(patient_id: int) -> float:
    remaining = readREMAINING(patient_id)
    return remaining if remaining is not None else 0.0


def get_patients_ordered():
    return readTable_PACIENTES_ordered()


def get_patients_with_remaining():
    return readPATIENTS_with_remaining_all()


def get_patient_full_data(patient_id: int) -> dict[str, Any] | None:
    paciente = readPACIENTE(patient_id)
    if not paciente:
        return None
    return {
        "paciente": paciente,
        "antecedentes": readANTECEDENTES(patient_id),
        "examen": readEXAMEN(patient_id),
        "remaining": get_patient_remaining(patient_id),
        "odontograma": readODONTOGRAMA_by_patient(patient_id),
    }


def filter_patients(
    patients,
    search_text: str = "",
    date_from=None,
    date_to=None,
) -> list:
    from datetime import datetime

    filtered = []
    for p in patients:
        matches_search = True
        if search_text:
            text = search_text.lower()
            matches_search = (
                text in p.name.lower()
                or text in p.lastName.lower()
                or text in str(p.CI)
            )

        matches_date = True
        if p.entryDate and date_from and date_to:
            try:
                entry_date = datetime.strptime(p.entryDate, "%Y-%m-%d").date()
                if entry_date < date_from or entry_date > date_to:
                    matches_date = False
            except (ValueError, TypeError):
                pass

        if matches_search and matches_date:
            filtered.append(p)

    return filtered
