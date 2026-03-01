import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from data.test_data import unique_email


@pytest.fixture(scope="function")
def new_email():
    """Fixture: уникальный email для каждого теста (гарантирует отсутствие конфликтов)."""
    return unique_email()


@pytest.fixture(scope="function")
def driver():
    options = webdriver.ChromeOptions()
    # options.add_argument("--headless")  # раскомментить для запуска без браузера
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    driver.maximize_window()
    yield driver
    driver.quit()
