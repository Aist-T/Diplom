from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
import allure
from selenium.webdriver.support import expected_conditions as EC
from pages.Cart_ui import AddToCart, SearchByAuthor, SearchByTitle, DeleteFromCart
from constants import UI_url

search_by_author = SearchByAuthor
search_by_title = SearchByTitle
add_to_card = AddToCart
delete_from_cart = DeleteFromCart

@allure.title("Тест поиска книг по автору. POSITIVE")
@allure.description("Этот тест проверяет, что поиск книг по автору работает корректно.")
@allure.feature("READ")
@allure.severity("CRITICAL")
def test_search_by_author ():
        """ 
                          Проверка корректности результатов поиска по автору.
                          
        """
        with allure.step ("Запустить браузер Chrome"):
            driver = webdriver.Chrome() 
       
        with allure.step ("Перейти на сайт Читай-город"):
            driver.get(UI_url)  

        with allure.step ("Найти книгу по автору Лев Толстой"):
            author_name = "Лев Толстой"
            search_by_author(author_name)
        
        with allure.step ("Получить результаты поиска"):
            results_find = driver.find_element(By.CLASS_NAME, "product-title__author")

        with allure.step ("Проверить, что поиск по автору успешен"):
            assert results_find is not None
    
        with allure.step ("Закрыть браузер"):
            driver.quit()  

@allure.title("Тест добавления товара в корзину. POSITIVE")
@allure.description("Этот тест проверяет, что товар добавляется в корзину.")
@allure.feature("CREATE")
@allure.severity("BLOCKER")
def test_add_to_card():
        """
                             Проверка корректности добавления товара в корзину.
                             
        """
        with allure.step ("Запустить браузер Chrome"):
            driver = webdriver.Chrome() 
        
        with allure.step ("Перейти на сайт Читай-город"):
            driver.get(UI_url)  

        with allure.step ("Добавить в корзину книгу с названием Война и мир"):
            book_title = "Война и мир"
            add_to_card(book_title)
        
        with allure.step ("Получить результаты добавления в корзину"):
            results_add = driver.find_element(By.CSS_SELECTOR, 'div.product-title__head')

        with allure.step ("Проверить, что корзина не пуста"):
            assert results_add is not None
               
        with allure.step ("Закрыть браузер"):
            driver.quit() 

@allure.title("Тест удаления товара из корзины. POSITIVE")
@allure.description("Этот тест проверяет, что товар из корзины удаляется корректно.")
@allure.feature("DELETE")
@allure.severity("BLOCKER")
def test_delete_from_card():
        """
                             Проверка корректности удаления товара из корзины.
                             
        """

        with allure.step ("Запустить браузер Chrome"):
            driver = webdriver.Chrome() 
        
        with allure.step ("Перейти на сайт Читай-город"):
            driver.get(UI_url)  


        with allure.step ("Удалить книгу из корзины"):
            book_title = "Война и мир"
            delete_from_cart(book_title)
            results_del = driver.find_elements(By.CSS_SELECTOR, 'div.product-title__head')

        with allure.step ("Проверить, что товар больше не существует в списке"):
            assert all(book_title not in element.text for element in results_del), f"Книга '{book_title}' все еще в корзине."

@allure.title("Тест поиска книг по жанру. POSITIVE")
@allure.description("Этот тест проверяет, что поиск книг по жанру работает корректно.")
@allure.feature("READ")
@allure.severity("CRITICAL")
@allure.feature("Поиск книг")
@allure.story("Поиск по жанру")
@allure.severity(allure.severity_level.NORMAL)
def test_search_by_genre():
    """ 
                          Проверка корректности результатов поиска по жанру, 
                          добавляет первую гнигу из результата покиска в корзину, 
                          увеличивает число копий книги на 1 в корзине
                          
        """
    with allure.step ("Запустить браузер Chrome"):
            driver = webdriver.Chrome() 
       
    with allure.step ("Перейти на сайт Читай-город"):
            driver.get(UI_url)
    
    with allure.step("Ввод жанра в поисковую строку"):
        search_input = webdriver(driver, 10).until(
            EC.presence_of_element_located((By.NAME, "query"))
        )
        search_input.clear()
        search_input.send_keys("фантастика")
        
        search_button = driver.find_element(By.CSS_SELECTOR, ".search-form__button")
        search_button.click()
        
    
    with allure.step("Проверка результатов поиска"):
        results = webdriver(driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".product-list__item"))
        )
        
        
        assert len(results) > 0, "Результаты поиска не найдены"
        
        
        first_book = results[0]
        book_title = first_book.find_element(By.CSS_SELECTOR, ".product-title__link").text
        allure.attach(f"Найденная книга: {book_title}", name="Результат поиска")
        
    with allure.step("Добавляем первую найденную книгу в корзину"):
        
         buy_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, ".product-card .btn-buy"))
        )
         buy_button.click()
        
    with allure.step("Проверяем, что книга добавлена в корзину"):
        
        cart_count = WebDriverWait(driver, 10).until(
            EC.text_to_be_present_in_element(
                (By.CSS_SELECTOR, ".header-cart .cart-counter"),
                "1"
            )
        )
        assert cart_count, "Книга не добавлена в корзину"
        
    with allure.step("Проверяем содержимое корзины"):
        
        driver.find_element(By.CSS_SELECTOR, ".header-cart").click()
        
        
        product_in_cart = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".cart-item"))
        )
        assert product_in_cart, "Товар не отображается в корзине"
    with allure.step("Увеличение количества книг в корзине"):
        
        driver.find_element(By.CSS_SELECTOR, ".header-controls__btn").click()
        wait = WebDriverWait(driver, 20)   
        
        quantity_input = wait.until(EC.presence_of_element_located((By.XPATH, "//input[@name='quantity']")))
        current_quantity = int(quantity_input.get_attribute("value"))
        quantity_input.clear()
        quantity_input.send_keys(str(current_quantity + 1))
        
        
        wait.until(EC.text_to_be_present_in_element((By.XPATH, "//input[@name='quantity']"), str(current_quantity + 1)))
    
    with allure.step("Проверка нового количества"):
        
        new_quantity = driver.find_element(By.XPATH, "//input[@name='quantity']").get_attribute("value")
        assert int(new_quantity) == current_quantity + 1