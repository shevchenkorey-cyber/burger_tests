from selenium.webdriver.common.by import By


class RegisterPageLocators:
    NAME_INPUT = (By.NAME, "name")
    EMAIL_INPUT = (By.NAME, "email")
    PASSWORD_INPUT = (By.NAME, "password")
    REGISTER_BUTTON = (By.XPATH, "//button[text()='Зарегистрироваться']")
    LOGIN_LINK = (By.LINK_TEXT, "Войти")
    PASSWORD_TOGGLE = (By.XPATH, "//div[contains(@class,'input__icon-action')]")

    # Сообщения об ошибках
    NAME_ERROR = (By.XPATH, "//input[@name='name']/ancestor::div[contains(@class,'input')]//p[contains(@class,'input__error')]")
    EMAIL_ERROR = (By.XPATH, "//input[@name='email']/ancestor::div[contains(@class,'input')]//p[contains(@class,'input__error')]")
    PASSWORD_ERROR = (By.XPATH, "//input[@name='password']/ancestor::div[contains(@class,'input')]//p[contains(@class,'input__error')]")
