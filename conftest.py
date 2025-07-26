import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.edge.options import Options as EdgeOptions

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

    else:
        raise ValueError(f"Navegador não suportado: {browser}")

    # Etapa comum para todos os testes: ir à página inicial e clicar em "Customer Login"
    driver.get("https://www.globalsqa.com/angularJs-protractor/BankingProject/#/login")

    customer_login_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//button[text()='Customer Login']"))
    )
    customer_login_button.click()

    WebDriverWait(driver, 10).until(
        EC.url_contains("/customer")
    )

    yield driver
    driver.quit()
