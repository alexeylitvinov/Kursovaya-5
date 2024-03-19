import requests
from db_manager import DBManager
from func import get_config, get_data_for_employers, get_data_for_vacancies


CONFIG_FILE = '../conf/config.ini'
response_keys = get_config(CONFIG_FILE, 'hh_ru')
employees_id = get_config(CONFIG_FILE, 'employees_id')
url = get_config(CONFIG_FILE, 'url')['url']

db = DBManager(CONFIG_FILE)
db.create_database('db_hhru')
db.create_table_employers()
db.create_table_vacancies()

print('Fill the table')
for i in employees_id:
    response_keys['employer_id'] = i
    response = requests.get(url, response_keys)
    data = response.json()
    for j in data['items']:
        db.into_table(' employers', 3, get_data_for_employers(j))
        db.into_table('vacancies', 10, get_data_for_vacancies(j))

# db.get_companies_and_vacancies_count()
# db.get_all_vacancies()
# db.get_avg_salary()
# db.get_vacancies_with_keyword('менеджер')
# db.get_vacancies_with_higher_salary()
db.close_connection()
