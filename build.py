import subprocess
import sys
import os

APP_NAME = "ClinicaOdontologica"
MAIN_SCRIPT = "main.py"
ICON_PATH = os.path.join("assets", "clinica-icon.ico")

PYINSTALLER_ARGS = [
    sys.executable, "-m", "PyInstaller",
    "--noconfirm",
    "--onedir",
    "--windowed",
    f"--name={APP_NAME}",
    f"--distpath=dist",
    f"--workpath=build",
    f"--specpath=dist",
    "--clean",
]

abs_icon = os.path.abspath(ICON_PATH)
if os.path.exists(abs_icon):
    PYINSTALLER_ARGS.append(f"--icon={abs_icon}")

HIDDEN_IMPORTS = [
    "views.welcome_dialog",
    "views.principal_view",
    "views.form_patient",
    "views.patient_detail_view",
    "views.abonos_view",
    "views.export_view",
    "views.components.patient_card",
    "views.components.search_filter",
    "views.components.tratamiento_dialog",
    "views.components.odontogram",
    "services.patient_service",
    "services.abono_service",
    "services.tratamiento_service",
    "services.export_service",
    "services.backup_service",
    "database.createDB",
    "database.migrations",
    "database.crypto",
    "database.models",
    "database.utils",
]

for imp in HIDDEN_IMPORTS:
    PYINSTALLER_ARGS.append(f"--hidden-import={imp}")

DATAS = [
    ("assets", "assets"),
]

for src, dst in DATAS:
    abs_src = os.path.abspath(src)
    if os.path.exists(abs_src):
        PYINSTALLER_ARGS.append(f"--add-data={abs_src}{os.pathsep}{dst}")

PYINSTALLER_ARGS.append(MAIN_SCRIPT)


def run_build():
    print("=" * 60)
    print(f"  Build {APP_NAME} con PyInstaller")
    print("=" * 60)
    print()
    print("Comando:")
    print(" ".join(PYINSTALLER_ARGS))
    print()

    result = subprocess.run(PYINSTALLER_ARGS, cwd=os.path.dirname(os.path.abspath(__file__)))

    if result.returncode == 0:
        print()
        print("=" * 60)
        print("  BUILD EXITOSO")
        print(f"  Ejecutable en: dist/{APP_NAME}/{APP_NAME}.exe")
        print("=" * 60)
    else:
        print()
        print("=" * 60)
        print("  BUILD FALLIDO")
        print(f"  Codigo de salida: {result.returncode}")
        print("=" * 60)
        sys.exit(1)


if __name__ == "__main__":
    run_build()
