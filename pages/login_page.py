from pages.base_page import BasePage
from locators.login_page_locators import LoginPageLocators


class LoginPage(BasePage):

    def open_login(self):
        self.open("/login")

    def enter_email(self, email):
        self.find(LoginPageLocators.EMAIL_INPUT).send_keys(email)

    def enter_password(self, password):
        self.find(LoginPageLocators.PASSWORD_INPUT).send_keys(password)

    def click_login_button(self):
        self.click(LoginPageLocators.LOGIN_BUTTON)

    def click_register_link(self):
        self.click(LoginPageLocators.REGISTER_LINK)

    def find_register_link(self):
        return LoginPageLocators.REGISTER_LINK

    def login(self, email, password):
        self.open_login()
        self.enter_email(email)
        self.enter_password(password)
        self.click_login_button()
