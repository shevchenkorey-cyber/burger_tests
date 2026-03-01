from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)
wait = WebDriverWait(driver, 10)

# === ТЕСТ 1: Куда редиректит после успешной регистрации ===
print("=== Успешная регистрация: куда ведёт редирект ===")
ts = int(time.time())
driver.get("https://burger-frontend-1.prakticum-team.ru/register")
wait.until(EC.presence_of_element_located((By.NAME, "name")))
driver.find_element(By.NAME, "name").send_keys("Андрей")
driver.find_element(By.NAME, "email").send_keys(f"success_{ts}@test.com")
driver.find_element(By.NAME, "password").send_keys("Test1234!")
driver.find_element(By.XPATH, "//button[text()='Зарегистрироваться']").click()
time.sleep(3)
print("  URL после регистрации:", driver.current_url)

# === ТЕСТ 2: Короткий пароль ===
print("\n=== Невалидный пароль 5 символов - URL и ошибка ===")
driver.get("https://burger-frontend-1.prakticum-team.ru/register")
wait.until(EC.presence_of_element_located((By.NAME, "name")))
driver.find_element(By.NAME, "name").send_keys("Андрей")
driver.find_element(By.NAME, "email").send_keys(f"pwd_{ts}@test.com")
driver.find_element(By.NAME, "password").send_keys("12345")
driver.find_element(By.XPATH, "//button[text()='Зарегистрироваться']").click()
time.sleep(2)
print("  URL после клика:", driver.current_url)
all_p = driver.find_elements(By.TAG_NAME, "p")
for p in all_p:
    cls = p.get_attribute("class") or ""
    if "error" in cls.lower():
        print("  ERROR P:", repr(p.text), "class:", cls)
form_html = driver.find_element(By.TAG_NAME, "form").get_attribute("outerHTML")
print("  FORM HTML:", form_html[:600])

# === ТЕСТ 3: Тоггл - точное поведение ===
print("\n=== Тоггл пароля: два клика, логи ===")
driver.get("https://burger-frontend-1.prakticum-team.ru/register")
wait.until(EC.presence_of_element_located((By.NAME, "password")))
driver.find_element(By.NAME, "password").send_keys("Test1234!")

toggle = driver.find_element(By.XPATH, "//div[contains(@class,'input__icon-action')]")
print("  Класс до клика:", toggle.get_attribute("class"))
toggle.click()
time.sleep(0.5)
pwd_type = driver.find_element(By.NAME, "password").get_attribute("type")
print("  Тип после 1-го клика:", pwd_type)
toggle_after = driver.find_element(By.XPATH, "//div[contains(@class,'input__icon-action')]")
print("  Класс после 1-го клика:", toggle_after.get_attribute("class"))

# Попробуем JS click на второй раз
driver.execute_script("arguments[0].click();", toggle_after)
time.sleep(0.5)
pwd_type2 = driver.find_element(By.NAME, "password").get_attribute("type")
print("  Тип после JS-клика:", pwd_type2)

driver.quit()
