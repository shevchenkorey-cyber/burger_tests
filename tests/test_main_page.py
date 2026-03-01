import allure
from pages.main_page import MainPage


@allure.feature("Главная страница")
class TestMainPage:

    @allure.title("Открытие главной страницы")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_main_page_opens(self, driver):
        page = MainPage(driver)
        with allure.step("Открываем главную страницу"):
            page.open_main()
        with allure.step("Проверяем что страница открылась"):
            assert "burger" in driver.current_url.lower() or driver.title != ""
