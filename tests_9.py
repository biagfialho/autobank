import time
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC

@pytest.mark.parametrize("browser", ["chrome", "firefox", "edge"])
def test_realizar_deposito(browser):
    # Setup do driver
    if browser == "chrome":
        driver = webdriver.Chrome()
    elif browser == "firefox":
        driver = webdriver.Firefox()
    elif browser == "edge":
        driver = webdriver.Edge()
    else:
        pytest.skip("Navegador não suportado.")

    wait = WebDriverWait(driver, 10)

    try:
        driver.get("https://www.globalsqa.com/angularJs-protractor/BankingProject/#/login")
        driver.maximize_window()

        # === Login como Cliente ===
        wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[ng-click='customer()']"))).click()
        Select(wait.until(EC.presence_of_element_located((By.ID, "userSelect")))).select_by_visible_text("Harry Potter")
        driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()

        # === Verificar informações da conta ===
        saldo_element = wait.until(EC.presence_of_element_located((By.XPATH, "//strong[2]")))
        saldo_inicial = int(saldo_element.text)

        # === Clicar na aba "Deposit" ===
        driver.find_element(By.CSS_SELECTOR, "button[ng-click='deposit()']").click()

        # === Inserir valor 1000 e confirmar ===
        valor_input = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "input[ng-model='amount']")))
        valor_input.send_keys("1000")
        driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()

        # === Verificar saldo atualizado ===
        time.sleep(1)  # espera pequena para atualização de saldo
        novo_saldo = int(driver.find_element(By.XPATH, "//strong[2]").text)
        assert novo_saldo == saldo_inicial + 1000, f"Saldo esperado: {saldo_inicial + 1000}, Saldo atual: {novo_saldo}"

        # === Confirmação visual da mensagem de sucesso ===
        msg = driver.find_element(By.CSS_SELECTOR, "span[ng-show='message']").text
        assert "Deposit Successful" in msg

    finally:
        driver.quit()
