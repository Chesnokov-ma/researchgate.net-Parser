from bs4 import BeautifulSoup as bs4


def __get_unaprofile(self) -> dict:
    """Парсинг профиля в неавторизованном моде"""

    un_profile = {'base_info': {},
                  'publications': {},
                  'stat': {}}

    source_data = self._driver.page_source
    soup = bs4(source_data, "html.parser")

    try:
        name = soup.find('div', {'class': ['nova-legacy-e-text nova-legacy-e-text--size-xl nova-legacy-e-text--family-display nova-legacy-e-text--spacing-xxs nova-legacy-e-text--color-inherit fn']}).text
    except AttributeError:
        name = soup.find('div', {'class': ['nova-legacy-e-text nova-legacy-e-text--size-xl nova-legacy-e-text--family-display nova-legacy-e-text--spacing-xxs nova-legacy-e-text--color-inherit']}).text

    try:
        institution = soup.find('div', {'class': ['nova-legacy-e-text nova-legacy-e-text--size-l nova-legacy-e-text--family-display nova-legacy-e-text--spacing-none nova-legacy-e-text--color-inherit nova-legacy-v-institution-item__title']}).text
    except AttributeError:
        institution = ''

    try:
        # department = soup.find_all('ul', {'class': ['nova-legacy-e-list nova-legacy-e-list--size-m nova-legacy-e-list--type-inline nova-legacy-e-list--spacing-none nova-legacy-v-institution-item__meta-data']})
        # children = department.findChildren('li', recursive=False)
        # department = [child.text for child in children]

        department = soup.find_all('li', {'class': ['nova-legacy-e-list__item nova-legacy-v-institution-item__meta-data-item']})
        department = [elem.text for elem in department]
    except AttributeError:
        department = []

    try:
        position = soup.find_all('li', {'class': ['nova-legacy-e-list__item nova-legacy-v-institution-item__info-section-list-item']})
        position = [elem.text for elem in position]
    except AttributeError:
        position = []

    try:
        lab = soup.find('div', {'class': ['nova-legacy-e-text nova-legacy-e-text--size-m nova-legacy-e-text--family-sans-serif nova-legacy-e-text--spacing-none nova-legacy-e-text--color-grey-900']})
        lab = lab.text
    except AttributeError:
        lab = ''

    un_profile['base_info']['name'] = name
    un_profile['base_info']['institution'] = institution
    un_profile['base_info']['department'] = department
    un_profile['base_info']['position'] = position
    un_profile['base_info']['lab'] = lab

    # TODO: если будет ошибка приделать try except AttributeError

    stat = soup.find_all('div', {'class': ['nova-legacy-e-text nova-legacy-e-text--size-xl nova-legacy-e-text--family-display nova-legacy-e-text--spacing-none nova-legacy-e-text--color-inherit']})
    number_of_publications = stat[0].text
    reads = stat[1].text
    citations = stat[2].text

    un_profile['stat']['number_of_publications'] = number_of_publications
    un_profile['stat']['reads'] = reads
    un_profile['stat']['citations'] = citations

    try:
        introduction = soup.find('span', {'class': ['Linkify']}).text
    except AttributeError:
        introduction = ''

    try:
        skills = soup.find('div', {'class': ['nova-legacy-l-flex__item nova-legacy-l-flex nova-legacy-l-flex--gutter-xs nova-legacy-l-flex--direction-row@s-up nova-legacy-l-flex--align-items-stretch@s-up nova-legacy-l-flex--justify-content-flex-start@s-up nova-legacy-l-flex--wrap-wrap@s-up js-target-skills']})
        children = skills.findChildren('div', recursive=False)
        skills = [child.text for child in children]
    except AttributeError:
        skills = []

    un_profile['base_info']['introduction'] = introduction
    un_profile['base_info']['skills'] = skills

    publications = []
    publ = str(soup.find_all('div', {'class': ['nova-legacy-c-card__body nova-legacy-c-card__body--spacing-none']})[0])
    publ_soup = bs4(publ, "html.parser")

    publications_soup = publ_soup.find_all('div', {'class': ['nova-legacy-o-stack__item']})
    for publication_container in publications_soup:
        containter_soup = bs4(str(publication_container), "html.parser")

        title = containter_soup.find('div', {'class': ['nova-legacy-e-text nova-legacy-e-text--size-l nova-legacy-e-text--family-display nova-legacy-e-text--spacing-none nova-legacy-e-text--color-inherit nova-legacy-v-publication-item__title']}).text

        publication_link = containter_soup.find('a', {'class': ['nova-legacy-c-button nova-legacy-c-button--align-center nova-legacy-c-button--radius-m nova-legacy-c-button--size-s nova-legacy-c-button--color-blue nova-legacy-c-button--theme-bare nova-legacy-v-publication-item__action']}).get('href')

        meta_left = containter_soup.find_all('div', {'class': ['nova-legacy-v-publication-item__meta-left']})

        if len(meta_left) == 2:
            publication_type = meta_left[0].text
            available = meta_left[1].text
        else:
            publication_type = meta_left[0].text
            available = ''

        publication_date = containter_soup.find('div', {'class': ['nova-legacy-v-publication-item__meta-right']}).text

        # try:
        #     description_not_full = containter_soup.find('div', {'class': ['nova-legacy-e-text nova-legacy-e-text--size-m nova-legacy-e-text--family-sans-serif nova-legacy-e-text--spacing-none nova-legacy-e-text--color-inherit nova-legacy-v-publication-item__description']}).text
        # except AttributeError:
        #     description_not_full = ''

        temp_dict = {'title': title, 'publication_type': publication_type, 'available': available,
                     'publication_date': publication_date, 'publication_link': publication_link}

        # 'publication_date': publication_date,

        publications.append(temp_dict)

        pass

    un_profile['publications'] = publications

    return un_profile
