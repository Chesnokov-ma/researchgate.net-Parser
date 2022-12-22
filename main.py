from researchgate import ResearchGateWebScraper
import json

#TODO
# connect_disconnect
# русские символы в json (+)
# статьи
#

conf_data = json.load(open('config.json', 'r'))

sergate_ws = ResearchGateWebScraper(conf_data['EXE_PATH'], options='-headless',
                                    login=conf_data['login'], password=conf_data['password'],)  #

# список ученных из выбранного института
# sergate_ws.get_institution_members('Joint-Institute-for-Nuclear-Research', stop_page=13, light_search=True)

sergate_ws.get_profile_info('B-Plourde')










pass