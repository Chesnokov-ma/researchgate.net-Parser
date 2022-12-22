from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException


def _research_gate_page_404(self):
    """Проверить, существует ли страница"""

    # если перекидывает назад на поиск
    if 'search.Search' in self._driver.current_url:  # is returned to "Search" page
        return True

    # если страница 404
    try:
        if self._driver.find_element(By.CLASS_NAME, 'headline').text == 'Page not found':
            return True
    except NoSuchElementException:
        pass

    else:
        return False
