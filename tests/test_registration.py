import pytest
import allure
import time
from pages.register_page import RegisterPage
from pages.login_page import LoginPage
from locators.register_page_locators import RegisterPageLocators
from data.test_data import (
    VALID_REGISTER, EXISTING_USER_EMAIL,
    INVALID_NAMES, INVALID_EMAILS, INVALID_PASSWORDS,
    unique_email
)


@allure.feature("Регистрация")
class TestRegistrationNavigation:

    @allure.title("Переход на страницу регистрации по ссылке со страницы авторизации")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_go_to_register_from_login(self, driver):
        page = LoginPage(driver)
        with allure.step("Открываем страницу авторизации"):
            page.open_login()
        with allure.step("Кликаем ссылку 'Зарегистрироваться'"):
            page.click_register_link()
        with allure.step("Проверяем переход на страницу регистрации"):
            assert "/register" in driver.current_url

    @allure.title("Страница регистрации доступна по прямой ссылке")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_register_page_available_by_direct_url(self, driver):
        page = RegisterPage(driver)
        with allure.step("Открываем /register напрямую"):
            page.open_register()
        with allure.step("Проверяем что страница открылась"):
            assert "/register" in driver.current_url

    @allure.title("Переход на страницу авторизации по ссылке 'Войти'")
    @allure.severity(allure.severity_level.NORMAL)
    def test_go_to_login_from_register(self, driver):
        page = RegisterPage(driver)
        with allure.step("Открываем страницу регистрации"):
            page.open_register()
        with allure.step("Кликаем ссылку 'Войти'"):
            page.click_login_link()
        with allure.step("Проверяем переход на страницу авторизации"):
            assert "/login" in driver.current_url


@allure.feature("Регистрация")
class TestRegistrationSuccess:

    @allure.title("Успешная регистрация → переход на страницу авторизации")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_successful_registration_redirects_to_login(self, driver):
        page = RegisterPage(driver)
        email = unique_email()
        with allure.step("Открываем страницу регистрации"):
            page.open_register()
        with allure.step(f"Заполняем имя: {VALID_REGISTER['name']}"):
            page.fill_name(VALID_REGISTER["name"])
        with allure.step(f"Заполняем уникальный email: {email}"):
            page.fill_email(email)
        with allure.step("Заполняем пароль"):
            page.fill_password(VALID_REGISTER["password"])
        with allure.step("Нажимаем 'Зарегистрироваться'"):
            page.click_register_button()
        with allure.step("Ожидаем редиректа и проверяем URL"):
            from selenium.webdriver.support.ui import WebDriverWait
            from selenium.webdriver.support import expected_conditions as EC
            WebDriverWait(driver, 10).until(EC.url_changes(
                "https://burger-frontend-1.prakticum-team.ru/register"
            ))
            assert "/login" in driver.current_url, (
                f"Ожидался редирект на /login, но URL = {driver.current_url}"
            )


@allure.feature("Регистрация")
class TestRegistrationNameValidation:

    @allure.title("Ошибка при невалидном имени: {reason}")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.parametrize("name,reason", INVALID_NAMES)
    def test_invalid_name_shows_error(self, driver, name, reason):
        page = RegisterPage(driver)
        email = unique_email()
        with allure.step("Открываем страницу регистрации"):
            page.open_register()
        with allure.step(f"Вводим невалидное имя ({reason})"):
            page.fill_name(name)
        with allure.step(f"Заполняем уникальный email: {email}"):
            page.fill_email(email)
        with allure.step("Заполняем пароль"):
            page.fill_password(VALID_REGISTER["password"])
        with allure.step("Нажимаем 'Зарегистрироваться' и ждём ответа"):
            page.click_register_button()
            time.sleep(2)
        with allure.step("Проверяем что остались на странице регистрации"):
            assert "/register" in driver.current_url, (
                f"Форма ушла со страницы регистрации (URL={driver.current_url}). "
                f"Ожидалась ошибка валидации для имени: '{name}'"
            )
        with allure.step("Проверяем текст ошибки под полем Имя"):
            assert page.is_visible(RegisterPageLocators.NAME_ERROR), (
                "Сообщение об ошибке 'Некорректное имя' не отображается"
            )
            assert page.get_name_error() == "Некорректное имя"


@allure.feature("Регистрация")
class TestRegistrationEmailValidation:

    @allure.title("Ошибка при невалидном email: {reason}")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.parametrize("email,reason", INVALID_EMAILS)
    def test_invalid_email_shows_error(self, driver, email, reason):
        page = RegisterPage(driver)
        with allure.step("Открываем страницу регистрации"):
            page.open_register()
        with allure.step("Заполняем поле Имя"):
            page.fill_name(VALID_REGISTER["name"])
        with allure.step(f"Вводим невалидный email ({reason})"):
            page.fill_email(email)
        with allure.step("Заполняем поле Пароль"):
            page.fill_password(VALID_REGISTER["password"])
        with allure.step("Нажимаем 'Зарегистрироваться' и ждём ответа"):
            page.click_register_button()
            time.sleep(2)
        with allure.step("Проверяем что остались на странице регистрации"):
            assert "/register" in driver.current_url, (
                f"Форма ушла со страницы (URL={driver.current_url}). "
                f"Ожидалась ошибка для email: '{email}'"
            )
        with allure.step("Проверяем текст ошибки под полем Email"):
            assert page.is_visible(RegisterPageLocators.EMAIL_ERROR), (
                "Сообщение об ошибке 'Некорректный e-mail' не отображается"
            )
            assert page.get_email_error() == "Некорректный e-mail"

    @allure.title("Ошибка при регистрации с уже существующим email")
    @allure.severity(allure.severity_level.NORMAL)
    def test_existing_email_shows_error(self, driver):
        page = RegisterPage(driver)
        with allure.step("Открываем страницу регистрации"):
            page.open_register()
        with allure.step("Заполняем имя"):
            page.fill_name(VALID_REGISTER["name"])
        with allure.step(f"Вводим уже зарегистрированный email: {EXISTING_USER_EMAIL}"):
            page.fill_email(EXISTING_USER_EMAIL)
        with allure.step("Заполняем пароль"):
            page.fill_password(VALID_REGISTER["password"])
        with allure.step("Нажимаем 'Зарегистрироваться' и ждём ответа"):
            page.click_register_button()
            time.sleep(3)
        with allure.step("Проверяем текст ошибки"):
            assert page.is_visible(RegisterPageLocators.EMAIL_ERROR), (
                "Сообщение 'Такой пользователь уже существует' не отображается"
            )
            assert page.get_email_error() == "Такой пользователь уже существует"


@allure.feature("Регистрация")
class TestRegistrationPasswordValidation:

    @allure.title("Ошибка при невалидном пароле: {reason}")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.parametrize("password,reason", INVALID_PASSWORDS)
    def test_invalid_password_shows_error(self, driver, password, reason):
        page = RegisterPage(driver)
        email = unique_email()
        with allure.step("Открываем страницу регистрации"):
            page.open_register()
        with allure.step("Заполняем имя"):
            page.fill_name(VALID_REGISTER["name"])
        with allure.step(f"Заполняем уникальный email: {email}"):
            page.fill_email(email)
        with allure.step(f"Вводим невалидный пароль ({reason})"):
            page.fill_password(password)
        with allure.step("Нажимаем 'Зарегистрироваться' и ждём ответа"):
            page.click_register_button()
            time.sleep(2)
        with allure.step("Проверяем что остались на странице регистрации"):
            assert "/register" in driver.current_url, (
                f"Форма ушла со страницы (URL={driver.current_url}). "
                f"Ожидалась ошибка для пароля: '{password[:10]}...'"
            )
        with allure.step("Проверяем текст ошибки под полем Пароль"):
            assert page.is_visible(RegisterPageLocators.PASSWORD_ERROR), (
                "Сообщение об ошибке 'Некорректный пароль' не отображается"
            )
            assert page.get_password_error() == "Некорректный пароль"


@allure.feature("Регистрация")
class TestPasswordVisibilityToggle:

    @allure.title("По умолчанию пароль скрыт")
    @allure.severity(allure.severity_level.MINOR)
    def test_password_hidden_by_default(self, driver):
        page = RegisterPage(driver)
        with allure.step("Открываем страницу регистрации"):
            page.open_register()
        with allure.step("Вводим пароль"):
            page.fill_password(VALID_REGISTER["password"])
        with allure.step("Проверяем что тип поля — password"):
            assert page.get_password_input_type() == "password"

    @allure.title("Клик на иконку показывает пароль")
    @allure.severity(allure.severity_level.MINOR)
    def test_password_toggle_shows_password(self, driver):
        page = RegisterPage(driver)
        with allure.step("Открываем страницу регистрации"):
            page.open_register()
        with allure.step("Вводим пароль"):
            page.fill_password(VALID_REGISTER["password"])
        with allure.step("Кликаем кнопку показа пароля"):
            page.click_password_toggle()
        with allure.step("Проверяем что тип поля изменился на text"):
            assert page.get_password_input_type() == "text"

    @allure.title("Повторный клик снова скрывает пароль")
    @allure.severity(allure.severity_level.MINOR)
    def test_password_toggle_hides_password_again(self, driver):
        page = RegisterPage(driver)
        with allure.step("Открываем страницу регистрации"):
            page.open_register()
        with allure.step("Вводим пароль"):
            page.fill_password(VALID_REGISTER["password"])
        with allure.step("Первый клик — показываем пароль"):
            page.click_password_toggle()
            assert page.get_password_input_type() == "text"
        with allure.step("Второй клик — скрываем пароль"):
            page.click_password_toggle()
        with allure.step("Проверяем что тип поля снова password"):
            assert page.get_password_input_type() == "password"
