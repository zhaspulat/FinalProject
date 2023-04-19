
import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from app import create_app
from models import Person,Movie,Mission
from test_config import PRODUCER_TOKEN ,ASSISTANT_TOKEN

class AgencyTestCase(unittest.TestCase):
    """This class represents the agency test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app('test_config')
        self.client = self.app.test_client
        self.producer_token = {'Authorization': PRODUCER_TOKEN }
        self.assistant_token = {'Authorization': ASSISTANT_TOKEN }


        self.new_person= {"person":{"name":"Katee Sackhoff",
                            "birth_date":"08-05-1980",
                            "gender":"Female"}}
             
        self.new_movie= {"movie":{"name":"Titanic",
                                   "genre":["Romance","Drama"],
                                   "release_date":"02.20.1998"}}

        self.delete_person= Person(name= 'Leonardo DiCaprio',
                                    gender= 'Male',
                                    birth_date = '06.20.1975')
        
        self.delete_person2= Person(name= 'Pedro Pascal',
                                    gender= 'Male',
                                    birth_date = '05-02-1975')
        
        self.delete_movie= Movie (name= 'The Godfather',
                                  genre=['Crime','Drama'],
                                  release_date= '10.21.1973')
        
        self.delete_movie2= Movie (name= 'The Mandalorian',
                                  genre= ['Action','Fantasy','Adventure'],
                                  release_date= '10.25.2019')

        self.delete_mission = Mission (name ='Director')
        self.delete_mission2 = Mission (name ='Writer')
        self.delete_mission3 = Mission (name ='Star')

    def tearDown(self):
        """Executed after reach test"""    
        pass

    #PERSON POST 
    def test_person_success_insert (self):
        res = self.client().post("/persons", headers=self.producer_token, json= self.new_person )
        data = json.loads(res.data)       
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue( data['id'] )

    def test_person_insert_403_autorization_unable_to_authorize (self):
        res = self.client().post("/persons", headers=self.assistant_token, json= self.new_person )
        data = json.loads(res.data)       
        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['success'], False)
    
    def test_person_insert_fail (self):
        res = self.client().post("/persons",headers=self.producer_token, json= { 'person':'' } )
        data = json.loads(res.data)       
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unprocessable')

    #PERSON GET
    def test_get_persons (self):
        with self.app.app_context():
            Person.insert(self.delete_person2)
        res = self.client().get("/persons", headers=self.producer_token)
        data = json.loads(res.data)       
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_404_beyond_valid_page (self):
        res = self.client().get("/persons?page=100000", headers=self.producer_token)
        data = json.loads(res.data)    
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'not found')

    #MOVIE POST 
    def test_movie_success_insert (self):
        res = self.client().post("/movies", headers=self.producer_token, json= self.new_movie )
        data = json.loads(res.data)       
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue( data['id'] )
        self.movie_id = data['id']
    
    def test_movie_insert_fail (self):
        res = self.client().post("/movies",headers=self.producer_token, json= { 'movie':'' } )
        data = json.loads(res.data)       
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unprocessable')

    def test_movie_insert_403_autorization_unable_to_authorize (self):
        res = self.client().post("/movies", headers=self.assistant_token, json= self.new_movie )
        data = json.loads(res.data)       
        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['success'], False)

    #MOVIE GET
    def test_get_movies (self):
        with self.app.app_context():
            Movie.insert(self.delete_movie2)  
        res = self.client().get("/movies", headers=self.producer_token) 
        data = json.loads(res.data)       
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_get_movies_with_assistant_role (self):
        with self.app.app_context():
            Movie.insert(self.delete_movie2)  
        res = self.client().get("/movies", headers=self.assistant_token) 
        data = json.loads(res.data)       
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_404_beyond_valid_movie_page (self):
        res = self.client().get("/movies?page=100000", headers=self.producer_token)
        data = json.loads(res.data)    
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'not found')
        
    def test_get_movie_with_id (self):
        with self.app.app_context():
            Movie.insert(self.delete_movie2)  
            movie_id = self.delete_movie2.id
        res = self.client().get(f"/movies/{movie_id}", headers=self.producer_token) 
        data = json.loads(res.data)       
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
    
    def test_404_movie_with_nonexist_id (self):
        res = self.client().get(f"/movies/999999999999", headers=self.producer_token) 
        data = json.loads(res.data)       
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'not found')
    
    #PERSON SEARCH
    def test_person_success_searching_with_result (self):
        with self.app.app_context():
            Person.insert(self.delete_person)
        res = self.client().post("/persons", headers=self.producer_token, json= {'searchTerm' : 'hOFf'})
        data = json.loads(res.data)   
        self.assertEqual(res.status_code, 200)
        self.assertTrue( data['total_persons'] )     

    def test_person_success_searching_without_result (self):
        res = self.client().post("/persons", headers=self.producer_token, json= {'searchTerm' : 'asdsdsdasa'})
        data = json.loads(res.data)   
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['total_persons'] ,0)

    #MOVIE SEARCH
    def test_movie_success_searching_with_result (self):
        res = self.client().post("/movies", headers=self.producer_token, json= {'searchTerm' : 'Ani'})
        data = json.loads(res.data)   
        self.assertEqual(res.status_code, 200)
        self.assertTrue( data['total_movies'])

    def test_movie_success_searching_without_result (self):
        res = self.client().post("/movies", headers=self.producer_token, json= {'searchTerm' : 'asdsdsdasa'})
        data = json.loads(res.data)   
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['total_movies'] ,0)

    #PERSON delete
    def test_delete_person (self):
        with self.app.app_context():
            Person.insert(self.delete_person)
            id=self.delete_person.id
        res = self.client().delete(f"/persons/{id}", headers=self.producer_token)
        data = json.loads(res.data)   
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True) 
        self.assertTrue(data['id'])

    def test_delete_person_403_authorization_fail(self):
        with self.app.app_context():
            Person.insert(self.delete_person)
            id=self.delete_person.id
        res = self.client().delete(f"/persons/{id}", headers=self.assistant_token)
        data = json.loads(res.data)   
        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['success'], False) 

    def test_404_delete_question (self):
        res = self.client().delete("/persons/99999", headers=self.producer_token)
        data = json.loads(res.data)   
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False) 
        self.assertEqual(data['message'],'not found')

    #MOVIE delete
    def test_delete_movie (self):
        with self.app.app_context():
            Movie.insert(self.delete_movie)
            id=self.delete_movie.id
        res = self.client().delete(f"/movies/{id}", headers=self.producer_token)
        data = json.loads(res.data)   
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True) 
        self.assertTrue(data['id'])

    def test_404_delete_question (self):
        res = self.client().delete("/movies/99999", headers=self.producer_token)
        data = json.loads(res.data)   
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False) 
        self.assertEqual(data['message'],'not found')

    def test_participance_success_insert (self):
        with self.app.app_context():
            Mission.insert (self.delete_mission)
            Person.insert(self.delete_person)
            Movie.insert(self.delete_movie)
            json_data = {"participance":{"person_id":self.delete_person.id,"movie_id":self.delete_movie.id,"mission_id":self.delete_mission.id}}

        res = self.client().post("/participances", headers=self.producer_token, json= json_data)
        data = json.loads(res.data)       
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue( data['id'] )
        self.movie_id = data['id']
    
    def test_participance_insert_fail (self):
        res = self.client().post("/participances",headers=self.producer_token, json= { 'particip':'' } )
        data = json.loads(res.data)       
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unprocessable')

if __name__ == "__main__":
    unittest.main()