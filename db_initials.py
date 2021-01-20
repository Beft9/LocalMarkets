import psycopg2 as dbapi2


dsn = "user='postgres' password='1234' host='localhost' port=5432 dbname='beft9'"
'''
# Date type definition
with dbapi2.connect(dsn) as connection:
    cursor = connection.cursor()
    statement = """CREATE TYPE DATE AS(
            DAY INTEGER, MONTH INTEGER, HOUR INTEGER) 
        """
    cursor.execute(statement)
    cursor.close()
'''



with dbapi2.connect(dsn) as connection:
    cursor = connection.cursor()
    statement = """CREATE TABLE COMPANY(
        id SERIAL PRIMARY KEY,
        Name VARCHAR(255) UNIQUE NOT NULL,
        Location VARCHAR(255))
        """
    cursor.execute(statement)
    cursor.close()

with dbapi2.connect(dsn) as connection:
    cursor = connection.cursor()
    statement = """CREATE TABLE PERSON(
        Username VARCHAR(255) UNIQUE PRIMARY KEY,
        Password VARCHAR(255) NOT NULL,
        Name VARCHAR(255) NOT NULL,
        Surname VARCHAR(255) NOT NULL,
        Email VARCHAR(255) UNIQUE NOT NULL,
        Location VARCHAR(255),
        Company_id INTEGER,
        CONSTRAINT Company_fk FOREIGN KEY(Company_id) REFERENCES COMPANY (id))
        """
    cursor.execute(statement)
    cursor.close()

with dbapi2.connect(dsn) as connection:
    cursor = connection.cursor()
    statement = """CREATE TABLE PRODUCT(
        id SERIAL PRIMARY KEY,
        Name VARCHAR(255) NOT NULL,
        Image VARCHAR(255) NOT NULL,
        Brand VARCHAR(255) NOT NULL,
        Model VARCHAR(255) NOT NULL,
        View_Number INTEGER DEFAULT  0,
        Quantity INTEGER NOT NULL,
        Price FLOAT NOT NULL,
        Company_id INTEGER,
        CONSTRAINT company_fk FOREIGN KEY(Company_id) REFERENCES COMPANY (id),
        Category VARCHAR(255) NOT NULL,
        CHECK ((Price >= 0) AND (Quantity >= 0)))
        """
    cursor.execute(statement)
    cursor.close()

with dbapi2.connect(dsn) as connection:
    cursor = connection.cursor()
    statement = """CREATE TABLE SOLD_PRODUCT(
        id SERIAL PRIMARY KEY,
        Date DATE NOT NULL,
        product_id INTEGER,
        CONSTRAINT product_fk FOREIGN KEY(product_id) REFERENCES PRODUCT (id))
        """
    cursor.execute(statement)
    cursor.close()

with dbapi2.connect(dsn) as connection:
    cursor = connection.cursor()
    statement = """CREATE TABLE CART(
        product_id INTEGER,
        Username VARCHAR(255),
        CONSTRAINT product_fk FOREIGN KEY(product_id) REFERENCES PRODUCT (id) ON DELETE CASCADE,
        CONSTRAINT person_fk FOREIGN KEY(Username) REFERENCES PERSON (Username) ON DELETE CASCADE)
        """
    cursor.execute(statement)
    cursor.close()




