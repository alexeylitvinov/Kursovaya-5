from configparser import ConfigParser


def get_config(filename, section):
    parser = ConfigParser()
    parser.read(filename)
    data = {}
    params = parser.items(section)
    for param in params:
        data[param[0]] = param[1]
    return data


def get_data_for_employers(data):
    vacancy_id = int(data['id'])
    employer_id = int(data['employer']['id'])
    employer_name = data['employer']['name']
    return vacancy_id, employer_id, employer_name


def get_data_for_vacancies(data):
    vacancy_id = int(data['id'])
    vacancy_name = data['name']
    city_name = data['area']['name']
    roles_name = data['professional_roles'][0]['name']
    salary_from = get_validation_salary(data['salary']['from'])
    salary_to = get_validation_salary(data['salary']['to'])
    currency = data['salary']['currency']
    url = data['alternate_url']
    requirement = data['snippet']['requirement']
    responsibility = data['snippet']['responsibility']
    return (vacancy_id, vacancy_name, city_name, roles_name, salary_from, salary_to, currency, url, requirement,
            responsibility)


def get_table_rows(cur):
    rows = cur.fetchall()
    for i in rows:
        print(i)


def get_arguments(quantity: int) -> str:
    """
    Принимает на вход число (количество столбцов) возвращает строку '%s' с нужным количеством
    '%s' разделенных запятой
    """
    list_symbols = ['%s' for _ in range(quantity)]
    result = ', '.join(list_symbols)
    return result


def get_validation_salary(num: str) -> int:
    """
    Если не указано поле salary вместо None возвращает 0
    :param num: str
    :return: int
    """
    if num is None:
        num = 0
        return num
    return int(num)
