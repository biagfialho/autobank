import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class Test4:

    def test_login_as_manager(self, setup):
        driver = setup

        # Voltar à tela de login (caso a fixture redirecione para /customer)
        driver.get("https://www.globalsqa.com/angularJs-protractor/BankingProject/#/login")

        # Etapa 1: Verificar se está na página de login
        assert "login" in driver.current_url, "Não está na página de login"

        # Etapa 2: Localizar o botão "Bank Manager Login"
        manager_login_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[text()='Bank Manager Login']"))
        )
        assert manager_login_button.is_displayed(), "Botão 'Bank Manager Login' não está visível"

        # Etapa 3: Clicar no botão
        manager_login_button.click()

        # Etapa 4: Aguardar r
