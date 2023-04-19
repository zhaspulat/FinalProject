import os
import json
import dateutil.parser
from datetime import datetime
from flask import Flask, request, abort, jsonify, render_template, url_for, redirect , session
from urllib.parse import urlencode, quote_plus
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_migrate import Migrate
from models import Person,Mission, Movie,Participance, db, setup_db
from auth import AuthError, requires_auth
from authlib.integrations.flask_client import OAuth
from config import COUNT_PER_PAGE


#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

def create_app(app_config=None):
  # create and configure the app
  app = Flask(__name__)
  app.config.from_object(app_config)
  setup_db(app)
  CORS(app)


#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#

  @app.route("/")
  def home():
    return jsonify ({'sucess':True})


#----------------------------------------------------------------------------#
# Routes.GET
#----------------------------------------------------------------------------#

  @app.route('/persons',methods=['GET'])
  @requires_auth ('get:persons')
  def retrieve_persons(jwt):

    person_list = []
    persons_query = Person.query
    current_persons = paginate (persons_query , model_name = 'Person')
    if len (current_persons) == 0 :
                abort (404)
    for person in current_persons:
      # person participances calc and show one line
      tasks = db.session \
                .query(Participance.mission_id,Mission.name) \
                .filter(Participance.person_id == person.id ) \
                .join(Mission) \
                .group_by(Participance.mission_id,Mission.name).all()
      task_list = []
      for task in tasks :
        task_list.append (task [1])
      person_list.append({
                  'id': person.id,
                  'name': person.name,
                  'birth_date':person.birth_date,
                  'gender':person.gender,
                  'participances':task_list
                  })    
    return  jsonify ({'success': True,
                      'persons': person_list, 
                      'total_count': persons_query.count() 
                    })


  @app.route('/movies',methods=['GET'])
  @requires_auth ('get:movies')
  def retrieve_movies(jwt):

    movie_list = []
    movies_query = Movie.query
    current_movies = paginate (movies_query , model_name = 'Movie')
    if len (current_movies) == 0 :
                abort (404)
    for movie in current_movies:
      movie_list.append({
                  'id': movie.id,
                  'name': movie.name,
                  'genre':movie.genre,
                  'release_date':movie.release_date
                  })    
    return  jsonify ({'success': True,
                      'movies': movie_list, 
                      'total_count': movies_query.count() 
                    })
  

  @app.route('/movies/<int:movie_id>',methods=['GET'])
  @requires_auth ('get:movies')
  def show_movie(jwt,movie_id):

    movie= Movie.query.get_or_404(movie_id)
    if movie is None:
                abort (404)
    participance_list=[]
    for participance in movie.participances:
      name = participance.person.name
      mission = participance.mission.name
      participance_list.append ({'name':name,'mission':mission })    
    return  jsonify ({'success': True,
                      'id': movie.id, 
                      'name': movie.name, 
                      'genre':movie.genre,
                      'release_date': movie.release_date,
                      'participances': participance_list})


  @app.route('/participances',methods=['GET'])
  @requires_auth ('get:participances')
  def retrieve_participances(jwt):

    participance_list = []
    participances_query = Participance.query
    current_participances = paginate (participances_query, model_name = 'Participance')
    for participance in current_participances:
      person = Person.query.get_or_404(participance.person_id)
      movie = Movie.query.get_or_404(participance.movie_id)
      mission = Mission.query.get_or_404(participance.mission_id)
      participance_list.append({
                  'person': {
                    'id': person.id,
                    'name': person.name
                  },
                  'movie' : {
                    'id': movie.id,
                    'name': movie.name
                  },
                  'mission': {
                    'id': mission.id,
                    'name': mission.name
                  }
                  })    
    return  jsonify ({'success': True,
                      'participances': participance_list, 
                      'total_count': participances_query.count()
                    })


#----------------------------------------------------------------------------#
# Routes.POST
#----------------------------------------------------------------------------#

  @app.route('/persons',methods=['POST'])
  @requires_auth ('post:persons')
  def new_person(jwt):
    body = request.get_json()
    searchTerm = body.get('searchTerm',None)
    person = body.get ('person',None)

    try:
      if searchTerm: 
        persons = Person.query \
                        .filter \
                          (Person.name.ilike("%{}%".format(searchTerm))).all()
        person_list = [] 
        for person in persons:
          person_list.append ({'name':person.name })
        return jsonify({'persons': person_list,
                        'total_persons':len(persons) 
                      })
    except:
      abort (422)
    try :
      if not searchTerm:
        if person is None:
          abort (422)
        name = person.get('name',None)
        gender = person.get('gender',None)
        birth_date =  person.get('birth_date',datetime.now())
        new_person= Person (name =name ,
                          gender = gender ,
                          birth_date = birth_date)
        new_person.insert()
        return jsonify({'success':True ,'id': new_person.id }) 
    except Exception as e:
        db.session.rollback()
        print(e)
        abort(422)
    

  @app.route('/movies',methods=['POST'])
  @requires_auth ('post:movies')
  def new_movie(jwt):

    body = request.get_json()
    movie = body.get ('movie',None)
    searchTerm = body.get('searchTerm',None)
    try:
      if searchTerm: 
        movies = Movie.query \
                        .filter \
                          (Movie.name.ilike("%{}%".format(searchTerm))).all()
        movie_list = [] 
        for movie in movies:
          movie_list.append ({'name':movie.name })
        return jsonify({'movies': movie_list,
                        'total_movies':len(movies) 
                      })
    except:
      abort (422)
    try :
      if not searchTerm :
        if movie is None:
          abort (422)
        name = movie.get ('name',None) 
        genre = movie.get ('genre',None) 

        if name is None or genre is None :
          abort (422)
        release_date = movie.get ('release_date',datetime.now()) 
        newmovie = Movie (name = name,
                        genre = genre,
                        release_date = release_date
                      )    
        newmovie.insert()
        return jsonify({'success':True ,'id': newmovie.id }) 
    except Exception as e:
      db.session.rollback()
      print(e)
      abort(422)
    

  @app.route('/participances',methods=['POST'])
  @requires_auth ('post:participances')
  def new_participance(jwt):

    body = request.get_json()
    participance = body.get ('participance', None)
    if participance is None:
       abort (422)
    person_id = participance.get ('person_id',None)  
    movie_id = participance.get ('movie_id',None) 
    mission_id = participance.get ('mission_id',None) 
    person = Person.query.get_or_404(person_id)
    movie = Movie.query.get_or_404 (movie_id)
    mission = Mission.query.get_or_404(mission_id)
    if person is None or movie is None or mission is None :
      abort (404)
    try:
      newparticipance= Participance (
                          person_id= person_id,
                          movie_id = movie_id,
                          mission_id = mission_id
                      )
      newparticipance.insert()
    except Exception as e:
      db.session.rollback()
      print(e)
      abort(422)
    return jsonify({'success':True ,'id': newparticipance.id}) 
  

#----------------------------------------------------------------------------#
# Routes.PATCH
#----------------------------------------------------------------------------#


  @app.route('/movies/<int:id>',methods=['PATCH'])
  @requires_auth ('update:movies')
  def patch_movie (jwt,id):

    body = request.get_json()
    data = body.get ('movie',None)
    movie = Movie.query.filter(Movie.id == id).one_or_none()
    if movie is None :
      abort (404)
    try:
      movie.release_date = data.get('release_date',movie.release_date)
      movie.update()
      return jsonify({'success':True})   
    except Exception as e:
      print(e)
      db.session.rollback()
      abort(422)


  @app.route('/persons/<int:id>',methods=['PATCH'])
  @requires_auth ('update:persons')
  def patch_person (jwt,id):

    body = request.get_json()
    data = body.get ('person',None)
    person = Person.query.filter(Person.id == id).one_or_none()
    if person is None :
      abort (404)
    try: 
      person.birth_date = data.get('birth_date',person.birth_date)
      person.update()
      return jsonify({'success':True})   
    except Exception as e:
      print(e)
      db.session.rollback()
      abort(422)


#----------------------------------------------------------------------------#
# Routes.DELETE
#----------------------------------------------------------------------------#


  @app.route('/persons/<int:id>',methods=['DELETE'])
  @requires_auth ('delete:persons')
  def delete_person(jwt,id):

    person = Person.query.get_or_404 (id)
    if person is None:
      abort (404)
    try:
      person.delete()
    except Exception as e:
      db.session.rollback()
      print(e)
      abort(422)
    return jsonify({'success':True, 'id':id}) 


  @app.route('/movies/<int:id>',methods=['DELETE'])
  @requires_auth ('delete:movies')
  def delete_movie(jwt,id):

    movie = Movie.query.get_or_404 (id)
    if movie is None:
      abort (404)
    try:
      movie.delete()
    except Exception as e:
      db.session.rollback()
      print(e)
      abort(422)
    return jsonify({'success':True, 'id':id}) 


#----------------------------------------------------------------------------#
# .Error Handling
#----------------------------------------------------------------------------#


  @app.errorhandler(401)
  def unauthorized(error):
      return jsonify({
          "success": False,
          "error": 401,
          "message": error.description
      }), 401

  @app.errorhandler(403)
  def unauthorized_permission(error):
      return jsonify({
          "success": False,
          "error": 403,
          "message": error.description
      }), 403
  
  @app.errorhandler(422)
  def unprocessable(error):
      return jsonify({
          "success": False,
          "error": 422,
          "message": "unprocessable"
      }), 422

  @app.errorhandler(404)
  def unprocessable(error):
      return jsonify({
          "success": False, 
          "error": 404, 
          "message": "not found"
      }), 404

  @app.errorhandler(400)
  def bad_request(error):
      return jsonify({
          "success": False,
          "error": 400, 
          "message": "bad request"
      }), 400
      
  @app.errorhandler(500)
  def bad_request(error):
      return jsonify({
          "success": False, 
          "error": 500, 
          "message": "internal server error"
      }), 500

  return app

app = create_app('config')
migrate= Migrate(app, db)

def paginate (query , model_name = None ):
    page = request.args.get('page', 1, type=int)
    current_index = page - 1
    if model_name is not None :
      if model_name == 'Movie':
        temp_list = query.order_by(Movie.id).limit(COUNT_PER_PAGE).offset(current_index * COUNT_PER_PAGE).all()
        return temp_list 
      if model_name == 'Person':
        temp_list = query.order_by(Person.id).limit(COUNT_PER_PAGE).offset(current_index * COUNT_PER_PAGE).all()
        return temp_list 
      if model_name == 'Participance':
        temp_list = query.order_by(Participance.id).limit(COUNT_PER_PAGE).offset(current_index * COUNT_PER_PAGE).all()
        return temp_list 
      else :
        return None
  

#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)