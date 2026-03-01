from pages.base_page import BasePage
from locators.register_page_locators import RegisterPageLocators


class RegisterPage(BasePage):

    def open_register(self):
        self.open("/register")

    def fill_name(self, name):
        self.find(RegisterPageLocators.NAME_INPUT).send_keys(name)

    def fill_email(self, email):
        self.find(RegisterPageLocators.EMAIL_INPUT).send_keys(email)

    def fill_password(self, password):
        self.find(RegisterPageLocators.PASSWORD_INPUT).send_keys(password)

    def click_register_button(self):
        self.click(RegisterPageLocators.REGISTER_BUTTON)

    def click_login_link(self):
        self.click(RegisterPageLocators.LOGIN_LINK)

    def click_password_toggle(self):
        import time
        from selenium.webdriver.support import expected_conditions as EC
        element = self.wait.until(EC.element_to_be_clickable(RegisterPageLocators.PASSWORD_TOGGLE))
        self.driver.execute_script("arguments[0].click();", element)
        time.sleep(0.5)

    def get_name_error(self):
        return self.get_text(RegisterPageLocators.NAME_ERROR)

    def get_email_error(self):
        return self.get_text(RegisterPageLocators.EMAIL_ERROR)

    def get_password_error(self):
        return self.get_text(RegisterPageLocators.PASSWORD_ERROR)

    def get_password_input_type(self):
        return self.find(RegisterPageLocators.PASSWORD_INPUT).get_attribute("type")

    def register(self, name, email, password):
        self.open_register()
        self.fill_name(name)
        self.fill_email(email)
        self.fill_password(password)
        self.click_register_button()
