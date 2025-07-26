from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC

from pycache.BasePage import BasePage


class CustomerPage(BasePage):
    url_customer = 'https://www.globalsqa.com/angularJs-protractor/BankingProject/#/customer'

    # Locators
    customer_dropdown = (By.ID, "userSelect")
    login_button = (By.XPATH, "//button[@type='submit' and text()='Login']")

    def __init__(self, browser=None, driver=None):
        super().__init__(driver=driver, browser=browser)

    def open_page(self):
        self.driver.get(self.url_customer)

    def select_customer(self, customer_name):
        """Select a customer from the dropdown by name"""
        # Wait for dropdown to be present
        dropdown_element = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(self.customer_dropdown)
        )

        # Create Select object and select by visible text
        select = Select(dropdown_element)
        select.select_by_visible_text(customer_name)

        # Wait for login button to become visible (it appears after selection)
        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(self.login_button)
        )

    def click_login(self):
        """Click the login button after customer selection"""
        login_btn = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(self.login_button)
        )
        login_btn.click()

    def select_customer_and_login(self, customer_name):
        """Complete flow: select customer and login"""
        self.select_customer(customer_name)
        self.click_login()

        # Wait for navigation to account page
        WebDriverWait(self.driver, 10).until(
            EC.url_contains("/account")
        )

    def get_available_customers(self):
        """Get list of all available customer names"""
        dropdown_element = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(self.customer_dropdown)
        )

        select = Select(dropdown_element)
        # Skip the first option which is "---Your Name---"
        return [option.text for option in select.options if option.text != "---Your Name---"]

    def is_url_account(self):
        """Check if current URL is the account page"""
        return self.driver.current_url == 'https://www.globalsqa.com/angularJs-protractor/BankingProject/#/account'

    def wait_for_account_page(self):
        """Wait for navigation to account page and verify URL"""
        WebDriverWait(self.driver, 10).until(
            EC.url_contains("/account")
        )
        return self.is_url_account()

    def is_login_button_clickable(self):
        """Check if login button is clickable after customer selection"""
        try:
            WebDriverWait(self.driver, 5).until(
                EC.element_to_be_clickable(self.login_button)
            )
            return True
        except:
            return False