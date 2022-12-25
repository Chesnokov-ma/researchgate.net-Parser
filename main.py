from researchgate import ResearchGateWebScraper
import json

#TODO
# connect_disconnect
# русские символы в json (+)
# статьи ajax (-)
# поправить поиск статистики просто через find_all (+)
# переписать members через bs4 (~)
# проверка на пренадлежность профиля (+)
# сделать json похожими (~)
# неправильные ссылки в am research !!!!!!!!!!!!!!!!!!!!!!!!!

conf_data = json.load(open('config.json', 'r'))

sergate_ws = ResearchGateWebScraper(conf_data['EXE_PATH'], #options='-headless',
                                    login=conf_data['login'], password=conf_data['password'],
                                    my_profile=conf_data['my_profile'],
                                    ignore_authorization=True)

# список ученных из выбранного института
# sergate_ws.get_institution_members('Joint-Institute-for-Nuclear-Research', stop_page=13, light_search=True)


# парсинг профиля
sergate_ws.get_profile_info('Michael-Saccone-2')
sergate_ws.get_profile_info('https://www.researchgate.net/profile/Mikhail-Chesnokov-2')
sergate_ws.get_profile_info('https://www.researchgate.net/profile/Alan-Farhan')
sergate_ws.get_profile_info('Kevin-Hofhuis')

sergate_ws.get_profile_info('https://www.researchgate.net/profile/Armin-Kleibert')
sergate_ws.get_profile_info('Karl-Heinz-Meiwes-Broer')
sergate_ws.get_profile_info('Josef-Tiggesbaeumker')






pass