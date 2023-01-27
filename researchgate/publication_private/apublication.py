from bs4 import BeautifulSoup as bs4
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import time


def __get_apublication(self):
    source_data = self._driver.page_source
    soup = bs4(source_data, "html.parser")

    try:
        name = soup.find('div', {'class': ['nova-legacy-e-text nova-legacy-e-text--size-xl nova-legacy-e-text--family-display nova-legacy-e-text--spacing-xs nova-legacy-e-text--color-inherit']}).text
    except AttributeError:
        name = ''

    try:
        abstract = soup.find('div', {'class': ['nova-legacy-o-stack nova-legacy-o-stack--gutter-m nova-legacy-o-stack--spacing-none nova-legacy-o-stack--no-gutter-outside']}).text
    except AttributeError:
        abstract = ''

    try:
        type = soup.find('span', {'class': ['nova-legacy-e-badge nova-legacy-e-badge--color-green nova-legacy-e-badge--display-block nova-legacy-e-badge--luminosity-high nova-legacy-e-badge--size-l nova-legacy-e-badge--theme-solid nova-legacy-e-badge--radius-m']}).text
    except AttributeError:
        type = ''

    try:
        available = soup.find('button', {'class': ['nova-legacy-e-badge nova-legacy-e-badge--color-green nova-legacy-e-badge--display-block nova-legacy-e-badge--luminosity-medium nova-legacy-e-badge--size-l nova-legacy-e-badge--theme-ghost nova-legacy-e-badge--radius-m']}).text
    except AttributeError:
        available = ''

    try:
        link = 'https://www.researchgate.net/' + soup.find('a', {'class': ['nova-legacy-c-button nova-legacy-c-button--align-center nova-legacy-c-button--radius-full nova-legacy-c-button--size-s nova-legacy-c-button--color-blue nova-legacy-c-button--theme-solid']}).get('href')
    except AttributeError:
        link = ''

    if 'Full-text available' in available:
        read = link
    else:
        read = self._driver.current_url

    metadata = str(soup.find_all('div', {'class': ['research-detail-meta']})[0])
    metadata_soup = bs4(metadata, "html.parser")
    metadata_list = []

    # разложить всю метадату
    for metadata_container in metadata_soup.find_all('ul', {}):
        containter_soup = bs4(str(metadata_container), "html.parser")
        # print({containter_soup.text: containter_soup.find('a').get('href')})
        metadata_list.append({containter_soup.text: containter_soup.find('a').get('href')})

    # поиск DOI
    DOI = ''
    for row in metadata_list:
        for key in row:
            if 'DOI' in key:
                DOI = row[key]
                break

    # авторы
    authors = []

    try:
        authors_button = None

        # не находит по xpath
        # authors_buttons = self._driver.find_element(By.XPATH, '//*[@id="rgw4_63d3a47ee440e"]/div/div[1]/div[1]/div[1]/div[1]/ul/li[4]/button')
        buttons = self._driver.find_elements(By.TAG_NAME, 'button')
        for webelement in buttons:
            if 'Show all' in webelement.text:
                authors_button = webelement
                break

        if authors_button:
            authors_button.click()
            time.sleep(1.5)

            # парсинг нового окна

    except NoSuchElementException:

        # парсинг элементов на основном окне

        pass

    # print(name)
    # print(abstract)
    # print(available)
    # print(link)
    # print(read)
    # print(metadata_list)
    # print(DOI)

    return {'name': name,
            'abstract': abstract.replace('\u200b', ''),
            'DOI': DOI,
            'authors': authors,
            'type': type,
            'available': available,
            'download link': link,
            'read link': read,
            'metadata': metadata_list}