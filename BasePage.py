from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class BasePage:
    # Common locators
    home_button = (By.XPATH, "//button[@class='btn home' and @ng-click='home()']")

    def __init__(self, driver, browser=None):
        if driver:
            self.driver = driver
        elif browser:
            if browser == 'chrome':
                options = Options()
                options.add_argument("--incognito")
                # options.add_argument("--headless")
                self.driver = webdriver.Chrome(options=options)
            elif browser == 'firefox':
                self.driver = webdriver.Firefox()
            elif browser == 'edge':
                self.driver = webdriver.Edge()
            else:
                raise Exception('Browser não suportado!')
        else:
            # Neither driver nor browser provided - driver will be set manually later
            self.driver = None

    def is_url(self, url):
        return self.driver.current_url == url

    def click_home_button(self):
        """Click the Home button to return to the main login page"""
        button = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(self.home_button)
        )
        button.click()
        # Wait for navigation to login page
        WebDriverWait(self.driver, 10).until(
            EC.url_contains("/login")
        )

    def close(self):
        self.driver.quit()