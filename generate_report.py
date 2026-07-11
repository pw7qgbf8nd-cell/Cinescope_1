import subprocess
import webbrowser
import os
from pathlib import Path

# Путь к результатам
results_dir = Path("./allure-results")
report_dir = Path("./allure-report")

# Проверяем, есть ли результаты
if not results_dir.exists():
    print("❌ Папка allure-results не найдена!")
    print("Сначала запустите тесты: pytest Test_Ui/test_cinescope.py --alluredir=./allure-results")
    exit(1)

# Ищем allure в системе
allure_cmd = None
for path in [
    "allure",
    r"C:\tools\allure\bin\allure.bat",
    r"C:\ProgramData\chocolatey\bin\allure.bat",
]:
    try:
        subprocess.run([path, "--version"], capture_output=True, check=True)
        allure_cmd = path
        break
    except:
        continue

if not allure_cmd:
    print("❌ Allure CLI не найден!")
    print("Установите Allure одним из способов:")
    print("1. choco install allure")
    print("2. npm install -g allure-commandline")
    print("3. Скачайте с https://github.com/allure-framework/allure2/releases")
    exit(1)

# Генерируем HTML-отчет
print("📊 Генерация отчета...")
subprocess.run([allure_cmd, "generate", str(results_dir), "-o", str(report_dir), "--clean"])

# Открываем в браузере
index_file = report_dir / "index.html"
if index_file.exists():
    print(f"✅ Отчет создан: {index_file}")
    print("🌐 Открываю в браузере...")
    webbrowser.open(f"file://{index_file.absolute()}")
else:
    print("❌ Не удалось создать отчет")