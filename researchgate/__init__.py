from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.common.exceptions import WebDriverException
from .exceptions import *
from os import path, makedirs
import warnings


class ResearchGateWebScraper:
    """Web scraper for https://www.researchgate.net"""

    # импорт методов класса
    from .institution_members import get_institution_members
    from .profile import get_profile_info
    from .private import _research_gate_page_404

    # удлось ли подключиться (доступен ли сайт)
    __is_connected = False
    # удалось ли авторизоваться
    _is_authorized = False
    # директории для выгрузки
    __nested = {'data': ('members', 'profile')}

    def __init__(self,
                 executable_path: str = None,
                 options: str = None,
                 login: str = None,
                 my_profile: str = None,
                 password: str = None,
                 cookie: dict = None,
                 ignore_authorization: bool = False):

        """Авторизоваться на сайте и создать selenium.webdriver, войти на www.researchgate.net."""

        # На сайте можно работать и авторизовавшись и без авторизации на сайте
        # во втором случае есть ограничения

        # если не существует, создать папки для выгрузки
        self._data_dir_path = 'researchgate_data'
        if not path.exists(self._data_dir_path):
            makedirs(self._data_dir_path)

        for fdir in self.__nested['data']:
            if not path.exists(f'{self._data_dir_path}/{fdir}'):
                makedirs(f'{self._data_dir_path}/{fdir}')

        final_options = None
        if options:
            if type(options) != Options:
                final_options = Options()
                final_options.add_argument(options)

        # Создать экземпляр драйвера webdriver
        try:
            self._driver = webdriver.Firefox(executable_path=executable_path, options=final_options)

        # если путь не найден, использовать настройки по-умолчанию
        except TypeError:
            self._driver = webdriver.Firefox(options=options)

        # не авторизовываться
        if not ignore_authorization:
            # Первая попытка авторизации на сайте, использование куки
            if cookie:
                # добавить куки к драйверу
                self._driver.add_cookie(cookie)

        # Сайти на сайт
        try:
            self._driver.get('https://www.researchgate.net')
        except WebDriverException:
            # если не доступен
            raise PageNotFoundException

        self._is_connected = True

        # не авторизовываться
        if not ignore_authorization:

            # Если перекидывет на страницу с "войти или зарегистрироваться"
            # то авторизация по сохраненным паролям и куки не прошла
            if not self._driver.find_element(By.CLASS_NAME, 'index-header__log-in') and \
                    self._driver.find_element(By.CLASS_NAME, 'index-header__sign-up gtm-new-index-page-join-btn-atf'):

                self._is_authorized = True

            else:
                # Авторизация через страницу "войти" с введенными логином и паролем
                self._driver.get('https://www.researchgate.net/login')

                # Ввести логин и пароль в форму, нажать на кнопку "войти" (это единственная <button> на странице)
                self._driver.find_element(By.ID, 'input-login').send_keys(login)
                self._driver.find_element(By.ID, 'input-password').send_keys(password)
                self._driver.find_element(By.CSS_SELECTOR, 'button').click()

                # Авторизаццция не прошла (адрес все еще https://www.researchgate.net/login)
                if self._driver.current_url == 'https://www.researchgate.net/login':
                    # raise AuthorizationFailedException

                    print('Authorization failed. Using unauthorized mode.')
                    self._is_authorized = False

                # Авторизация прошла успешно
                else:
                    print('Authorization succeed')
                    self._is_authorized = True

        else:
            print('Authorization ignored. Using unauthorized mode.')

        if self._is_authorized:
            self._my_profile = my_profile

    def connect(self):
        pass

    def disconnect(self):
        # if not self._is_authorized:
        #     warnings.warn('Unauthorized already')
        #     return
        pass

    @property
    def is_connected(self):
        return self.__is_connected

    @property
    def is_authorized(self):
        return self._is_authorized
