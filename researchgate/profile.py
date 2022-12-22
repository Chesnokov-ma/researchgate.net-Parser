from bs4 import BeautifulSoup as bs4
import json

from .exceptions import *


def get_profile_info(self,
                     profile: str,
                     p_url: str = None) -> None:
    """Получить игформацию из профиля"""

    # в unauthorized mode профиль - это 1 страница, иначе - 3 страницы
    profile = profile.replace(' ', '-')

    # Сначала проверить, существует ли такой институт
    self._driver.get(f'https://www.researchgate.net/profile/{profile}')

    if self._research_gate_page_404():
        if p_url:  # если есть ссылка на профиль
            self._driver.get(p_url)
            if self._research_gate_page_404():
                raise PageNotFoundException(self._driver.current_url)
        else:
            raise PageNotFoundException(self._driver.current_url)  # если нет, завершить - выкинуть исключение

    this_page_is_valid = True  # сущесттвует ли текущая страница
    profile = {}  # словарь бля хранения данных о профиле

    # теги для двух версий отличаются
    if not self._is_authorized:
        __get_unaprofile(self)
    else:
        __get_aprofile(self, ('/research', '/stats'))


def __get_aprofile(self, pages: tuple):
    source_data = self._driver.page_source
    soup = bs4(source_data, "html.parser")

    # поиск по разметке

    name = soup.find('div', {'class': ['nova-legacy-e-text nova-legacy-e-text--size-xl nova-legacy-e-text--family-display nova-legacy-e-text--spacing-none nova-legacy-e-text--color-grey-900']}).text

    # информация расположена в одной строке без тегов, программно нельзя понять, что к чему относится
    info = soup.find('ul', {'class': ['nova-legacy-e-list nova-legacy-e-list--size-l nova-legacy-e-list--type-inline nova-legacy-e-list--spacing-none']})
    children = info.findChildren('li', recursive=False)
    info = [child.text for child in children]

    introduction = soup.find('div', {'class': ['nova-legacy-e-text nova-legacy-e-text--size-m nova-legacy-e-text--family-sans-serif nova-legacy-e-text--spacing-none nova-legacy-e-text--color-grey-900']}).text

    disciplines = soup.find('ul', {'class': ['nova-legacy-e-list nova-legacy-e-list--size-m nova-legacy-e-list--type-inline nova-legacy-e-list--spacing-none']})
    children = disciplines.findChildren('li', recursive=False)
    disciplines = [child.text for child in children]

    skills = soup.find('ul', {'class': ['nova-legacy-e-list nova-legacy-e-list--size-m nova-legacy-e-list--type-inline nova-legacy-e-list--spacing-none']})
    children = skills.findChildren('li', recursive=False)
    kills = [child.text for child in children]

    activity = soup.find('ul', {'class': ['nova-legacy-e-list nova-legacy-e-list--size-m nova-legacy-e-list--type-inline nova-legacy-e-list--spacing-xxs']})
    children = activity.findChildren('li', recursive=False)
    activity = [child.text for child in children]


    print(name)



def __get_unaprofile(self):
    pass


def __get_research(self):
    pass
