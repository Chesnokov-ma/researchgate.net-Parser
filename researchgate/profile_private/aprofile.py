from bs4 import BeautifulSoup as bs4
from ..exceptions import *
import time

def __get_aprofile(self, pages: tuple) -> dict:
    """Парсинг профиля в авторизованном моде"""

    source_data = self._driver.page_source
    soup = bs4(source_data, "html.parser")

    dict_output = {}

    # поиск по разметке

    name = soup.find('div', {'class': ['nova-legacy-e-text nova-legacy-e-text--size-xl nova-legacy-e-text--family-display nova-legacy-e-text--spacing-none nova-legacy-e-text--color-grey-900']}).text

    # информация расположена в одной строке без тегов, программно нельзя понять, что к чему относится
    info = soup.find('ul', {'class': ['nova-legacy-e-list nova-legacy-e-list--size-l nova-legacy-e-list--type-inline nova-legacy-e-list--spacing-none']})
    children = info.findChildren('li', recursive=False)
    info = [child.text for child in children]

    # Параметров ниже может не быть

    try:
        introduction = soup.find('div', {'class': ['nova-legacy-e-text nova-legacy-e-text--size-m nova-legacy-e-text--family-sans-serif nova-legacy-e-text--spacing-none nova-legacy-e-text--color-grey-900']}).text
    except AttributeError:
        introduction = ''

    try:
        disciplines = soup.find('ul', {'class': ['nova-legacy-e-list nova-legacy-e-list--size-m nova-legacy-e-list--type-inline nova-legacy-e-list--spacing-none']})
        children = disciplines.findChildren('li', recursive=False)
        disciplines = [child.text for child in children]
    except AttributeError:
        disciplines = []

    try:
        skills = soup.find_all('ul', {'class': ['nova-legacy-e-list nova-legacy-e-list--size-m nova-legacy-e-list--type-inline nova-legacy-e-list--spacing-none']})[1]
        children = skills.findChildren('li', recursive=False)
        skills = [child.text for child in children]
    except AttributeError:
        skills = []

    try:
        activity = soup.find('ul', {'class': ['nova-legacy-e-list nova-legacy-e-list--size-m nova-legacy-e-list--type-inline nova-legacy-e-list--spacing-xxs']})
        children = activity.findChildren('li', recursive=False)
        activity = [child.text for child in children]
    except AttributeError:
        activity = []

    # подготовить итоговый словарь
    dict_output['base_info'] = {
        'name': name,
        'introduction': introduction,
        'disciplines': disciplines,
        'skills': skills,
        'activity': activity,
        'base_info': info,
    }

    # Research (Статьи)
    dict_output['publications'] = __get_aresearch(self, pages[0])

    # Stat (Статистика)
    dict_output['stat'] = __get_stat(self, pages[1])

    return dict_output


def __get_aresearch(self, add_to_url: str) -> dict:
    """Парсинг статей в авторизованном моде, ajax-запросы"""

    self._driver.get(f'{self._driver.current_url}{add_to_url}')
    if self._research_gate_page_404():
        raise PageNotFoundException(self._driver.current_url)

    publications = []

    source_data = self._driver.page_source
    soup = bs4(source_data, "html.parser")

    publ = str(soup.find_all('div', {'class': ['nova-legacy-o-stack nova-legacy-o-stack--gutter-xxxl nova-legacy-o-stack--spacing-none nova-legacy-o-stack--show-divider nova-legacy-o-stack--no-gutter-outside']}))
    publ_soup = bs4(publ, "html.parser")

    publications_soup = publ_soup.find_all('div', {'class': ['nova-legacy-v-publication-item nova-legacy-v-publication-item--size-m']})

    for publication_container in publications_soup:
        containter_soup = bs4(str(publication_container), "html.parser")

        title = containter_soup.find('div', {'class': ['nova-legacy-e-text nova-legacy-e-text--size-l nova-legacy-e-text--family-display nova-legacy-e-text--spacing-none nova-legacy-e-text--color-inherit nova-legacy-v-publication-item__title']}).text

        publication_link = containter_soup.find('a', {'class': ['nova-legacy-e-link nova-legacy-e-link--color-inherit nova-legacy-e-link--theme-bare']}).get('href')
        publication_link = publication_link[:publication_link.find('?')]

        meta_left = containter_soup.find_all('div', {'class': ['nova-legacy-v-publication-item__meta-left']})

        if len(meta_left) == 2:
            publication_type = meta_left[0].text
            available = meta_left[1].text
        else:
            publication_type = meta_left[0].text
            available = ''

        try:
            publication_date = containter_soup.find_all('li', {'class': ['nova-legacy-e-list__item nova-legacy-v-publication-item__meta-data-item']})[0].text
        except AttributeError:
            publication_date = ''

        temp_dict = {'title': title, 'publication_type': publication_type, 'available': available,
                    'publication_date': publication_date,
                     'publication_link': f'https://www.researchgate.net/{publication_link}'}

        publications.append(temp_dict)

    return publications


def __get_stat(self, add_to_url: str) -> dict:
    """Парсинг статистики профиля в авторизованном моде"""

    self._driver.get(f'{self._driver.current_url.replace("/research", "/stats")}')
    if self._research_gate_page_404():
        raise PageNotFoundException(self._driver.current_url)

    source_data = self._driver.page_source
    soup = bs4(source_data, "html.parser")

    # статистика доступна для любого аккаунта

    stat_info = soup.find_all('div', {'class': ['nova-legacy-e-text nova-legacy-e-text--size-xxxl nova-legacy-e-text--family-display nova-legacy-e-text--spacing-none nova-legacy-e-text--color-inherit']})
    stat = [elem.text for elem in stat_info]

    # сложить в словарь
    return {'research_interest_score': stat[0],
            'reads': stat[1],
            'citations': stat[2],
            'recommendations': stat[3],
            'h_index': stat[4],
            'h_index_excl': stat[5]}