import requests
import json
import allure
from constants import API1_url,API2_url, bearer_token

class TestBookSearchAPI:
    @allure.feature("Поиск книг")
    @allure.story("Базовый поиск")
    @allure.title("Проверка успешного поиска книг")
    @allure.description("Тестирование успешного ответа от API при поиске книг")
    def test_search_books(self):
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
@allure.description("Тестирование добавления товара в корзину на сайте Читай-город.")
class AddToCartAPI:
    """Класс для работы с API добавления товара в корзину."""
    
    url = API1_url  # URL для добавления товара в корзину
   

    # Инициализация класса
    def __init__(self, url):
        """
                    Создает новый объект для работы с API.
        """
        self.url = url
        self.headers = {
            'Content-Type': 'application/json',  # Установка типа контента
            'Authorization': bearer_token  # Установка токена для авторизации
        }

    def add_product_to_cart(self, product_id: int, item_list_name: str) -> int:
        """             Добавляет товар в корзину и возвращает статус-код ответа.
        
                        Args:
                            product_id (int): ID товара для добавления.
                            item_list_name (str): Имя списка, к которому принадлежит товар.
        
                        Returns:
                            int: Статус-код ответа от сервера (например, 200 для успешного добавления).
        """
        # Данные для добавления товара
        payload = {
            "id": product_id,  # ID товара
            "adData": {
                "item_list_name": item_list_name,  # Имя списка товаров
            }
        } 
        
        # Отправляем POST-запрос
        resp = requests.post(self.url, headers=self.headers, data=json.dumps(payload))
        return resp.status_code  # Возвращаем статус-код ответа
    
@allure.title("Класс для удаления товара из корзины")
class DeleteFromCart:
    # URL для API
    url = API1_url  # URL для удаления товаров
    url_2 = API2_url  # URL для получения содержимого корзины

    @allure.step("Инициализация класса DeleteFromCart")
    def __init__(self, url):
        """
        Создает объект для работы с корзиной.

        :param url: URL для удаления товара из корзины.
        """
        self.url = url
        self.headers = {
            'Content-Type': 'application/json',  # Указываем, что отправляем JSON
            'Authorization': bearer_token  # Токен для авторизации
        }

    @allure.step("Получение содержимого корзины")
    def get_cart_contents(self)-> dict:
        """
        Получает содержимое корзины.

        :return: Статус-код ответа и содержимое корзины в формате JSON.
        """
        # Отправляем GET-запрос для получения содержимого корзины
        response = requests.get(self.url_2, headers=self.headers)
        return response.status_code, response.json()  # Возвращаем статус-код и данные корзины

    @allure.step("Удаление товара из корзины")
    def delete_product_from_cart(self, prod_id)-> None:
        """
        Удаляет товар из корзины.

        :param prod_id: ID товара, который нужно удалить.
        :return: Статус-код ответа от сервера.
        """
        # Отправляем DELETE-запрос для удаления товара из корзины
        response = requests.delete(self.url_2, headers=self.headers, data=json.dumps(prod_id))
        return response.status_code  # Возвращаем статус-код ответа 
      
class CartApi:
    """
    Класс с методами для API-запросов при работе с корзиной товаров.
    - Поиск товара на главной странице сайта.
    - Очистка корзины товаров,
    - Получение кратких данных о составе корзины,
    - Получение информации о содержимом корзины,
    - Добавление товара в корзину по артикулу (id)б
    - Удаление товара из корзины по id.
    """
    @allure.step("""CartApi. URL:{cart_url}, {cart_short_url},
                 параметры для авторизации: {params}""")
    def __init__(self, cart_url: str, cart_short_url: str,
                 params: dict) -> None:
        """
        Инициализация метода 'CartApi'.
        Определяет сущность класса 'CartApi' и формирует
        параметры для requests-запросов:
        cart_url: str - основной URL для работы с корзиной,
        cart_short_url: str - URL для получения краткой информации
                        о содержимом корзины,
        params: dict - словарь с необходимыми для авторизации данными,
                        содержит ключи:
                        - token: str,
                        - user_agent: str,
                        - content_type: str.
        """
        self.cart_url = cart_url
        self.cart_short_url = cart_short_url
        self.params = params

    @allure.step("Очистить корзину товаров")
    def cart_delete_all(self) -> dict:
        path = self.cart_url
        resp = requests.delete(path, headers=self.params)
        return resp

    @allure.step("Получить краткие данные о составе корзины")
    def cart_short(self) -> dict:
        path = self.cart_short_url
        resp = requests.get(path, headers=self.params)
        return resp

    @allure.step("Получить полную информацию о содержимом корзины")
    def cart_info(self) -> dict:
        path = self.cart_url
        resp = requests.get(path, headers=self.params)
        return resp

    @allure.step("Добавить в корзину товар по артикулу: {add_id}.")
    def add_to_cart(self, add_id: dict) -> dict:
        path = self.cart_url + "/product"
        resp = requests.post(path, headers=self.params, json=add_id)
        return resp

    @allure.step("Удалить из корзины товар по id: {del_id}.")
    def del_from_cart(self, del_id: str) -> dict:
        path = self.cart_url + "/product/" + del_id
        resp = requests.delete(path, headers=self.params)
        return resp

    @allure.step("Изменить количество единиц товара: {quantity_id}.")
    def change_product_quantity(self, quantity_id: dict) -> dict:
        path = self.cart_url
        resp = requests.put(path, headers=self.params, json=quantity_id)
        return resp     