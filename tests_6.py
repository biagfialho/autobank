import pytest

# test_open_account.py
import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC

class Test6:

    def test_create_account_for_existing_customer(self, setup):
        driver = setup
        driver.get("https://www.globalsqa.com/angularJs-protractor/BankingProject/#/login")

        # Etapa 1: Entrar como gerente
        manager_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[text()='Bank Manager Login']"))
        )
        manager_button.click()
        WebDriverWait(driver, 10).until(EC.url_contains("/manager"))

        # Etapa 2: Clicar na aba "Open Account"
        open_account_tab = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[@ng-class='btnClass2']"))
        )
        open_account_tab.click()

        # Etapa 3: Selecionar cliente "Ron Weasly"
        customer_dropdown = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "userSelect"))
        )
        select_customer = Select(customer_dropdown)
        select_customer.select_by_visible_text("Ron Weasly")
        assert select_customer.first_selected_option.text == "Ron Weasly"

        # Etapa 4: Selecionar moeda "Dollar"
        currency_dropdown = Select(driver.find_element(By.ID, "currency"))
        currency_dropdown.select_by_visible_text("Dollar")
        assert currency_dropdown.first_selected_option.text == "Dollar"

        # Etapa 5: Clicar no botão "Process"
        process_button = driver.find_element(By.XPATH, "//button[text()='Process']")
        process_button.click()

        # Etapa 6: Validar alerta de sucesso
        WebDriverWait(driver, 10).until(EC.alert_is_present())
        alert = driver.switch_to.alert
        alert_text = alert.text
        assert "Account created successfully" in alert_text, "Texto do alerta inesperado"
        alert.accept()


        # Assert the account creation success alert and click OK
        print(f"✅ Account opened successfully for Ron Weasly! Alert message: {alert_text}")
