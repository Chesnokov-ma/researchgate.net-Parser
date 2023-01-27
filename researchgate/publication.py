from .exceptions import *
from .publication_private.unapublication import __get_unapublication
from .publication_private.apublication import __get_apublication
import json


def get_publication_info(self,
                     research: str = None,
                     r_url: str = None) -> None:

    if not research and not r_url:
        raise LinkNotProvidedException

    if research:
        research = research.replace('https://www.researchgate.net/publication/', '').replace(' ', '-')
        self._driver.get(f'https://www.researchgate.net/publication/{research}')

    if not research:
        self._driver.get(r_url)

    research_dict = {}

    if not self._is_authorized:
        research_dict = __get_unapublication(self)
    else:
        research_dict = __get_apublication(self)

    # Запись в json-файл

    with open(f'{self._data_dir_path}/research/{research.replace("-", "_")}'
              f'{"" if self._is_authorized else "_unauthorized"}.json', 'w', encoding='utf-8') as js_out:
        json.dump(research_dict, js_out, ensure_ascii=False)
    print(f'[RESEARCH {"A" if self._is_authorized else "UN"}]: {research.replace("-", "_")} - collected.')