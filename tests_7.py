import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select


@pytest.mark.parametrize("browser", ["chrome", "firefox", "edge"])
def test_manager_full_flow(browser):
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

        # 1. Clicar no botão "Bank Manager Login"
        manager_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[ng-click='manager()']")))
        manager_button.click()

        # 2. Clicar no botão "Add Customer"
        add_customer_btn = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[ng-class='btnClass1']")))
        add_customer_btn.click()

        # 3. Preencher campos com os dados
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "input[ng-model='fName']"))).send_keys("John")
        driver.find_element(By.CSS_SELECTOR, "input[ng-model='lName']").send_keys("Doe")
        driver.find_element(By.CSS_SELECTOR, "input[ng-model='postCd']").send_keys("12345")

        # 4. Clicar no botão "Add Customer" para submeter
        driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()

        # 5. Verificar mensagem de sucesso
        alert = wait.until(EC.alert_is_present())
        assert "Customer added successfully" in alert.text
        alert.accept()

        # 6. Criar conta para o cliente
        open_account_btn = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[ng-class='btnClass2']")))
        open_account_btn.click()

        # Selecionar cliente e moeda
        user_select = wait.until(EC.presence_of_element_located((By.ID, "userSelect")))
        Select(user_select).select_by_visible_text("John Doe")
        Select(driver.find_element(By.ID, "currency")).select_by_visible_text("Dollar")

        # Submeter criação da conta
        driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()

        # 7. Extrair número da conta do alerta
        alert = wait.until(EC.alert_is_present())
        assert "Account created successfully" in alert.text
        alert_text = alert.text
        account_number = ''.join(filter(str.isdigit, alert_text))
        assert account_number != "", "Número da conta não encontrado no alerta"
        alert.accept()

        # 8. Verificar cliente na aba "Customers"
        customers_btn = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[ng-class='btnClass3']")))
        customers_btn.click()

        # Aguarda a tabela aparecer
        table = wait.until(EC.presence_of_element_located((By.TAG_NAME, "table")))
        table_rows = table.find_elements(By.XPATH, ".//tbody/tr")

        cliente_encontrado = False
        for row in table_rows:
            cols = row.find_elements(By.TAG_NAME, "td")
            if (
                cols[0].text == "John" and
                cols[1].text == "Doe" and
                cols[2].text == "12345"
            ):
                cliente_encontrado = True
                break

        assert cliente_encontrado, "Cliente 'John Doe' não encontrado na tabela de clientes"

    finally:
        driver.quit()
