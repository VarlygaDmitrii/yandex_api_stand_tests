import sender_stand_request
import data
import requests
import configuration


# Функция для изменения значения в параметре kit_name в теле запроса
def get_kit_body(kit_name):
    # Копируется словарь с телом запроса из файла data
    current_body = data.kit_body.copy()
    # Изменение значения в поле kit_name
    current_body["name"] = kit_name
    # Возвращается новый словарь с нужным значением kit_name
    return current_body


# Функция для определения значения authToken из запроса на создание нового пользователя
def get_new_user_token():
    auth_token = sender_stand_request.post_new_user(data.user_body)
    return auth_token.json()["authToken"]


print(get_new_user_token())


# Функция для создания нового набора
def post_new_client_kit(kit_body):
    return requests.post(configuration.URL_SERVICE + configuration.CREATE_KIT_PATH, json=kit_body,
                         headers=data.auth_token)


data.auth_token["Authorization"] = f"Bearer {get_new_user_token()}"
response = post_new_client_kit(data.kit_body)
print(response.status_code)
print(response.json())


# Функция для позитивной проверки
def positive_assert(kit_name):
    # В переменную user_kit сохраняется обновлённое тело корзины
    user_kit = get_kit_body(kit_name)
    # В переменную user_response сохраняется результат запроса на создание корзины:
    user_response = post_new_client_kit(user_kit)

    # Проверяется, что код ответа равен 201
    assert user_response.status_code == 201
    # Проверяется, что в имя в ответе совпадает с подставляемыми тестовыми значениями
    assert user_response.json()["name"] == kit_name


def negative_assert_symbol(kit_name):
    # В переменную user_kit сохраняется обновлённое тело запроса
    user_kit = get_kit_body(kit_name)
    # В переменную kit_response сохраняется результат
    kit_response = post_new_client_kit(user_kit)

    # Проверяется, что код ответа равен 400
    assert kit_response.status_code == 400
    # Проверяется, что в теле ответа атрибут "code" равен 400
    assert kit_response.json()["code"] == 400


def empty_name_assert(kit_name):
    # В переменную user_kit сохраняется обновлённое тело запроса
    user_kit = get_kit_body(kit_name)
    # В переменную kit_response сохраняется результат
    kit_response = post_new_client_kit(user_kit)
    # Удаляем имя kit_name как параметр из тела

    # Проверяется, что код ответа равен 400
    assert kit_response.status_code == 400
    # Проверяется, что в теле ответа атрибут "code" равен 400
    assert kit_response.json()["code"] == 400
    # Проверяется, что в имя в ответе совпадает с подставляемыми тестовыми значениями
    assert user_kit.json()["name"] == kit_name


# Тест 1: Имя набора состоит из 1 символа, ОР - ответ 201, имя совпадает с тестовым значением
def test_1create_kit_name_with_1_letter_success():
    positive_assert("a")


# Тест 2: Имя набора состоит из 511 символов, ОР - ответ 201, имя совпадает с тестовым значением
def test_2create_kit_name_with_511_letter_success():
    positive_assert("AbcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdAbcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabC")


# Тест 3: Имя набора состоит из пустого(не заполненного значения), ОР - ответ 400, набор не создался
def test_3create_kit_name_with_no_letter_fail():
    negative_assert_symbol("")


# Тест 4: Имя набора состоит из 512 символа, ОР - ответ 400, набор не создался
def test_4create_kit_name_with_512_letter_fail():
    negative_assert_symbol("AbcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdAbcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcD")


# Тест 5: Имя набора состоит из латиницы, ОР - ответ 201, имя совпадает с тестовым значением
def test_5create_kit_name_with_english_symbol_letter_success():
    positive_assert("QWErty")


# Тест 6: Имя набора состоит из кириллицы, ОР - ответ 201, имя совпадает с тестовым значением
def test_6create_kit_name_with_russian_symbol_letter_success():
    positive_assert("Мария")


# Тест 7: Имя набора состоит из спецсимволов, ОР - ответ 201, имя совпадает с тестовым значением
def test_7create_kit_name_with_special_symbol_letter_success():
    positive_assert("№%@,")


# Тест 8: Имя набора включает в себя пробел, ОР - ответ 201, имя совпадает с тестовым значением
def test_8create_kit_name_with_space_between_symbol_letter_success():
    positive_assert("Человек и КО")


# Тест 9: Имя набора состоит из чисел(формат - STR), ОР - ответ 201, имя совпадает с тестовым значением
def test_9create_kit_name_with_str_numbers_symbol_letter_success():
    positive_assert("123")


# Тест 10: Имя набора не передано как параметр, ОР - ответ 400, набор не создался
def test_10create_kit_name_with_empty_param_fail():
    empty_name_assert(None)


# Тест 11: Имя набора состоит из чисел(формат - INT), ОР - ответ 201, имя совпадает с тестовым значением
def test_11create_kit_name_with_int_numbers_symbol_letter_success():
    negative_assert_symbol(123)
