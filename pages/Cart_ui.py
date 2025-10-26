from selenium import webdriver
from selenium.webdriver.common.by import By
import allure

@allure.description("Тестирование добавления товара в корзину на сайте Читай-город.")
class AddToCart:
  
    # ИНИЦИАЛИЗАЦИЯ
    def __init__(self, book_title: str):
        """         Создает объект для добавления книги в корзину.

                    :param book_title: Название книги для добавления в корзину.
        """
        self.book_title = book_title

    # ПОИСК КНИГИ ПО НАЗВАНИЮ
    def search_by_title(self, driver: webdriver.Chrome, book_title: str) -> dict:
        """         Ищет книгу по названию и добавляет её в корзину.

                    :param driver: Экземпляр драйвера Selenium.
                    :param book_title: Название книги для поиска.
                    :return: Словарь с результатами поиска (в данном методе возвращает None).
        """
        # Ввод названия книги в строку поиска
        driver.find_element(By.NAME, "phrase").send_keys(book_title)
        
        # Клик по кнопке поиска
        search_button_find = driver.find_element(By.CSS_SELECTOR, "button[aria-label='Искать']")
        search_button_find.click()

        # Клик по кнопке "Купить"
        search_button_buy = driver.find_element(By.CSS_SELECTOR, "button[aria-label='Купить']")
        search_button_buy.click() 
        
        # Открытие корзины
        cart_icon = driver.find_element(By.CSS_SELECTOR, '.header-cart__icon')
        cart_icon.click()

@allure.description("Тестирование поля поиска по автору на сайте Читай-город.")
class SearchByAuthor:
    """Класс для выполнения поиска книг по автору на сайте Читай-город."""

    def __init__(self, author_name: str):
        """
                Инициализация класса SearchByAuthor.

                :param author_name: Имя автора, книги которого необходимо найти.
        """
        self.author_name = author_name

    @allure.step("Поиск книги по автору")
    def search_by_author(self, driver: webdriver.Chrome) -> None:
        """         
                Поиск книг по имени автора на сайте Читай-город.

                :param driver: Экземпляр драйвера Selenium (в данном случае Chrome).
                :raises Exception: Возникает, если не удается найти элементы поиска на странице.
        """
        try:
            # Ввод имени автора в строку поиска
            search_input = driver.find_element(By.NAME, "phrase")
            search_input.send_keys(self.author_name)
            
            # Клик по кнопке поиска
            search_button = driver.find_element(By.CSS_SELECTOR, "button[aria-label='Искать']")
            search_button.click()
        
        except Exception as e:
            allure.attach(str(e), name="error", attachment_type=allure.attachment_type.TEXT)
            raise   
@allure.description("Тестирование поля поиска по названию на сайте Читай-город.")
class SearchByTitle:
    """Класс для выполнения поиска книг по названию на сайте Читай-город."""

    def __init__(self, book_title: str):
        """
                    Инициализация класса SearchByTitle.

                    :param book_title: Название книги, которую необходимо найти.
        """
        self.book_title = book_title

    @allure.step("Поиск книги по названию")
    def search_by_title(self, driver: webdriver.Chrome) -> None:
        """
                    Поиск книг по названию на сайте Читай-город.

                    :param driver: Экземпляр драйвера Selenium (в данном случае Chrome).
                    :raises Exception: Возникает, если не удается найти элементы поиска на странице.
        """
        # Ввод названия в строку поиска
        try:
            search_input = driver.find_element(By.NAME, "phrase")
            search_input.send_keys(self.book_title)

            # Клик по кнопке поиска
            search_button = driver.find_element(By.CSS_SELECTOR, "button[aria-label='Искать']")
            search_button.click()
        except Exception as e:
            allure.attach(str(e), name="error", attachment_type=allure.attachment_type.TEXT)
            raise   
@allure.description("Тестирование удаления товара из корзины на сайте Читай-город.")
class DeleteFromCart:
          """Класс для удаления товара из корзины на сайте Читай-город."""
def __init__(self, book_title: str): 
        """
        Инициализация класса DeleteFromCart.
        
        :param book_title: Название книги, которую нужно удалить из корзины.
        """
        self.book_title = book_title
@allure.step("Поиск книги по названию и удаление из корзины")
def delete_from_cart(self, driver: webdriver.Chrome) -> None:
        """
        Поиск книги по названию, добавление в корзину и удаление из нее.

        :param driver: Экземпляр драйвера Selenium (в данном случае Chrome).
        :raises Exception: Возникает, если не удается найти элементы на странице.
        """
    
            # Поиск книги по названию
        driver.find_element(By.NAME, "phrase").send_keys(self.book_title)

            # Клик по кнопке поиска
        search_button_find = driver.find_element(By.CSS_SELECTOR, "button[aria-label='Искать']")
        search_button_find.click()

            # Клик по кнопке "Купить"
        search_button_buy = driver.find_element(By.CSS_SELECTOR, "button[aria-label='Купить']")
        search_button_buy.click()

            # Открытие корзины
        cart_icon = driver.find_element(By.CSS_SELECTOR, '.header-cart__icon')
        cart_icon.click()

            # Клик по кнопке "Очистить корзину"
        delete_button = driver.find_element(By.CSS_SELECTOR, 'span.clear-cart')
        delete_button.click()             