import requests
from db_manager import DBManager
from func import get_config, get_data_for_employers, get_data_for_vacancies


CONFIG_FILE = '../conf/config.ini'
response_keys = get_config(CONFIG_FILE, 'hh_ru')
employees_id = get_config(CONFIG_FILE, 'employees_id')
url = get_config(CONFIG_FILE, 'url')['url']
db = DBManager(CONFIG_FILE)
# db.create_database('db_hhru')
# print(db.param_connect)
# db.create_table_employers()
# db.create_table_vacancies()

# print(db.param_connect)
# for i in employees_id:
#     response_keys['employer_id'] = i
#     response = requests.get(url, response_keys)
#     data = response.json()
#     for j in data['items']:
        # in_table = get_data_for_employers(j)
        # print(get_data_for_employers(j))
        # print(get_data_for_vacancies(j))
        # db.into_table(' employers', 3, get_data_for_employers(j))
        # db.into_table('vacancies', 10, get_data_for_vacancies(j))

db.get_companies_and_vacancies_count()
db.get_all_vacancies()
db.close_connection()
#         print(j['area']['id'])
#         print(j['area']['name'])
#         print(j['id'])
#         print(j['name'])
#         print(j['employer']['id'])
#         print(j['employer']['name'])
#         print(j['professional_roles'][0]['name'])
#         print(j['salary']['from'])
#         print(j['salary']['to'])
#         print(j['salary']['currency'])
#         print(j['alternate_url'])
#         print(j['snippet']['requirement'])
#         print(j['snippet']['responsibility'])
#         print('=======================================================================================================')
