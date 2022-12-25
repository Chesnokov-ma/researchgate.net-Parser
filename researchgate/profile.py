from .exceptions import *
from .profile_private.aprofile import __get_aprofile
from .profile_private.unaprofile import __get_unaprofile
import json
import warnings


def get_profile_info(self,
                     profile: str = None,
                     p_url: str = None) -> None:
    """Получить игформацию из профиля"""

    if not profile and not p_url:
        raise LinkNotProvidedException

    if profile:
        # в unauthorized mode профиль - это 1 страница, иначе - 3 страницы
        profile = profile.replace('https://www.researchgate.net/profile/', '').replace(' ', '-')

        # Сначала проверить, существует ли такой профиль
        self._driver.get(f'https://www.researchgate.net/profile/{profile}')

    if not profile:
        self._driver.get(p_url)

    if self._research_gate_page_404():
        raise PageNotFoundException(self._driver.current_url)

    # проверка, свой ли профиль
    if self._is_authorized:
        if self._driver.current_url == f'https://www.researchgate.net/profile/{self._my_profile}' \
                or self._driver.current_url == p_url:
            warnings.warn('Used profile from config.json')
            return

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
    print(f'[PROFILE {"A" if self._is_authorized else "UN"}]: {profile.replace("-", "_")} - collected.')
