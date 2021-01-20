from movie import Movie
import sqlalchemy as sql
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import sessionmaker
#from flask_sqlalchemy import SQLAlchemy


engine = create_engine('sqlite:///database.db',echo=True)
Base = declarative_base()


class User(Base):
    __tablename__='user_table'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    surname = Column(String)
    username = Column(String)

    def __repr__(self):
        return "<User(name='%s', surname='%s', username='%s')>" % (self.name, self.surname, self.username)


def main():
    Base.metadata.create_all(engine)
    user1 = User(name='Berkay', surname='Bayraktar', username='Beft9') 
    user2 = User(name='Berat', surname='Bayraktar', username='b0rto') 
    user3 = User(name='Emirhan', surname='Bayraktar', username='emirtheking') 
    user4 = User(name='Cavit', surname='Bayraktar', username='AvCavit') 
    user5 = User(name='Nihal', surname='Bayraktar', username='nihal')
    user6 = User(name='Feyza', surname='Bayraktar', username='DidemFeyza')
    Session = sessionmaker()
    Session.configure(bind=engine)
    session = Session()
    session.add(user1)
    session.add(user2)
    session.add(user3)
    session.add(user4)
    session.add(user5)
    session.add(user6)
    session.commit()
    our_user = session.query(User).filter_by(surname='Bayraktar')
    for user in our_user:
        print(user)

if __name__ == "__main__":
    
    main()











class Database:
    def __init__(self):
        self.movies = {}
        self.last_movie_key = 0

    def Add_movie(self, movie):
        self.last_movie_key += 1
        self.movies[self.last_movie_key] = movie
        
        return self.last_movie_key

    def Delete_movie(self, movie_key):
        if movie_key in self.movies:
            del self.movies[movie_key]


    def Get_movie(self, movie_key):
        movie = self.movies.get(movie_key)
        if movie is None:
            return None
        movie_ = Movie(movie.title, year=movie.year)
        return movie_ 

    def Get_movies(self):
        movies = []

        for movie_key, movie in self.movies.items():
            movie = Movie(movie.title, movie.year)
            movies.append((movie_key, movie))

        return movies 
