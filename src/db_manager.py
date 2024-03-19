from func import get_config, get_arguments, get_table_rows
import psycopg2


class DBManager:
    def __init__(self, config_file):
        self.param_connect = get_config(config_file, 'postgresql')
        self.conn = psycopg2.connect(**self.param_connect)
        self.cur = self.conn.cursor()

    def create_database(self, db_name):
        try:
            self.conn.autocommit = True
            self.cur = self.conn.cursor()
            self.cur.execute(f'DROP DATABASE IF EXISTS {db_name};')
            self.cur.execute(f'CREATE DATABASE {db_name};')
            print('DB create')
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            self.cur.close()
            self.conn.close()
            self.conn = psycopg2.connect(dbname=db_name, **self.param_connect)
            self.cur = self.conn.cursor()

    def create_table_employers(self):
        try:
            self.cur.execute('''CREATE TABLE employers
                                (vacancy_id int,
                                employer_id int,
                                employer_name varchar,
                                CONSTRAINT pk_employers_vacancy_id PRIMARY KEY (vacancy_id));''')
            print('Table employers create')
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)

    def create_table_vacancies(self):
        try:
            self.cur.execute('''CREATE TABLE vacancies
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
            print('Table vacancies create')
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)

    def into_table(self, table_name, columns, data):
        try:
            self.cur.execute(f'INSERT INTO {table_name} VALUES({get_arguments(columns)})', data)
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)

    def close_connection(self):
        self.cur.close()
        self.conn.commit()
        self.conn.close()

    def get_companies_and_vacancies_count(self):
        try:
            self.cur.execute('''SELECT employer_name, COUNT(*)
                                FROM employers
                                GROUP BY employer_name
                                ORDER BY COUNT(*);''')
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        get_table_rows(self.cur)

    def get_all_vacancies(self):
        try:
            self.cur.execute('''SELECT employers.employer_name, 
                                vacancy_name, salary_from, salary_to, url
                                FROM vacancies INNER JOIN employers
                                USING(vacancy_id);''')
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        get_table_rows(self.cur)

    def get_vacancies_with_higher_salary(self):
        try:
            self.cur.execute('''SELECT vacancy_id, vacancy_name, roles_name, salary_from, salary_to 
                                FROM vacancies
                                WHERE salary_from > (SELECT AVG (salary_from) FROM vacancies)
                                ORDER BY salary_from;''')
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        get_table_rows(self.cur)

    def get_avg_salary(self):
        try:
            self.cur.execute('SELECT AVG (salary_from) FROM vacancies')
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        get_table_rows(self.cur)

    def get_vacancies_with_keyword(self, key_world):
        try:
            self.cur.execute(f'''SELECT vacancy_id, vacancy_name, roles_name, url
                                FROM vacancies 
                                WHERE vacancy_name LIKE '%{key_world.lower()}%' 
                                OR vacancy_name LIKE '{key_world.title()}%'
                                OR vacancy_name LIKE '%{key_world.lower}'
                                OR roles_name LIKE '%{key_world.lower}%'
                                OR roles_name LIKE '{key_world.title}%'
                                OR roles_name LIKE '%{key_world.lower}';''')
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        get_table_rows(self.cur)
