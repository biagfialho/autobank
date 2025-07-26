import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.edge.options import Options as EdgeOptions

# ✅ Fixture parametrizada para múltiplos navegadores
@pytest.fixture(params=["chrome", "firefox", "edge"])
def setup(request):
    browser = request.param
    driver = None

    if browser == "chrome":
        options = ChromeOptions()
        options.add_argument("--start-maximized")
        driver = webdriver.Chrome(options=options)

    elif browser == "firefox":
        options = FirefoxOptions()
        options.add_argument("--width=1920")
        options.add_argument("--height=1080")
        driver = webdriver.Firefox(options=options)

    elif browser == "edge":
        options = EdgeOptions()
        options.add_argument("--start-maximized")
        driver = webdriver.Edge(options=options)

    driver.get("https://www.globalsqa.com/angularJs-protractor/BankingProject/#/login")

    # Clicar no botão "Customer Login"
    customer_login_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//button[text()='Customer Login']"))
    )
    customer_login_button.click()

    WebDriverWait(driver, 10).until(EC.url_contains("/customer"))

    yield driver
    driver.quit()


class Test3:

    def test_validate_customer_dropdown(self, setup):
        driver = setup

        # Etapa 1: Localizar o dropdown
        customer_dropdown = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "userSelect"))
        )
        select = Select(customer_dropdown)

        # Etapa 2: Extrair todos os clientes
        customers = [option.text for option in select.options if option.text.strip()]
        print(f"Clientes encontrados: {customers}")

        # Etapa 3: Verificar presença dos clientes esperados
        assert "Harry Potter" in customers, "'Harry Potter' não está presente na lista"
        assert "Hermoine Granger" in customers, "'Hermoine Granger' não está presente na lista"

        # Etapa 4: Verificar quantidade mínima
        assert len(customers) >= 1, "Lista de clientes está vazia"
