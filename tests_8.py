import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC


@pytest.mark.parametrize("browser", ["chrome", "firefox", "edge"])
def test_end_to_end_cliente_login(browser):
    # Setup dos drivers
    if browser == "chrome":
        driver = webdriver.Chrome()
    elif browser == "firefox":
        driver = webdriver.Firefox()
    elif browser == "edge":
        driver = webdriver.Edge()
    else:
        pytest.skip("Navegador não suportado")

    wait = WebDriverWait(driver, 10)

    try:
        driver.get("https://www.globalsqa.com/angularJs-protractor/BankingProject/#/login")
        driver.maximize_window()

        # === Parte 1: Gerente cria cliente ===
        wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[ng-click='manager()']"))).click()
        wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[ng-class='btnClass1']"))).click()

        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "input[ng-model='fName']"))).send_keys("John")
        driver.find_element(By.CSS_SELECTOR, "input[ng-model='lName']").send_keys("Doe")
        driver.find_element(By.CSS_SELECTOR, "input[ng-model='postCd']").send_keys("12345")
        driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()

        alert = wait.until(EC.alert_is_present())
        assert "Customer added successfully" in alert.text
        alert.accept()

        # === Parte 2: Criar conta para o cliente ===
        wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[ng-class='btnClass2']"))).click()
        Select(wait.until(EC.presence_of_element_located((By.ID, "userSelect")))).select_by_visible_text("John Doe")
        Select(driver.find_element(By.ID, "currency")).select_by_visible_text("Dollar")
        driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()

        alert = wait.until(EC.alert_is_present())
        assert "Account created successfully" in alert.text
        alert.accept()

        # === Parte 3: Voltar para a página inicial ===
        wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "home"))).click()

        # === Parte 4: Login como cliente ===
        wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[ng-click='customer()']"))).click()
        Select(wait.until(EC.presence_of_element_located((By.ID, "userSelect")))).select_by_visible_text("John Doe")
        driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()

        # === Parte 5: Verificação da página de conta ===
        welcome = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "fontBig")))
        assert welcome.text.strip() == "John Doe"

        account_dropdown = wait.until(EC.presence_of_element_located((By.ID, "accountSelect")))
        assert account_dropdown.is_displayed()

    finally:
        driver.quit()
