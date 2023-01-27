from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from bs4 import BeautifulSoup as bs4
import time

def __get_unapublication(self):

    # раскрываем всех авторов
    try:
        authors_button = self._driver.find_element(By.XPATH, '//span[contains(@class, "js-show-more-authors")]')
        authors_button.click()
        time.sleep(1.5)     # ждем пока скрипт выполнится
    except NoSuchElementException:
        pass

    source_data = self._driver.page_source
    soup = bs4(source_data, "html.parser")

    try:
        name = soup.find('h1', {'class': ['nova-legacy-e-text nova-legacy-e-text--size-xl nova-legacy-e-text--family-display nova-legacy-e-text--spacing-none nova-legacy-e-text--color-grey-900 research-detail-header-section__title']}).text
    except AttributeError:
        name = ''

    try:
        abstract = soup.find('div', {'class': ['nova-legacy-e-text nova-legacy-e-text--size-m nova-legacy-e-text--family-sans-serif nova-legacy-e-text--spacing-none nova-legacy-e-text--color-grey-800 research-detail-middle-section__abstract']}).text
    except AttributeError:
        abstract = ''

    try:
        type = soup.find('span', {'class': ['nova-legacy-e-badge nova-legacy-e-badge--color-green nova-legacy-e-badge--display-inline nova-legacy-e-badge--luminosity-high nova-legacy-e-badge--size-l nova-legacy-e-badge--theme-solid nova-legacy-e-badge--radius-m research-detail-header-section__badge']}).text
    except AttributeError:
        type = ''

    try:
        available = soup.find('span', {'class': ['nova-legacy-e-badge nova-legacy-e-badge--color-green nova-legacy-e-badge--display-inline nova-legacy-e-badge--luminosity-medium nova-legacy-e-badge--size-l nova-legacy-e-badge--theme-ghost nova-legacy-e-badge--radius-m research-detail-header-section__badge']}).text
    except AttributeError:
        available = ''

    try:
        link = 'https://www.researchgate.net/' + soup.find('a', {'class': ['nova-legacy-c-button nova-legacy-c-button--align-center nova-legacy-c-button--radius-m nova-legacy-c-button--size-m nova-legacy-c-button--color-blue nova-legacy-c-button--theme-solid nova-legacy-c-button--width-full js-target-download-btn-5955cf35a6fdcc2569d6770a js-lite-click']}).get('href')
    except AttributeError:
        link = ''

    try:
        read = 'https://www.researchgate.net/' + soup.find('a', {'class': ['nova-legacy-c-button nova-legacy-c-button--align-left nova-legacy-c-button--radius-m nova-legacy-c-button--size-m nova-legacy-c-button--color-blue nova-legacy-c-button--theme-ghost nova-legacy-c-button--width-full gtm-read-full-text-btn-header-promo js-lite-click']}).get('href')
    except AttributeError:
        read = ''

    # дата, DOI, лецензия и т.д.
    # все идет беспорядочно, поэтому мною складывается в обычный массив
    # исключение сделать для DOI, но оставить также и в метаданных

    metadata = str(soup.find_all('div', {'class': ['research-detail-header-section__metadata']})[0])
    metadata_soup = bs4(metadata, "html.parser")
    metadata_list = []

    # разложить всю метадату
    for metadata_container in metadata_soup.find_all('div', {'class': ['nova-legacy-e-text nova-legacy-e-text--size-m nova-legacy-e-text--family-sans-serif nova-legacy-e-text--spacing-xxs nova-legacy-e-text--color-grey-700']}):
        containter_soup = bs4(str(metadata_container), "html.parser")
        metadata_list.append({containter_soup.text: containter_soup.find('a').get('href')})

    # поиск DOI
    DOI = ''
    for row in metadata_list:
        for key in row:
            if 'DOI' in key:
                DOI = row[key]
                break

    # все авторы

    authors = str(soup.find_all('div', {'class': ['nova-legacy-l-flex__item nova-legacy-l-flex nova-legacy-l-flex--gutter-m nova-legacy-l-flex--direction-column@s-up nova-legacy-l-flex--direction-row@m-up nova-legacy-l-flex--align-items-flex-start@s-up nova-legacy-l-flex--align-items-center@m-up nova-legacy-l-flex--justify-content-flex-start@s-up nova-legacy-l-flex--wrap-wrap@s-up research-detail-author-list__list js-authors-list']})[0])
    authors_soup = bs4(authors, "html.parser")
    authors_list = []

    #TODO: код ниже можно сделать поумнее

    # внутри блоков с авторами лежат еще ссылки, которые не визуально не видны и не нажимаемы
    # нужно от них исбавиться
    for authors_container in authors_soup.find_all('a'):
        authors_list.append([authors_container.text, authors_container.get('href')])

    temp = []
    for panel in authors_list:
        if panel[0] != ' ':
            if 'profile/' in panel[1]:
                temp.append({panel[0]: 'https://www.researchgate.net/' + panel[1]})
            elif 'scientific-contributions/' in panel[1]:
                temp.append({panel[0]: ''})

    # встречаются и дубликаты
    authors_list = []
    for elem in temp:
        if elem not in authors_list:
            authors_list.append(elem)

    # print(name)
    # print(abstract)
    # print(type)
    # print(available)
    # print(link)
    # print(read)
    # print(metadata_list)
    # print(DOI)
    print(authors_list)

    return {'name': name,
            'abstract': abstract,
            'DOI': DOI,
            'authors': authors_list,
            'type': type,
            'available': available,
            'download link': link,
            'read link': read,
            'metadata': metadata_list}