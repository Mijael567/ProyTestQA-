"""
conftest.py - Configuración compartida de pytest para tests_selenium_generados
Define fixtures y configuración global para todos los tests
"""

import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


@pytest.fixture(scope="function")
def driver():
    """
    Fixture que proporciona una instancia de WebDriver Chrome
    Se crea antes de cada test y se cierra después
    """
    chrome_service = Service(ChromeDriverManager().install())
    options = webdriver.ChromeOptions()
    options.add_argument("--window-size=1400,900")
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-extensions")
    options.add_argument("--no-sandbox")
    
    driver = webdriver.Chrome(service=chrome_service, options=options)
    driver.maximize_window()
    
    yield driver
    
    driver.quit()


def pytest_configure(config):
    """Hook que se ejecuta antes de correr los tests"""
    print("\n" + "="*70)
    print("SUITE DE TESTS SELENIUM - POLLOS EXPRESS")
    print("URL Base: http://localhost/sistema/public/")
    print("="*70 + "\n")
