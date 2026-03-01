import uuid

BASE_URL = "https://burger-frontend-1.prakticum-team.ru"

VALID_USER = {
    "email": "test@example.com",
    "password": "Test1234!"
}

INVALID_USER = {
    "email": "wrong@example.com",
    "password": "wrongpassword"
}

# Данные для регистрации
VALID_REGISTER = {
    "name": "Андрей",
    "password": "Test1234!"
}

EXISTING_USER_EMAIL = "shevchenko.rey@gmail.com"


def unique_email():
    """Генерирует гарантированно уникальный email для каждого теста."""
    return f"test_{uuid.uuid4().hex[:12]}@mailtest.com"

# Невалидные имена
INVALID_NAMES = [
    ("А", "слишком короткое имя (1 символ)"),
    ("А" * 26, "слишком длинное имя (26 символов)"),
    ("Andrey123", "имя с цифрами"),
    ("Andrey!", "имя со спецсимволами"),
]

# Невалидные email
INVALID_EMAILS = [
    ("ab@c", "слишком короткий email (4 символа)"),
    ("a" * 45 + "@test.com", "слишком длинный email (54 символа)"),
    ("andrey test@mail.ru", "email с пробелом"),
    ("andrey#test@mail.ru", "email с недопустимым символом #"),
]

# Невалидные пароли
INVALID_PASSWORDS = [
    ("12345", "слишком короткий пароль (5 символов)"),
    ("a" * 51, "слишком длинный пароль (51 символ)"),
]
