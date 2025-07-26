# test_add_customer.py
import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class Test5:

    def test_add_new_customer(self, setup):
        driver = setup
        driver.get("https://www.globalsqa.com/angularJs-protractor/BankingProject/#/login")

        # Etapa 1: Entrar como gerente
        manager_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[text()='Bank Manager Login']"))
        )
        manager_button.click()
        WebDriverWait(driver, 10).until(EC.url_contains("/manager"))

        # Etapa 2: Clicar no botão "Add Customer"
        add_customer_tab = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[@ng-class='btnClass1']"))
        )
        add_customer_tab.click()

        # Etapa 3: Preencher o formulário
        first_name_input = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, "//input[@placeholder='First Name']"))
        )
        last_name_input = driver.find_element(By.XPATH, "//input[@placeholder='Last Name']")
        post_code_input = driver.find_element(By.XPATH, "//input[@placeholder='Post Code']")

        first_name_input.send_keys("John")
        last_name_input.send_keys("Doe")
        post_code_input.send_keys("12345")

        # Etapa 4: Submeter o formulário
        add_button = driver.find_element(By.XPATH, "//button[@type='submit']")
        add_button.click()

        # Etapa 5: Capturar e validar o alerta
        WebDriverWait(driver, 10).until(EC.alert_is_present())
        alert = driver.switch_to.alert
        alert_text = alert.text

        assert "Customer added successfully" in alert_text, "Texto do alerta inesperado"
        alert.accept()
