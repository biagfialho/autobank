from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from pycache.BasePage import BasePage
from pycache.CustomerPage import CustomerPage


class LoginPage(BasePage):
    url_login = 'https://www.globalsqa.com/angularJs-protractor/BankingProject/#/login'
    customer_login_button = (By.XPATH, "//button[text()='Customer Login']")
    manager_login_button = (By.XPATH, "//button[text()='Bank Manager Login']")

    def __init__(self, browser):
        super().__init__(driver=None, browser=browser)

    def open_page(self):
        self.driver.get(self.url_login)

    def is_url_login(self):
        return self.is_url(self.url_login)

    def is_url_customer(self):
        return self.driver.current_url == 'https://www.globalsqa.com/angularJs-protractor/BankingProject/#/customer'

    def is_url_manager(self):
        return self.driver.current_url == 'https://www.globalsqa.com/angularJs-protractor/BankingProject/#/manager'

    def wait_for_customer_page(self):
        """Wait for navigation to customer page after clicking Customer Login"""
        WebDriverWait(self.driver, 10).until(
            EC.url_contains("/customer")
        )
        return self.is_url_customer()

    def wait_for_manager_page(self):
        """Wait for navigation to manager page after clicking Bank Manager Login"""
        WebDriverWait(self.driver, 10).until(
            EC.url_contains("/manager")
        )
        return self.is_url_manager()

    def click_login_button(self):
        button = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(self.customer_login_button)
        )
        button.click()

    def click_manager_login_button(self):
        """Click the Bank Manager Login button"""
        button = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(self.manager_login_button)
        )
        button.click()

    def navigate_to_customer_page(self):
        self.click_login_button()
        self.wait_for_customer_page()
        return CustomerPage(driver=self.driver, browser=None)
