import os
import sys
import pytest
import tempfile

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

from services.export_service import generate_patients_pdf
from database.createDB import createRow_PACIENTES


class TestExportPDF:
    def test_generate_pdf_for_patient(self, test_db, sample_patient_data):
        patient_id = createRow_PACIENTES(
            sample_patient_data["name"],
            sample_patient_data["lastName"],
            sample_patient_data["age"],
            sample_patient_data["CI"],
            sample_patient_data["entryDate"],
            sample_patient_data["phoneNumber"],
            sample_patient_data["home"],
            sample_patient_data["representName"],
            sample_patient_data["representCI"],
            sample_patient_data["consultReason"],
            sample_patient_data["presentIssues"],
        )
        with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as f:
            output_path = f.name
        try:
            result = generate_patients_pdf([patient_id], output_path)
            assert os.path.exists(result)
            assert os.path.getsize(result) > 0
        finally:
            if os.path.exists(output_path):
                os.unlink(output_path)

    def test_generate_pdf_empty_list(self, test_db):
        with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as f:
            output_path = f.name
        try:
            result = generate_patients_pdf([], output_path)
            assert os.path.exists(result)
        finally:
            if os.path.exists(output_path):
                os.unlink(output_path)
