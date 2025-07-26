import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.chrome.options import Options
import time


@pytest.mark.parametrize("browser", ["chrome", "firefox", "edge"])
def test_add_existing_customer(browser):
    # Setup do driver com base no navegador
    if browser == "chrome":
        driver = webdriver.Chrome()
    elif browser == "firefox":
        driver = webdriver.Firefox()
    elif browser == "edge":
        driver = webdriver.Edge()
    else:
        pytest.skip("Navegador não suportado")

    try:
        driver.get("https://www.globalsqa.com/angularJs-protractor/BankingProject/#/login")
        driver.maximize_window()
        time.sleep(1)

        # Passo 1: Clicar em "Bank Manager Login"
        driver.find_element(By.CSS_SELECTOR, "button[ng-click='manager()']").click()
        time.sleep(1)

        # Passo 2: Clicar em "Add Customer"
        driver.find_element(By.CSS_SELECTOR, "button[ng-class='btnClass1']").click()
        time.sleep(1)

        # Passo 3-5: Preencher dados do cliente já existente
        driver.find_element(By.CSS_SELECTOR, "input[ng-model='fName']").send_keys("Ron")
        driver.find_element(By.CSS_SELECTOR, "input[ng-model='lName']").send_keys("Weasly")
        driver.find_element(By.CSS_SELECTOR, "input[ng-model='postCd']").send_keys("E55555")

        # Passo 6: Clicar em "Add Customer"
        driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
        time.sleep(1)

        # Captura do alerta
        alert = Alert(driver)
        alert_text = alert.text

        # Validação da mensagem de erro
        assert "Customer may be duplicate" in alert_text, f"Texto inesperado no alerta: {alert_text}"
        alert.accept()

    finally:
        driver.quit()
