from flask import Flask, render_template, current_app, request, redirect, url_for
import sys
from database import User, Product, Company, Product, Cart
from database import Check_User, Find_User, Find_Company, Find_Product, Find_Products_with_Company
from database import Find_Products, Find_Cart_Products, Check_In_Cart, Delete_From_Cart
from database import Find_Distinct_Brands, Find_Distinct_Models, Categorize_Products, Filter_Products
from database import Find_Local_Products

curr_user = []
products = []

def home_page():
    global products, curr_user
    today = "wednesday"
    curr_user.clear()
    return render_template("home.html", day=today)

def logging():
    username = request.form['Username']
    password = request.form['Password']
    global products
    if(Check_User(username, password)):
        curr_user.append(Find_User(username))
        products = Find_Products()
        return redirect(url_for('.signed', username=username))
    else:
        return redirect(url_for('home_page'))

def signing():
    user = User(request.form['username'], request.form['fname'],request.form['lname'],request.form['email'],request.form['password'],request.form['address'])
    user.AddtoDatabase()
    curr_user.append(user)
    global products
    products = Find_Products()
    
    return redirect(url_for('.signed', username=user.username)) #(render_template("signed.html", usern))

def turning_signed(username):
    if(len(curr_user) != 1 or username!=curr_user[0].username):
        return redirect(url_for('home_page'))
    global products
    products = Find_Products()
    return redirect(url_for('.signed', username=username)) #(render_template("signed.html", usern))

def signed(username):
    
    if(len(curr_user) == 1 and username==curr_user[0].username):
        brands = Find_Distinct_Brands()
        models = Find_Distinct_Models()
        return (render_template("signed.html", username=username, name=username, product_list=products, brands=brands, models=models))
    else:
        return redirect(url_for('home_page'))
def sign_up_page():
    return render_template("sign_up.html")


def product_page(username, product_id):
    if(len(curr_user) != 1 or username!=curr_user[0].username):
        return redirect(url_for('home_page'))
    
    product = Find_Product(product_id)
    in_cart = Check_In_Cart(username, product_id)
    return render_template("product.html",username=username, product_id=product.id, product=product, in_cart=in_cart)



def person_page(username):
    if(len(curr_user) != 1 or username!=curr_user[0].username):
        return redirect(url_for('home_page'))
    print(curr_user[0].location)
    return render_template("person.html", username=username, user=curr_user[0])



def company_page(username):
    if(len(curr_user) != 1 or username!=curr_user[0].username):
        return redirect(url_for('home_page'))
    company = None
    global products
    products.clear()
    if(curr_user[0].company_id != None):
        company = Find_Company(curr_user[0].company_id)
        products = Find_Products_with_Company(company.id)

    return render_template("company.html", username=username, user=curr_user[0], company=company, product_list=products)

def cart_page(username):
    if(len(curr_user) != 1 or username!=curr_user[0].username):
        return redirect(url_for('home_page'))
    
    global products
    products.clear()
    products = Find_Cart_Products(username)

    return render_template("cart.html", username=username, user=curr_user[0], product_list=products)

def company_creating(username):
    if(len(curr_user) != 1 or username!=curr_user[0].username):
        return redirect(url_for('home_page'))

    company = Company(request.form['company'],request.form['location'])
    curr_user[0].Set_Company_ID(str(company.AddtoDatabase()))

    return redirect(url_for('.company_page', username=username))



def adding_product(username):
    if(len(curr_user) != 1 or username!=curr_user[0].username):
        return redirect(url_for('home_page'))

    
    product = Product(request.form['pname'],"asd",request.form['brand'],request.form['model'],0,request.form['quantity'],request.form['price'],curr_user[0].company_id,request.form['category'])

    product.AddtoDatabase()

    return redirect(url_for('.company_page', username=username))

def AddingtoCart(username, product_id):
    if(len(curr_user) != 1 or username!=curr_user[0].username):
        return redirect(url_for('home_page'))
    cart = Cart(username, product_id)
    cart.AddtoDatabase()

    return redirect(url_for('.turning_signed', username=username))

def deleting_from_cart(username, product_id):
    if(len(curr_user) != 1 or username!=curr_user[0].username):
        return redirect(url_for('home_page'))
    
    Delete_From_Cart(username,product_id)

    return redirect(url_for('.turning_signed', username=username))

def categorize(company=None,cart=None):
    global products
    category = request.form['category']
    
    products = Categorize_Products(category)

    if(company != None):
        redirect(url_for('.company_page', username=curr_user[0].username))
    
    if(cart != None):
        redirect(url_for('.cart_page', username=curr_user[0].username))

    if(len(curr_user) < 1):
        return redirect(url_for('.home_page'))

    return redirect(url_for('.signed', username=curr_user[0].username))

def filter(username):
    if(len(curr_user) < 1):
        return redirect(url_for('.home_page'))
    allbrands = Find_Distinct_Brands()
    brands = []
    for brand in allbrands:
        temp = request.form.get(brand, None)
        if(temp != None):
            brands.append(temp)
    
    global products
    products = Filter_Products(brands)

    local = request.form.get('local', None)
    if(local != None):
        products.clear()
        products = Find_Local_Products(curr_user[0].location)
        print(len(products))

    return redirect(url_for('.signed', username=curr_user[0].username))



def searching(username):
    if(len(curr_user) < 1):
        return redirect(url_for('.home_page'))

    search = request.form['search']
    print("search")
    return redirect(url_for('.signed', username=curr_user[0].username))

