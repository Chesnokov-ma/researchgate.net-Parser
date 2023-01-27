# researchgate.net-Parser
Парсер для сайта researchgate.net

## Примеры
```python
conf_data = json.load(open('config.json', 'r'))

sergate_ws = ResearchGateWebScraper(conf_data['EXE_PATH'], options='-headless',
                                    login=conf_data['login'], password=conf_data['password'],
                                    my_profile=conf_data['my_profile'],
                                    ignore_authorization=False)

# список ученных из выбранного института
sergate_ws.get_institution_members('https://www.researchgate.net/institution/Joint-Institute-for-Nuclear-Research/members', stop_page=13, light_search=True)
# sergate_ws.get_institution_members('Joint-Institute-for-Nuclear-Research', stop_page=13, light_search=True)

# профиль
sergate_ws.get_profile_info('https://www.researchgate.net/profile/Armin-Kleibert')
# sergate_ws.get_profile_info('Armin-Kleibert')

# страница статьи
sergate_ws.get_publication_info('https://www.researchgate.net/publication/317614509_Engineering_the_breaking_of_time-reversal_symmetry_in_gate-tunable_hybrid_ferromagnettopological_insulator_heterostructures')
# sergate_ws.get_publication_info('317614509_Engineering_the_breaking_of_time-reversal_symmetry_in_gate-tunable_hybrid_ferromagnettopological_insulator_heterostructures')
```

# conf.json
```json
{
  "EXE_PATH" : "/geckodriver.exe",
  "login" : "login@gmail.com",
  "password" :  "password"
}
```
