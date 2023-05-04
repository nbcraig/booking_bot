from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from booking.constants import URL
from booking.filtration import ResultFiltration
import time
import pyshorteners

class Booking(webdriver.Chrome):
    def __init__(self, driver=webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))):
        self.driver = driver 
        super(Booking, self).__init__()
        self.implicitly_wait(15)
        self.maximize_window()

    def get_home_page(self, currency='USD'):
        self.get(URL + f'/?selected_currency={currency}')

        # Accept cookies
        cookies = self.find_element(By.ID, "onetrust-accept-btn-handler")
        cookies.click()

    def select_destination(self, destination):
        search_field = self.find_element(
            By.CSS_SELECTOR, 
            'input[name="ss"]'
        )
        search_field.clear() # Clearing any text or placeholder in the input field
        search_field.send_keys(destination)

        time.sleep(2) # Explicitly wait in case of slow internet

        suggestion = self.find_element(
            By.XPATH, 
            '/html[1]/body[1]/div[2]/div[2]/div[1]/div[1]/form[1]/div[1]/div[1]/div[1]/div[1]/div[2]/ul[1]/li[1]'
        )
        suggestion.click()

    def select_dates(self, check_in, check_out):
        select_check_in = self.find_element(
            By.CSS_SELECTOR, 
            f'span[data-date="{check_in}"]'
        )
        select_check_in.click()

        select_check_out = self.find_element(
                    By.CSS_SELECTOR, 
                    f'span[data-date="{check_out}"]'
                )
        select_check_out.click()

    def select_occupants(self, people): # Adults only in this case
        selection = self.find_element(By.CSS_SELECTOR, 'button[data-testid="occupancy-config"]')
        selection.click()

        decrease = self.find_element(
            By.XPATH, 
            '/html[1]/body[1]/div[2]/div[2]/div[1]/div[1]/form[1]/div[1]/div[3]/div[1]/div[1]/div[1]/div[1]/div[1]/div[2]/button[1]'
        )

        increase = self.find_element(
            By.XPATH, 
            '/html[1]/body[1]/div[2]/div[2]/div[1]/div[1]/form[1]/div[1]/div[3]/div[1]/div[1]/div[1]/div[1]/div[1]/div[2]/button[2]'
        )

        while True:
            people_count = int(self.find_element(
                By.ID, 
                'group_adults'
            ).get_attribute('value'))

            if people == people_count:
                break
            elif people < people_count:
                decrease.click()
            else:
                increase.click()

        submit = self.find_element(
            By.XPATH, 
            '/html[1]/body[1]/div[2]/div[2]/div[1]/div[1]/form[1]/div[1]/div[3]/div[1]/div[1]/div[1]/button[1]'
        )
        submit.click()

        search_button = self.find_element(
            By.XPATH, 
            '/html[1]/body[1]/div[2]/div[2]/div[1]/div[1]/form[1]/div[1]/div[4]/button[1]'
        )
        search_button.click()

    def apply_filtrations(self):
        filtration = ResultFiltration(driver=self)
        filtration.by_ranking(3, 4)
        filtration.sort_by_price()

    def report_results(self):
        results_box = self.find_element(
            By.CLASS_NAME, 
            'd4924c9e74'
        )
        results = results_box.find_elements(By.CSS_SELECTOR, 'div[data-testid="property-card"]')

        t = time.localtime()
        time_now = time.strftime('%H:%M:%S', t)
        print(f'Best deals at { time_now }\n\n')
        # Best 5 deals
        for result in results[:5]:
            hotel_name = result.find_element(
                By.CSS_SELECTOR, 
                'div[data-testid="title"]'
            ).get_attribute("innerText")
            price = result.find_element(
                By.CSS_SELECTOR, 
                'span[data-testid="price-and-discounted-price"]'
            ).get_attribute("innerText")
            url = result.find_element(
                By.CSS_SELECTOR, 
                'a[data-testid="title-link"]'
            ).get_attribute('href')
            type_bitly = pyshorteners.Shortener()
            short_url = type_bitly.tinyurl.short(url)


            print(f'{hotel_name}\n{price}\n{short_url}\n----------')