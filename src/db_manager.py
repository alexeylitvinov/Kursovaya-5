from func import get_config, get_arguments, get_table_rows
import psycopg2


class DBManager:
    """
    Класс для работы с базой данных и таблицами
    """
    def __init__(self, config_file):
        self.__param_connect = get_config(config_file, 'postgresql')
        self.__conn = psycopg2.connect(**self.__param_connect)
        self.__cur = self.__conn.cursor()

    def create_database(self, db_name: str) -> None:
        """
        Создаем новую базу данных, если такая уже существует удаляем и создаем заново
        :param db_name: str
        :return: None
        """
        try:
            self.__conn.autocommit = True
            self.__cur = self.__conn.cursor()
            self.__cur.execute(f'DROP DATABASE IF EXISTS {db_name};')
            self.__cur.execute(f'CREATE DATABASE {db_name};')
            print(f'База данных {db_name} создана')
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            self.__cur.close()
            self.__conn.close()
            self.__conn = psycopg2.connect(dbname=db_name, **self.__param_connect)
            self.__cur = self.__conn.cursor()

    def create_table_employers(self) -> None:
        """
        Создаем таблицу employers
        return: None
        """
        try:
            self.__cur.execute('''CREATE TABLE employers
                                (vacancy_id int,
                                employer_id int,
                                employer_name varchar,
                                CONSTRAINT pk_employers_vacancy_id PRIMARY KEY (vacancy_id));''')
            print('Таблица employers создана')
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)

    def create_table_vacancies(self) -> None:
        """
        Создаем таблицу vacancies
        :return: None
        """
        try:
            self.__cur.execute('''CREATE TABLE vacancies
                                (vacancy_id int,
                                vacancy_name varchar,
                                city_name varchar,
                                roles_name varchar,
                                salary_from int,
                                salary_to int,
                                currency char(3),
                                url varchar,
                                requirement text,
                                responsibility text,
                                CONSTRAINT pk_vacancies_vacancy_id PRIMARY KEY (vacancy_id));
                                ALTER TABLE vacancies ADD CONSTRAINT fk_vacancies_vacancy_id FOREIGN KEY (vacancy_id)
                                REFERENCES employers(vacancy_id);''')
            print('Таблица vacancies создана')
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)

    def into_table(self, table_name: str, columns: int, data: tuple) -> None:
        """
        Принимает на вход название таблицы, количество столбцов, данные и заполняет таблицу
        :param table_name: str
        :param columns: int
        :param data: tuple
        :return: None
        """
        try:
            self.__cur.execute(f'INSERT INTO {table_name} VALUES({get_arguments(columns)})', data)
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)

    def close_connection(self) -> None:
        """
        Закрываем коннект с базой данных
        :return: None
        """
        self.__cur.close()
        self.__conn.commit()
        self.__conn.close()

    def get_companies_and_vacancies_count(self) -> None:
        """
        Получает список всех компаний и количество вакансий у каждой компании
        :return: None
        """
        try:
            self.__cur.execute('''SELECT employer_name, COUNT(*)
                                FROM employers
                                GROUP BY employer_name
                                ORDER BY COUNT(*);''')
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        get_table_rows(self.__cur)

    def get_all_vacancies(self) -> None:
        """
        Получает список всех вакансий с указанием названия компании, названия вакансии и зарплаты и ссылки на вакансию
        :return: None
        """
        try:
            self.__cur.execute('''SELECT employers.employer_name, 
                                vacancy_name, salary_from, salary_to, url
                                FROM vacancies INNER JOIN employers
                                USING(vacancy_id);''')
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        get_table_rows(self.__cur)

    def get_vacancies_with_higher_salary(self) -> None:
        """
        Получает список всех вакансий, у которых зарплата выше средней по всем вакансиям
        :return: None
        """
        try:
            self.__cur.execute('''SELECT vacancy_id, vacancy_name, roles_name, salary_from, salary_to 
                                FROM vacancies
                                WHERE salary_from > (SELECT AVG (salary_from) FROM vacancies)
                                ORDER BY salary_from;''')
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        get_table_rows(self.__cur)

    def get_avg_salary(self) -> None:
        """
        Получает среднюю зарплату по вакансиям
        :return: None
        """
        try:
            self.__cur.execute('SELECT AVG (salary_from) FROM vacancies')
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        get_table_rows(self.__cur)

    def get_vacancies_with_keyword(self, key_world: str) -> None:
        """
        Получает список всех вакансий, в названии которых содержатся переданные в метод слова
        :param key_world: str
        :return: None
        """
        try:
            self.__cur.execute(f'''SELECT vacancy_id, vacancy_name, roles_name, url
                                FROM vacancies 
                                WHERE vacancy_name LIKE '%{key_world.lower()}%' 
                                OR vacancy_name LIKE '{key_world.title()}%'
                                OR vacancy_name LIKE '%{key_world.lower}'
                                OR roles_name LIKE '%{key_world.lower}%'
                                OR roles_name LIKE '{key_world.title}%'
                                OR roles_name LIKE '%{key_world.lower}';''')
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        get_table_rows(self.__cur)
