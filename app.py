# app.py

from flask import Flask, request, jsonify
from flask_restx import Api, Resource
from flask_sqlalchemy import SQLAlchemy
# from model import Movie, Director, Genre, movie_schema, movies_schema, movielist_schema
from marshmallow import Schema, fields
from sqlalchemy import and_

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['RESTX_JSON'] = {'ensure_ascii': False, 'indent': 2}
app.config['strict_slashes']=False


db = SQLAlchemy(app)

api = Api(app)
movies_ns = api.namespace('movies')
directors_ns = api.namespace('directors')


class Movie(db.Model):
    __tablename__ = 'movie'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    description = db.Column(db.String(255))
    trailer = db.Column(db.String(255))
    year = db.Column(db.Integer)
    rating = db.Column(db.Float)
    genre_id = db.Column(db.Integer, db.ForeignKey("genre.id"))
    genre = db.relationship("Genre")
    director_id = db.Column(db.Integer, db.ForeignKey("director.id"))
    director = db.relationship("Director")

class MovieSchema(Schema):

    id = fields.Int()
    title = fields.Str()
    description = fields.Str()
    trailer = fields.Str()
    year = fields.Int()
    rating = fields.Float()
    genre_id = fields.Int()
    director_id = fields.Int()

class MovieListSchema(Schema):

    title = fields.Str()

movie_schema = MovieSchema()
movielist_schema = MovieListSchema(many=True)
movies_schema = MovieSchema(many=True)


class Director(db.Model):
    __tablename__ = 'director'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))


class Genre(db.Model):
    __tablename__ = 'genre'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))


@movies_ns.route('/<int:id>')
class MovieView(Resource):

    def get(self, id: int):
        try:
            movie = movie_schema.dump(Movie.query.get(id))
            if not movie:
                return f"Фильм с id {id} не найден", 404
            return movie, 200
        except Exception as e:
            return {str(e)}, 404

@movies_ns.route('/')
class MoviesView(Resource):

    def get(self):
        args = request.args

        # получаем фильмы:
        movies = movielist_schema.dump(Movie.query.all())
        # Если есть пагинация:
        if 'page' in args:
            # Устанавливаем количество на страницу
            items_per_page = 5
            movies = movielist_schema.dump(Movie.query.offset(int(args['page']) * items_per_page).limit(items_per_page))
        # если пагинации нет, проверяем фильтры на режиссера
        else:
            if 'director_id' in args:
                movies = movies_schema.dump(Movie.query.filter(Movie.director_id == args['director_id']).all())
            if 'genre_id' in args:
                movies = movies_schema.dump(Movie.query.filter(Movie.genre_id == args['genre_id']).all())
            if 'director_id' in args and 'genre_id' in args:
                print('both filters', int(args['director_id']), int(args['genre_id']))
                movies = movies_schema.dump(Movie.query.filter(and_(Movie.director_id == int(args['director_id']), Movie.genre_id == int(args['genre_id']))).all())
        return movies, 200

@directors_ns.route('/')
class DirectorView(Resource):

    def post(self):
        data = request.json
        director = Director(**data)
        print("!!!", director)
        db.session.add(director)
        db.session.commit()
        return "Добавлен новый режиссер", 201

@directors_ns.route('/<int:id>')
class DirectorView(Resource):

    def put(self, id:int):
        director = Director.query.get(id)
        data = request.json
        print(data)
        director.name = data['name']
        db.session.add(director)
        db.session.commit()
        return f"Теперь режиссера зовут {director.name}", 204

    def delete(self, id:int):
        director = Director.query.get(id)
        db.session.delete(director)
        db.session.commit()
        return f"Прощаемся с режиссером {director.name}", 204

if __name__ == '__main__':
    app.run(debug=True)
