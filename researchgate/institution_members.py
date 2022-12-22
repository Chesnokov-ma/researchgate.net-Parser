from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import json

from .exceptions import PageNotFoundException


def get_institution_members(self,
                            institution: str,
                            start_page: int = 1,
                            stop_page: int = None,
                            light_search: bool = False) -> None:

    """Получить информацио о ученных из института. Для light_search == True
    лучше использовать unauthorized mode."""

    institution = institution.replace(' ', '-')
    current_page = start_page

    # Сначала проверить, существует ли такой институт
    self._driver.get(f'https://www.researchgate.net/institution/{institution}/members/{current_page}')

    if self._research_gate_page_404():
        raise PageNotFoundException(self._driver.current_url)  # если нет, завершить - выкинуть исключение

    this_page_is_valid = True  # сущесттвует ли следующая страница
    institution_members = {}  # словарь бля хранения данных о ученных

    # обязательные параметры
    name, profile_link = None, None
    # необязательные параметры
    photo, department, disciplines = None, None, None

    # Цикл по institution members от start_page до stop_page
    while this_page_is_valid:

        # Найти все блоки с информацие на странице
        for member in self._driver.find_elements(By.CLASS_NAME, 'nova-legacy-v-person-list-item'):

            name = member.find_element(By.CLASS_NAME, 'nova-legacy-v-person-list-item__align-content a')
            profile_link = name.get_attribute('href')

            # скачать только имя и ссылку на профиль
            if not light_search:

                photo = member.find_element(By.CLASS_NAME, 'nova-legacy-e-avatar__img').get_attribute('src')

                # департамента может и не быть, по тегу или классу find_element почему то не ищет, даже если есть
                # пока такой костыль
                temp_text = member.text.split('\n')
                if temp_text[1] == 'Department':
                    department = temp_text[2]
                else:
                    department = ''

                # дисциплины могут быть не указаны
                try:
                    disciplines = [dis.text for dis in member.find_elements(By.CSS_SELECTOR, 'span .nova-legacy-e-link')]
                except NoSuchElementException:
                    disciplines = []

            # добавление в словарь с именем в качестве ключа
            institution_members[name.text] = {}
            institution_members[name.text]['profile_link'] = profile_link

            if not light_search:
                institution_members[name.text]['photo'] = photo
                institution_members[name.text]['department'] = department
                institution_members[name.text]['disciplines'] = disciplines

        # вывыод страницы для отладки
        # print(current_page)

        # На слудющую страницу
        current_page += 1
        self._driver.get(f'https://www.researchgate.net/institution/{institution}/members/{current_page}')

        # Если страница не найдена, цикл завершается
        if self._research_gate_page_404() or current_page == stop_page + 1:
            stop_page = current_page - 1
            this_page_is_valid = False

    # Запись в json-файл
    with open(f'{self._data_dir_path}/members/{institution.replace("-", "_")}_{start_page}-{stop_page}_'
              f'{"" if not light_search else "light"}.json', 'w', encoding='utf-8') as js_out:
        json.dump(institution_members, js_out, ensure_ascii=False)
    print(f'Data for {institution.replace("-", "_")} collected.')
