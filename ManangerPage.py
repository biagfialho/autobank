from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC

from pycache.BasePage import BasePage


class ManagerPage(BasePage):
    url_manager = 'https://www.globalsqa.com/angularJs-protractor/BankingProject/#/manager'

    # Locators
    add_customer_button = (By.XPATH, "//button[@ng-click='addCust()']")
    open_account_button = (By.XPATH, "//button[@ng-click='openAccount()']")
    customers_button = (By.XPATH, "//button[@ng-click='showCust()']")
    first_name_input = (By.XPATH, "//input[@placeholder='First Name']")
    last_name_input = (By.XPATH, "//input[@placeholder='Last Name']")
    postcode_input = (By.XPATH, "//input[@placeholder='Post Code']")
    add_customer_submit = (By.XPATH, "//button[@type='submit']")
    customer_select = (By.ID, "userSelect")
    currency_select = (By.ID, "currency")
    process_button = (By.XPATH, "//button[@type='submit']")
    customers_table = (By.XPATH, "//table[@class='table table-bordered table-striped']")
    customers_table_rows = (By.XPATH, "//table[@class='table table-bordered table-striped']//tbody//tr")

    def __init__(self, browser=None, driver=None):
        super().__init__(driver=driver, browser=browser)

    def open_page(self):
        self.driver.get(self.url_manager)

    def click_add_customer_button(self):
        """Click the Add Customer button to open the form"""
        button = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(self.add_customer_button)
        )
        button.click()

    def fill_customer_form(self, first_name, last_name, postcode):
        """Fill the add customer form with provided data"""
        # Wait for form to be visible and fill fields
        first_name_field = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(self.first_name_input)
        )
        first_name_field.clear()
        first_name_field.send_keys(first_name)

        last_name_field = self.driver.find_element(*self.last_name_input)
        last_name_field.clear()
        last_name_field.send_keys(last_name)

        postcode_field = self.driver.find_element(*self.postcode_input)
        postcode_field.clear()
        postcode_field.send_keys(postcode)

    def submit_add_customer(self):
        """Submit the add customer form"""
        submit_button = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(self.add_customer_submit)
        )
        submit_button.click()

    def add_customer(self, first_name, last_name, postcode):
        """Complete flow: click Add Customer, fill form, and submit"""
        self.click_add_customer_button()
        self.fill_customer_form(first_name, last_name, postcode)
        self.submit_add_customer()

    def is_alert_present(self):
        """Check if success alert is present after adding customer"""
        try:
            WebDriverWait(self.driver, 5).until(EC.alert_is_present())
            return True
        except:
            return False

    def get_alert_text_and_accept(self):
        """Get alert text and accept it"""
        if self.is_alert_present():
            alert = self.driver.switch_to.alert
            alert_text = alert.text
            alert.accept()
            return alert_text
        return None

    def wait_and_assert_customer_added_alert(self):
        """Wait for customer addition alert, assert content, and click OK"""
        if self.is_alert_present():
            alert_text = self.get_alert_text_and_accept()
            # Assert the alert contains success message and customer ID
            assert "Customer added successfully" in alert_text, f"Expected success message, but got: {alert_text}"
            assert "customer id" in alert_text, f"Expected customer ID in alert, but got: {alert_text}"
            return alert_text
        else:
            raise AssertionError("Expected success alert after adding customer, but no alert was present")

    def wait_for_customer_added_success(self):
        """Wait for customer addition success and return True if successful"""
        if self.is_alert_present():
            alert_text = self.get_alert_text_and_accept()
            return "Customer added successfully" in alert_text or "added successfully" in alert_text
        return False

    def click_open_account_button(self):
        """Click the Open Account button to switch to account opening form"""
        button = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(self.open_account_button)
        )
        button.click()

    def get_available_customers_for_account(self):
        """Get list of all available customers in the Open Account dropdown"""
        customer_dropdown = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(self.customer_select)
        )
        select = Select(customer_dropdown)
        # Skip the first option which is "---Customer Name---"
        return [option.text for option in select.options if option.text != "---Customer Name---"]

    def select_customer_for_account(self, customer_name_contains):
        """Select a customer from the dropdown for opening account (partial match)"""
        customer_dropdown = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(self.customer_select)
        )
        select = Select(customer_dropdown)

        # Find customer by partial name match (case insensitive)
        for option in select.options:
            if customer_name_contains.lower() in option.text.lower():
                select.select_by_visible_text(option.text)
                print(f"✅ Selected customer: {option.text}")
                return option.text

        # If no match found, show available options
        available_customers = [opt.text for opt in select.options if opt.text != "---Customer Name---"]
        raise ValueError(
            f"Could not find customer containing '{customer_name_contains}'. Available customers: {available_customers}")

    def select_currency(self, currency):
        """Select currency from the dropdown"""
        currency_dropdown = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(self.currency_select)
        )
        select = Select(currency_dropdown)
        select.select_by_visible_text(currency)

    def click_process_button(self):
        """Click the Process button to create the account"""
        process_btn = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(self.process_button)
        )
        process_btn.click()

    def open_account_for_customer(self, customer_name_contains, currency):
        """Complete flow: click Open Account, select customer, select currency, and process"""
        self.click_open_account_button()
        selected_customer = self.select_customer_for_account(customer_name_contains)
        self.select_currency(currency)
        self.click_process_button()
        return selected_customer

    def wait_and_assert_account_created_alert(self):
        """Wait for account creation alert, assert content, and click OK"""
        if self.is_alert_present():
            alert_text = self.get_alert_text_and_accept()
            # Assert the alert contains success message and account number (case insensitive)
            assert "Account created successfully" in alert_text, f"Expected success message, but got: {alert_text}"
            assert "account number" in alert_text.lower(), f"Expected account number in alert, but got: {alert_text}"
            return alert_text
        else:
            raise AssertionError("Expected success alert after creating account, but no alert was present")

    def click_customers_button(self):
        """Click the Customers button to view customers table"""
        button = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(self.customers_button)
        )
        button.click()

    def wait_for_customers_table(self):
        """Wait for customers table to be visible"""
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(self.customers_table)
        )

    def get_customers_table_data(self):
        """Get all customer data from the table as a list of dictionaries"""
        self.wait_for_customers_table()

        customers = []
        rows = self.driver.find_elements(*self.customers_table_rows)

        for row in rows:
            cells = row.find_elements(By.TAG_NAME, "td")
            if len(cells) >= 4:  # Ensure we have all required columns
                customer = {
                    'first_name': cells[0].text.strip(),
                    'last_name': cells[1].text.strip(),
                    'post_code': cells[2].text.strip(),
                    'account_numbers': cells[3].text.strip().split()  # Split account numbers
                }
                customers.append(customer)

        return customers

    def find_customer_in_table(self, first_name, last_name):
        """Find a specific customer in the table and return their data"""
        customers = self.get_customers_table_data()

        for customer in customers:
            if (customer['first_name'].lower() == first_name.lower() and
                    customer['last_name'].lower() == last_name.lower()):
                return customer

        return None

    def verify_customer_in_table(self, first_name, last_name, expected_post_code, expected_account_number=None):
        """Verify that a customer exists in the table with correct data"""
        self.click_customers_button()
        customer = self.find_customer_in_table(first_name, last_name)

        if not customer:
            available_customers = [f"{c['first_name']} {c['last_name']}" for c in self.get_customers_table_data()]
            raise AssertionError(
                f"Customer '{first_name} {last_name}' not found in table. Available customers: {available_customers}")

        # Verify post code
        assert customer[
                   'post_code'] == expected_post_code, f"Expected post code '{expected_post_code}', but got '{customer['post_code']}'"

        # Verify account number if provided
        if expected_account_number:
            assert expected_account_number in customer[
                'account_numbers'], f"Expected account number '{expected_account_number}' not found in {customer['account_numbers']}"

        print(
            f"✅ Customer verified: {customer['first_name']} {customer['last_name']}, Post Code: {customer['post_code']}, Accounts: {customer['account_numbers']}")
        return customer
