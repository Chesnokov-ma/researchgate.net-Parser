from bs4 import BeautifulSoup as bs4
from .exceptions import *
from .profile_private.aprofile import __get_aprofile
from .profile_private.unaprofile import __get_unaprofile
import json


def get_profile_info(self,
                     profile: str,
                     p_url: str = None) -> None:
    """Получить игформацию из профиля"""

    # в unauthorized mode профиль - это 1 страница, иначе - 3 страницы
    profile = profile.replace(' ', '-')

    # Сначала проверить, существует ли такой профиль
    self._driver.get(f'https://www.researchgate.net/profile/{profile}')

    if self._research_gate_page_404():
        if p_url:  # если есть ссылка на профиль
            self._driver.get(p_url)
            if self._research_gate_page_404():
                raise PageNotFoundException(self._driver.current_url)
        else:
            raise PageNotFoundException(self._driver.current_url)  # если нет, завершить - выкинуть исключение

    if not profile:
        profile = p_url.replace('https://www.researchgate.net/profile/', '')

    # this_page_is_valid = True  # сущесттвует ли текущая страница
    profile_dict = {profile: {}}  # словарь бля хранения данных о профиле

    # теги для двух версий отличаются
    # TODO: выходной файл тоже
    if not self._is_authorized:
        profile_dict[profile] = __get_unaprofile(self)
    else:
        profile_dict[profile] = __get_aprofile(self, ('/research', '/stats'))

    # print(profile_dict)

    # Запись в json-файл

    with open(f'{self._data_dir_path}/profile/{profile.replace("-", "_")}'
              f'{"" if self._is_authorized else "_unauthorized"}.json', 'w', encoding='utf-8') as js_out:
        json.dump(profile_dict, js_out, ensure_ascii=False)
    print(f'[PROFILE]: {profile.replace("-", "_")} - collected.')
