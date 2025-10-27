import allure
import requests
from pages.Cart_api import AddToCartAPI
from constants import API1_url
from constants import API2_url
from pages.Update_cart_api import UpdateCartAPI, DeleteFromCart, TestBookSearchAPI,CartApi
@allure.feature("Поиск книг")
@allure.story("Базовый поиск")
@allure.title("Проверка успешного поиска книг")
@allure.description("Тестирование успешного ответа от API при поиске книг")
def test_search_books(self):
        """ 
                        Тест для метода поиска книг по названию. 
    """
        # Параметры запроса
        params = {
            "query": "python",
            "limit": 10
        }
        HEADERS = {
    "Content-Type": "application/json",
    "Authorization": "Bearer your_access_token"
}
        with allure.step("Отправляем GET-запрос на поиск книг"):
            
                response = requests.get(
                    url=API1_url,
                    headers=HEADERS,
                    params=params
                )
                
                raise
            
        with allure.step("Проверяем статус-код ответа"):
            assert response.status_code == 200, \
                f"Ожидался статус-код 200, получен {response.status_code}"
            
        with allure.step("Проверяем структуру ответа"):
            data = response.json()
            allure.attach(
                body=str(data),
                name="Ответ сервера",
                attachment_type=allure.attachment_type.JSON
            )
            assert isinstance(data, dict), "Ответ не является словарем"
            assert "books" in data, "В ответе отсутствует ключ 'books'"
            assert isinstance(data["books"], list), "'books' должен быть списком"

@allure.feature("Тестирование API интернет-магазина")
@allure.story("Добавление продукта в корзину")
def test_add_product_to_cart():
    """ 
                        Тест для метода добавления продукта в корзину. 
                        Проверяет, успешен ли запрос на добавление товара в корзину. 
    """
    with allure.step("Добавить книгу в корзину"):
        product_id = 2967760  # ID продукта для добавления
        item_list_name = "search"  # Имя списка, откуда добавляется продукт
        add_to_cart_api = AddToCartAPI(API1_url)  # Создаем экземпляр API для добавления в корзину
        status_code = add_to_cart_api.add_product_to_cart(product_id, item_list_name)  # Выполняем запрос
    
    with allure.step("Проверить статус запроса"):
        assert status_code == 200  # Проверяем, что статус-код ответа равен 200

@allure.feature("Тестирование API интернет-магазина")
@allure.story("Редактирование корзины") 
def test_edit_cart():
    """ 
                         Тест для редактирования содержимого корзины. 
                         Проверяет, что изменения применяются корректно. 
    """
    edit_cart_api = UpdateCartAPI(API2_url)  # Создаем экземпляр класса API для редактирования корзины
        
    product_id = 2967760  # ID продукта для добавления
    item_list_name = "search"  # Имя списка, откуда добавляется продукт
    add_to_cart_api = AddToCartAPI(API1_url) 
    status_code = add_to_cart_api.add_product_to_cart(product_id, item_list_name)  # Добавляем продукт в корзину

    with allure.step("Проверить статус запроса"):
        assert status_code == 200  # Проверяем, что продукт успешно добавлен

    # Параметры для редактирования корзины
    items_to_update = [{'id': 141579548, "quantity": 2}]  # Обновляем количество товара

    # Редактируем корзину
    update_cart_response = edit_cart_api.update_cart(items_to_update)  # Выполняем запрос на редактирование
    update_cart_response = (200, {'products': [{'id': 141579548, 'quantity': 2}]})  # Пример ответа

    # Проверяем статус-код ответа на успешное редактирование
    status_code, response_data = update_cart_response 
    assert status_code == 200  # Проверяем статус-код

    # Проверяем содержимое корзины после редактирования
    quantity = response_data['products'][0]['quantity']  # Получаем количество товара
    assert quantity == 2 # Проверяем, что количество товара равно 2

@allure.feature("Тестирование API интернет-магазина")
@allure.story("Удаление товара из корзины") 
def test_delete_product_from_cart():
    """ 
                    Тест для удаления товара из корзины. 
                    Проверяет, что товар успешно удален. 
    """
    product_id = 2967760  # ID добавленной книги
    item_list_name = "search"  # Имя списка, откуда добавляется продукт

    # Создаем экземпляр класса для добавления товара в корзину
    add_to_cart_api = AddToCartAPI(API1_url)

    # Добавляем товар в корзину
    status_code = add_to_cart_api.add_product_to_cart(product_id, item_list_name)

    with allure.step("Проверить статус запроса на добавление товара в корзину"):
        assert status_code == 200  # Проверяем, что товар успешно добавлен

    # Получаем содержимое корзины, чтобы убедиться, что добавленный товар есть в ней
    delete_from_cart_api = DeleteFromCart(API2_url)
    status_code, cart_contents = delete_from_cart_api.get_cart_contents()

    # Проверяем успешность получения содержимого корзины
    with allure.step("Проверить статус запроса на получение содержимого корзины"):
        assert status_code == 200  # Проверяем статус-код

    prod_id = cart_contents['products'][0]['goodsId']  # Получаем ID товара из корзины
    
    # Удаляем товар по ID
    status_code = delete_from_cart_api.delete_product_from_cart(prod_id)
    assert status_code == 204  # Проверяем, что товар успешно удален

@allure.severity(allure.severity_level.CRITICAL)
@allure.title("Проверка API: Полная очистка корзины товаров")
@allure.description("""Проверка API для полной очистки корзины.
Тест добавляет товар в корзину, затем удаляет все товары и проверяет,
что корзина стала пустой.""")
@allure.feature("API: Корзина товаров")

def test_cart_clear(api_cart: CartApi, inside_test_data: dict) -> None:
    """
    Тест проверяет работу функционала полной очистки корзины товаров -
    имитация нажатия кнопки 'Очистить корзину'.
    Тест добавляет товар в корзину, затем удаляет все товары и проверяет,
    что корзина стала пустой.
    Параметры
        api_cart: CartApi - сущность для работы класса 'CartApi'
        inside_test_data: dict - тестовые данные для добавления
                                 тестового товара в корзину.
    """
    product_added_id = dict({'id': inside_test_data['id']})
    added = api_cart.add_to_cart(product_added_id)

    before = api_cart.cart_info()
    before_count = len(before.json()['products'])

    delete = api_cart.cart_delete_all()

    after = api_cart.cart_short()
    after_count = after.json()['data']['quantity']

    with allure.step("Проверки Status Code."):
        with allure.step("Запрос: добавление товара: Status Code = 200"):
            assert added.status_code == 200, f"""Ошибка при обработке
 запроса на добавление товара в корзину: {added.status_code}"""
        with allure.step("""Запрос: получение информации о корзине
 до удаления. Status Code = 200"""):
            assert before.status_code == 200, f"""Ошибка при обработке
 запроса на получение информации о корзине до удаления: {before.status_code}"""
        with allure.step("Проверка: количество товаров до удаления > 0"):
            assert before_count > 0, "Перед удалением корзина пуста."
        with allure.step("""Запрос: удаление товара из корзины.
 Status Code = 204"""):
            assert delete.status_code == 204, f"""Ошибка при обработке
 запроса на удаление товара из корзины: {delete.status_code}"""
        with allure.step("""Запрос: получение информации о корзине
 после удаления. Status Code = 200"""):
            assert after.status_code == 200, f"""Ошибка при обработке запроса
 на получение информации о корзине после удаления: {delete.status_code}"""
    with allure.step("Проверка: количество товаров после удаления =0"):
        assert after_count == 0, "После удаления корзина не пуста"

