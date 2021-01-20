from flask import Flask, render_template, url_for

from database import User
from movie import Movie
import sys, view




def Create_app():
    app = Flask(__name__)
    app.add_url_rule("/",view_func=view.home_page)
    app.add_url_rule("/sign_up", view_func=view.sign_up_page)
    app.add_url_rule("/categorize", methods=['POST'], view_func=view.categorize)
    app.add_url_rule("/per/<string:username>/profile",methods=['GET', 'POST'], view_func=view.person_page)
    app.add_url_rule("/signing", methods=['POST'], view_func=view.signing)
    app.add_url_rule("/logging", methods=['POST'], view_func=view.logging)
    app.add_url_rule("/per/<string:username>/turning", view_func=view.turning_signed)
    app.add_url_rule("/per/<string:username>", methods=['GET'], view_func=view.signed)
    app.add_url_rule("/per/<string:username>/filter", methods=['POST'], view_func=view.filter)
    app.add_url_rule("/per/<string:username>/search", methods=['POST'], view_func=view.searching)
    app.add_url_rule("/per/<string:username>/cart", view_func=view.cart_page)
    app.add_url_rule("/per/<string:username>/<int:product_id>", view_func=view.product_page)
    app.add_url_rule("/per/<string:username>/<int:product_id>/adding", methods=['POST'], view_func=view.AddingtoCart)
    app.add_url_rule("/per/<string:username>/<int:product_id>/deleting", methods=['POST'], view_func=view.deleting_from_cart)
    app.add_url_rule("/per/<string:username>/company", view_func=view.company_page)
    app.add_url_rule("/per/<string:username>/company_creating",methods=['POST'], view_func=view.company_creating)
    app.add_url_rule("/per/<string:username>/adding_product",methods=['POST'], view_func=view.adding_product)
    print('This is standard output', file=sys.stdout)
    
    """db.Add_movie(Movie("troy",year=2004))
    db.Add_movie(Movie("Dark Knight", year=2012))
    db.Add_movie(Movie("The Shawshank Redemption"))
    app.config["db"] = db

    app.config.from_object("settings")"""

    return app


if __name__ == "__main__":
    app = Create_app()
    app.run(host="0.0.0.0", port=8080, debug=True)
