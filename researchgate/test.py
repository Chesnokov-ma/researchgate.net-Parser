from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import time


def authors_button_test(self):
    url = ('https://www.researchgate.net/publication/317614509_Engineering_the_breaking_of_time-reversal'
           '_symmetry_in_gate-tunable_hybrid_ferromagnettopological_insulator_heterostructures')

    self._driver.get(url)
    authors_button = None

    if self._is_authorized:
        # xpath (не работает)

        try:
            # authors_buttons = self._driver.find_element(By.XPATH, '//*[@id="rgw4_63d3a47ee440e"]/div/div[1]/div[1]/div[1]/div[1]/ul/li[4]/button')
            buttons = self._driver.find_elements(By.TAG_NAME, 'button')
            for webelement in buttons:
                print(webelement.text)
                if 'Show all' in webelement.text:
                    print(webelement.text)
                    authors_button = webelement
                    break
        except NoSuchElementException:
            pass

    else:
        try:
            authors_button = self._driver.find_element(By.XPATH, '//span[contains(@class, "js-show-more-authors")]')
        except NoSuchElementException:
            pass

    if authors_button:
        authors_button.click()
        print('clicked')
        time.sleep(1.5)

    # self._driver.close()


