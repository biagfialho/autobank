from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


class Test2:
    # Inicia o navegador
    driver = webdriver.Chrome()
    driver.get("https://www.globalsqa.com/angularJs-protractor/BankingProject/#/login")

    try:
        wait = WebDriverWait(driver, 10)

        # Clica em "Customer Login"
        customer_login_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Customer Login')]")))
        customer_login_btn.click()

        # Aguarda o dropdown dos clientes
        dropdown = wait.until(EC.presence_of_element_located((By.ID, "userSelect")))

        # Seleciona o cliente "Harry Potter"
        from selenium.webdriver.support.ui import Select
        select = Select(dropdown)
        select.select_by_visible_text("Harry Potter")

        # Clica no botão "Login"
        login_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@type='submit']")))
        login_btn.click()

        # Verifica se o login foi bem-sucedido
        welcome_message = wait.until(EC.presence_of_element_located((By.XPATH, "//strong[contains(text(), 'Harry Potter')]")))
        assert "Harry Potter" in welcome_message.text
        print("✅ Teste CT-002 passou com sucesso!")

    finally:
        time.sleep(2)
        driver.quit()
