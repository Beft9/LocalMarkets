import psycopg2 as dbapi2


dsn = "user='postgres' password='1234' host='localhost' port=5432 dbname='beft9'"

class User:
    def __init__(self, username, name, surname, email, password, location=None, company_id=None):
        self.username = username
        self.name = name
        self.surname = surname
        self.email = email
        self.location = location
        self.password = password
        self.company_id = company_id

    def AddtoDatabase(self):
        with dbapi2.connect(dsn) as connection:
            cursor = connection.cursor()
            statement = """INSERT INTO PERSON (username, password, name, surname, email, location) VALUES (
                '{}', '{}', '{}', '{}', '{}', '{}');
                """.format(self.username, self.password,self.name,self.surname,self.email, self.location)
            cursor.execute(statement)
            cursor.close()
    
    def Set_Company_ID(self,company_id):
        with dbapi2.connect(dsn) as connection:
            cursor = connection.cursor()
            statement = """UPDATE PERSON SET company_id = {} WHERE username = '{}';""".format(company_id, self.username)
            self.company_id = company_id
            cursor.execute(statement)
            cursor.close()


class Company:
    def __init__(self, name, location, id=None):
        self.id = id
        self.name = name
        self.location = location

    def AddtoDatabase(self):
        with dbapi2.connect(dsn) as connection:
            cursor = connection.cursor()
            statement = """INSERT INTO COMPANY (name, location) VALUES(
                '{}','{}') RETURNING id;""".format(self.name,self.location)
            cursor.execute(statement)
            for row in cursor:
                self.id = row[0]
                cursor.close()
                return self.id

            

class SoldProduct:
    def __init__(self, id, date, product_id):
        self.id = id
        self.date = date
        self.product_id = product_id

    def AddtoDatabase(self):
        with dbapi2.connect(dsn) as connection:
            cursor = connection.cursor()
            statement = """INSERT INTO PERSON() VALUES(
                {},{},{})
                """.format(self.id,self.date,self.product_id)
            cursor.execute(statement)
            cursor.close()

class Cart:
    def __init__(self, username,product_id):
        self.username = username
        self.product_id = product_id

    def AddtoDatabase(self):
        with dbapi2.connect(dsn) as connection:
            cursor = connection.cursor()
            statement = """INSERT INTO CART VALUES(
                {},'{}')
                """.format(self.product_id,self.username)
            cursor.execute(statement)
            cursor.close()

class Product:
    def __init__(self,name,image,brand,model, view, quantity, price, company_id, category, id=None):
        self.id = id
        self.name = name
        self.image = image
        self.brand = brand
        self.model = model
        self.view = view
        self.quantity = quantity
        self.price = price
        self.company_id = company_id
        self.category = category

    def AddtoDatabase(self):
        with dbapi2.connect(dsn) as connection:
            cursor = connection.cursor()
            statement = """INSERT INTO PRODUCT VALUES(
                {},'{}','{}','{}','{}',{},{},{},{},'{}') RETURNING id;
                """.format('DEFAULT',self.name,self.image,self.brand,self.model, self.view, self.quantity, self.price, self.company_id,self.category)
            cursor.execute(statement)
            for row in cursor:
                cursor.close()
                self.id = row[0]
                return self.id
            cursor.close()


def Check_User(username, password):
    with dbapi2.connect(dsn) as connection:
        with connection.cursor() as cursor:
            statement = """select * FROM PERSON where person.username = '{}' and person.password = '{}'""".format(username, password)
            cursor.execute(statement)
            for row in cursor:
                cursor.close()
                return True
    cursor.close()
    return False

    
def Find_User(username):
    with dbapi2.connect(dsn) as connection:
        with connection.cursor() as cursor:
            statement = """select * FROM PERSON where person.username = '{}';""".format(username)
            cursor.execute(statement)
            for row in cursor:
                cursor.close()
                print(row)
                return User(str(row[0]),str(row[2]),str(row[3]),str(row[4]),str(row[1]),str(row[5]),row[6])


def Find_Company(company_id):
    with dbapi2.connect(dsn) as connection:
        with connection.cursor() as cursor:
            statement = """select * FROM COMPANY WHERE company.id = {};""".format(company_id)
            cursor.execute(statement)
            for row in cursor:
                cursor.close()
                return Company(str(row[1]),str(row[2]), row[0])
            cursor.close()
            return None

def Find_Products_with_Company(company_id):
    with dbapi2.connect(dsn) as connection:
        with connection.cursor() as cursor:
            statement = """select * FROM PRODUCT WHERE product.company_id = {};""".format(company_id)
            cursor.execute(statement)
            product_list = []
            for row in cursor:
                #print(str(row[1]),str(row[2]),str(row[3]),str(row[4]),row[5],row[6],row[7],str(row[8]),str(row[9]), row[0])
                product_list.append(Product(str(row[1]),str(row[2]),str(row[3]),str(row[4]),row[5],row[6],row[7],str(row[8]),str(row[9]), row[0]))
            cursor.close()
            return product_list

def Find_Product(id):
    with dbapi2.connect(dsn) as connection:
        with connection.cursor() as cursor:
            statement = """select * FROM PRODUCT WHERE product.id = {};""".format(id)
            cursor.execute(statement)
            for row in cursor:
                cursor.close()
                return Product(str(row[1]),str(row[2]),str(row[3]),row[4],row[5],row[6],row[7],str(row[8]),str(row[9]), row[0]) 

def Find_Products():
    with dbapi2.connect(dsn) as connection:
        with connection.cursor() as cursor:
            statement = """select * FROM PRODUCT;"""
            cursor.execute(statement)
            product_list = []
            for row in cursor:
                #print(str(row[1]),str(row[2]),str(row[3]),str(row[4]),row[5],row[6],row[7],str(row[8]),str(row[9]), row[0])
                product_list.append(Product(str(row[1]),str(row[2]),str(row[3]),str(row[4]),row[5],row[6],row[7],str(row[8]),str(row[9]), row[0]))
            cursor.close()
            return product_list
        
def Find_Cart_Products(username):
    with dbapi2.connect(dsn) as connection:
        with connection.cursor() as cursor:
            statement = """select * FROM product as p where exists (select * from cart where cart.username = '{}' and p.id = cart.product_id);""".format(username)
            cursor.execute(statement)
            product_list = []
            for row in cursor:
                #print(str(row[1]),str(row[2]),str(row[3]),str(row[4]),row[5],row[6],row[7],str(row[8]),str(row[9]), row[0])
                product_list.append(Product(str(row[1]),str(row[2]),str(row[3]),str(row[4]),row[5],row[6],row[7],str(row[8]),str(row[9]), row[0]))
            cursor.close()
            return product_list


def Check_In_Cart(username, product_id):
    with dbapi2.connect(dsn) as connection:
        with connection.cursor() as cursor:
            statement = """select * FROM CART WHERE cart.product_id = {} and cart.username = '{}';""".format(product_id, username)
            cursor.execute(statement)
            for row in cursor:
                cursor.close()
                return True
            cursor.close()
            return False

def Delete_From_Cart(username, product_id):
    with dbapi2.connect(dsn) as connection:
        with connection.cursor() as cursor:
            statement = """DELETE FROM CART WHERE cart.product_id = {} and cart.username = '{}';""".format(product_id, username)
            cursor.execute(statement)
            cursor.close()

def Find_Distinct_Models():
    with dbapi2.connect(dsn) as connection:
        with connection.cursor() as cursor:
            statement = """select  distinct Model from  product;"""
            models = []
            cursor.execute(statement)
            for row in cursor:
                models.append(row[0])
            cursor.close()
            return models

def Find_Distinct_Brands():
    with dbapi2.connect(dsn) as connection:
        with connection.cursor() as cursor:
            statement = """select  distinct Brand from  product;"""
            brands = []
            cursor.execute(statement)
            for row in cursor:
                brands.append(row[0])
            cursor.close()
            return brands

def Categorize_Products(category):
    with dbapi2.connect(dsn) as connection:
        with connection.cursor() as cursor:
            statement = """select * FROM product where product.category = '{}';""".format(category)
            cursor.execute(statement)
            product_list = []
            for row in cursor:
                #print(str(row[1]),str(row[2]),str(row[3]),str(row[4]),row[5],row[6],row[7],str(row[8]),str(row[9]), row[0])
                product_list.append(Product(str(row[1]),str(row[2]),str(row[3]),str(row[4]),row[5],row[6],row[7],str(row[8]),str(row[9]), row[0]))
            cursor.close()
            return product_list


def Filter_Products(brands, local=None):
    if(len(brands) <1):
        return None
    with dbapi2.connect(dsn) as connection:
        with connection.cursor() as cursor:
            statement = """select * FROM product where ("""
            for brand in brands:
                statement += "product.brand = '{}' or ".format(brand)
            statement  = statement[:-3]
            statement += ')'
            if(local != None):
                statement += "and (product.location = '{}')".format(local)
            statement += ';'
            print(statement)
            cursor.execute(statement)
            product_list = []
            for row in cursor:
                #print(str(row[1]),str(row[2]),str(row[3]),str(row[4]),row[5],row[6],row[7],str(row[8]),str(row[9]), row[0])
                product_list.append(Product(str(row[1]),str(row[2]),str(row[3]),str(row[4]),row[5],row[6],row[7],str(row[8]),str(row[9]), row[0]))
            cursor.close()
            return product_list

def Find_Local_Products(city):
    with dbapi2.connect(dsn) as connection:
        with connection.cursor() as cursor:
            statement = """select  * from product as p where exists (select * from company where company.id = p.company_id and company.location = '{}');""".format(city)
            cursor.execute(statement)
            product_list = []
            for row in cursor:
                #print(str(row[1]),str(row[2]),str(row[3]),str(row[4]),row[5],row[6],row[7],str(row[8]),str(row[9]), row[0])
                product_list.append(Product(str(row[1]),str(row[2]),str(row[3]),str(row[4]),row[5],row[6],row[7],str(row[8]),str(row[9]), row[0]))
            cursor.close()
            return product_list