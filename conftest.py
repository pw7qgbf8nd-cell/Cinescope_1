import email
from unittest.mock import DEFAULT
from pathlib import Path
from datetime import datetime
import pytest
from playwright.sync_api import sync_playwright
from types import SimpleNamespace
import pytest
from utils import DataGenerator

DEFAULT_UI_TIMEOUT = 30000

@pytest.fixture(scope="function")
def registered_user():
    return SimpleNamespace(
        email="test223@email.qa",
        password="OLEG_AQA25",
        feedback=DataGenerator.generate_random_feedback()
    )
@pytest.fixture(scope="function")
def new_user():
    return SimpleNamespace(
        email=DataGenerator.generate_random_email(),
        password=DataGenerator.generate_random_password(),
        full_name=DataGenerator.generate_random_name()
    )


@pytest.fixture(scope="session") # Браузер запускается один раз для всей сессии
def browser(playwright):
    browser = playwright.chromium.launch(headless=False) # headless=True для CI/CD, headless=False для локальной разработки
    yield browser # yield возвращает значение фикстуры, выполнение теста продолжится после yield
    browser.close() # Браузер закрывается после завершения всех тестов

@pytest.fixture(scope="function") # Контекст создается для каждого теста
def context(browser):
    context = browser.new_context()
    context.tracing.start(screenshots=True, snapshots=True, sources=True)# Трассировка для отладки
    context.set_default_timeout(DEFAULT_UI_TIMEOUT) # Установка таймаута по умолчанию
    yield context # yield возвращает значение фикстуры, выполнение теста продолжится после yield
    context.close() # Контекст закрывается после завершения теста

@pytest.fixture(scope="function")# Страница создается для каждого теста
def page(context):
    page = context.new_page()
    yield page # yield возвращает значение фикстуры, выполнение теста продолжится после yield
    page.close() # Страница закрывается после завершения теста

@pytest.fixture(scope="function")
def context(browser):
    context = browser.new_context()
    context.tracing.start(screenshots=True, snapshots=True, sources=True)
    context.set_default_timeout(DEFAULT_UI_TIMEOUT)
    yield context
    log_name = f"trace_{Tools.get_timestamp()}.zip"
    trace_path = Tools.files_dir('playwright_trace', log_name)
    context.tracing.stop(path=trace_path)
    context.close()

class Tools:
    @staticmethod
    def project_dir():
        """
        Возвращает корневую директорию проекта.
        Предполагается, что текущий файл находится в поддиректории `common`.
        """
        return Path(__file__).parent.parent

    @staticmethod
    def files_dir(nested_directory: str = None, filename: str = None):
        """
        Возвращает путь к директории `files` (или её поддиректории).
        Если директория не существует, она создается.
        Если указан `filename`, возвращает полный путь к файлу.
        """
        files_path = Tools.project_dir() / "files"
        if nested_directory:
            files_path = files_path / nested_directory
        files_path.mkdir(parents=True, exist_ok=True)

        if filename:
            return files_path / filename
        return files_path

    @staticmethod
    def get_timestamp():
        """
        Возвращает текущую временную метку в формате YYYY-MM-DD_HH-MM-SS.
        """
        return datetime.now().strftime("%Y-%m-%d_%H-%M-%S")