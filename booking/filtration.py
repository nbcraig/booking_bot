from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.common.by import By

class ResultFiltration:
    def __init__(self, driver:WebDriver):
        self.driver = driver

    def by_ranking(self, *stars):
        ranking_box = self.driver.find_element(By.CSS_SELECTOR, 'div[data-filters-group="class"]')
        ranking_box_elements = ranking_box.find_elements(By.CSS_SELECTOR, '*')

        for i in stars:
            for element in ranking_box_elements:
                if str(element.get_attribute('innerHTML')).strip() == f'{i} stars':
                    element.click()

    def sort_by_price(self):
        option_btn = self.driver.find_element(By.CSS_SELECTOR, 'button[data-testid="sorters-dropdown-trigger"]')
        option_btn.click()

        select = self.driver.find_element(By.CSS_SELECTOR, 'button[data-id="price"]')
        select.click()