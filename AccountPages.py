from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC

from pycache.BasePage import BasePage


class AccountPage(BasePage):
    url_account = 'https://www.globalsqa.com/angularJs-protractor/BankingProject/#/account'

    # Locators
    welcome_message = (By.XPATH, "//strong[contains(text(), 'Welcome')]")
    customer_name = (By.XPATH, "//span[@class='fontBig ng-binding']")
    account_select = (By.ID, "accountSelect")
    account_number_display = (By.XPATH, "//div[contains(text(), 'Account Number')]/strong[1]")
    balance_display = (By.XPATH, "//div[contains(text(), 'Account Number')]/strong[2]")
    currency_display = (By.XPATH, "//div[contains(text(), 'Account Number')]/strong[3]")

    # Tab buttons
    transactions_button = (By.XPATH, "//button[@ng-click='transactions()']")
    deposit_button = (By.XPATH, "//button[@ng-click='deposit()']")
    withdrawl_button = (By.XPATH, "//button[@ng-click='withdrawl()']")

    # Deposit form (appears after clicking deposit)
    amount_input = (By.XPATH, "//input[@placeholder='amount']")
    deposit_submit_button = (By.XPATH, "//button[@type='submit' and text()='Deposit']")
    deposit_success_message = (By.XPATH, "//span[contains(text(), 'Deposit Successful')]")

    def __init__(self, browser=None, driver=None):
        super().__init__(driver=driver, browser=browser)

    def open_page(self):
        self.driver.get(self.url_account)

    def is_url_account(self):
        return self.is_url(self.url_account)

    def wait_for_account_page(self):
        """Wait for account page to load"""
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(self.welcome_message)
        )
        return True

    def get_customer_name(self):
        """Get the customer name from welcome message"""
        element = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(self.customer_name)
        )
        return element.text.strip()

    def get_available_accounts(self):
        """Get list of available account numbers"""
        account_dropdown = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(self.account_select)
        )
        select = Select(account_dropdown)
        return [option.text for option in select.options]

    def select_account(self, account_number):
        """Select an account from the dropdown"""
        account_dropdown = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(self.account_select)
        )
        select = Select(account_dropdown)
        select.select_by_visible_text(str(account_number))

        # Wait for account info to update
        WebDriverWait(self.driver, 5).until(
            lambda driver: self.get_current_account_number() == str(account_number)
        )

    def get_current_account_number(self):
        """Get the currently selected account number"""
        element = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(self.account_number_display)
        )
        return element.text.strip()

    def get_current_balance(self):
        """Get the current balance as a float"""
        element = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(self.balance_display)
        )
        balance_text = element.text.strip()
        return float(balance_text)

    def get_current_currency(self):
        """Get the current currency"""
        element = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(self.currency_display)
        )
        return element.text.strip()

    def click_deposit_button(self):
        """Click the Deposit tab button"""
        button = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(self.deposit_button)
        )
        button.click()

        # Wait for deposit form to appear
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(self.amount_input)
        )

    def enter_deposit_amount(self, amount):
        """Enter amount in the deposit form"""
        amount_field = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(self.amount_input)
        )
        amount_field.clear()
        amount_field.send_keys(str(amount))

    def click_deposit_submit(self):
        """Click the Deposit submit button"""
        submit_button = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(self.deposit_submit_button)
        )
        submit_button.click()

    def wait_for_deposit_success(self):
        """Wait for deposit success message"""
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(self.deposit_success_message)
        )
        return True

    def make_deposit(self, amount):
        """Complete deposit flow: click deposit, enter amount, submit, wait for success"""
        initial_balance = self.get_current_balance()
        print(f"💰 Initial balance: {initial_balance}")

        self.click_deposit_button()
        self.enter_deposit_amount(amount)
        self.click_deposit_submit()
        self.wait_for_deposit_success()

        # Wait for balance to update
        expected_balance = initial_balance + float(amount)
        WebDriverWait(self.driver, 10).until(
            lambda driver: self.get_current_balance() == expected_balance
        )

        final_balance = self.get_current_balance()
        print(f"💰 Final balance after depositing {amount}: {final_balance}")
        return final_balance

    def click_transactions_button(self):
        """Click the Transactions tab button"""
        button = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(self.transactions_button)
        )
        button.click()

    def click_withdrawl_button(self):
        """Click the Withdrawl tab button"""
        button = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(self.withdrawl_button)
        )
        button.click()

    def get_account_info(self):
        """Get complete account information"""
        return {
            'customer_name': self.get_customer_name(),
            'account_number': self.get_current_account_number(),
            'balance': self.get_current_balance(),
            'currency': self.get_current_currency(),
            'available_accounts': self.get_available_accounts()
        }