from selenium.webdriver.common.by import By


class MainPageLocators:
    HEADER = (By.TAG_NAME, "h1")
    CONSTRUCTOR_LINK = (By.LINK_TEXT, "Конструктор")
    FEED_LINK = (By.LINK_TEXT, "Лента заказов")
    LOGIN_BUTTON = (By.LINK_TEXT, "Войти в аккаунт")
