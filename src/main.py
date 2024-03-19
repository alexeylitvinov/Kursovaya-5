import requests
from db_manager import DBManager
from menu import user_menu
from func import get_config, get_data_for_employers, get_data_for_vacancies

CONFIG_FILE = '../conf/config.ini'


def user_main() -> None:
    """
    Функция для взаимодействия с пользователем
    :return: None
    """
    response_keys = get_config(CONFIG_FILE, 'hh_ru')
    employees_id = get_config(CONFIG_FILE, 'employees_id')
    url = get_config(CONFIG_FILE, 'url')['url']

    db = DBManager(CONFIG_FILE)
    db.create_database('db_hhru')
    db.create_table_employers()
    db.create_table_vacancies()

    print('Заполняем таблицы...')
    for i in employees_id:
        response_keys['employer_id'] = i
        response = requests.get(url, response_keys)
        data = response.json()
        for j in data['items']:
            db.into_table(' employers', 3, get_data_for_employers(j))
            db.into_table('vacancies', 10, get_data_for_vacancies(j))

    while True:
        user_menu()
        command = input('Введите команду: ')
        if command == '1':
            db.get_companies_and_vacancies_count()
        elif command == '2':
            db.get_all_vacancies()
        elif command == '3':
            db.get_avg_salary()
        elif command == '4':
            db.get_vacancies_with_higher_salary()
        elif command == '5':
            key_word = input('Введите ключевое слово: ')
            db.get_vacancies_with_keyword(key_word)
        elif command == '0':
            db.close_connection()
            break
        else:
            print('Нет такой команды...')


if __name__ == '__main__':
    user_main()
