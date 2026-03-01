from pages.base_page import BasePage
from locators.main_page_locators import MainPageLocators


class MainPage(BasePage):

    def open_main(self):
        self.open("/")

    def get_header_text(self):
        return self.get_text(MainPageLocators.HEADER)
