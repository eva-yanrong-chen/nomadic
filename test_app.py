import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from app import app
from models import setup_db, Artist, Client, Project, db_drop_and_creat_all
from config import artist_token, client_token


# Creating request headers with 'Authorization' key and access token as value
artist_auth_header = {
    'Authorization': artist_token
}

client_auth_header = {
    'Authorization': client_token
}


class TestCase(unittest.TestCase):

    def setUp(self):
        """Set up of the test"""
        self.app = app
        self.client = self.app.test_client
        self.database_name = "nomadic"
        self.database_path = "postgres://{}/{}".format(
            'localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)
        db_drop_and_creat_all()

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

    def tearDown(self):
        """Executed after reach test"""
        pass

# ----------------------------------------------------------------------------#
# Tests for GET /projects
# ----------------------------------------------------------------------------#
    def test_get_project_names_unauthorized(self):
        res = self.client().get('/projects')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertFalse(data['success'])

    def test_get_project_names_artists(self):
        res = self.client().get('/projects', headers=artist_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertGreater(len(data['projects']), 0)

# ----------------------------------------------------------------------------#
# Tests for GET /artists
# ----------------------------------------------------------------------------#
    def test_get_all_artists_unauthorized(self):
        res = self.client().get('/artists')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertFalse(data['success'])

    def test_get_all_artists_artists(self):
        res = self.client().get('/artists', headers=artist_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertGreater(len(data['artists']), 0)


# ----------------------------------------------------------------------------#
# Tests for GET /project/<int:id>
# ----------------------------------------------------------------------------#
    def test_get_project_detail_404(self):
        res = self.client().get('/projects/10', headers=artist_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])

    def test_get_project_detail(self):
        res = self.client().get('/projects/1', headers=artist_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(data['project'].get('id'), 1)

# ----------------------------------------------------------------------------#
# Tests for POST /clients
# ----------------------------------------------------------------------------#
    def test_create_new_client(self):
        client = {
            'name': 'Nomadic',
            'description': 'A platfor that connects artists and art projects'
        }

        res = self.client().post('/clients', json=client,
                                 headers=client_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(data['client'], 'Nomadic')

    def test_create_new_client_no_json(self):
        res = self.client().post('/clients', headers=client_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertFalse(data['success'])

    def test_create_new_client_by_artist(self):
        client = {
            'name': 'Udacity',
            'description': 'An online learning platform'
        }

        res = self.client().post('/clients', json=client,
                                 headers=artist_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertFalse(data['success'])

# ----------------------------------------------------------------------------#
# Tests for POST /projects
# ----------------------------------------------------------------------------#
    def test_create_new_project(self):

        project = {
            'name': 'Fyyur office wall painting',
            'client_id': 1,
            'description': 'Paint a large wall in the Fyyur office'
        }
        res = self.client().post('/projects', json=project,
                                 headers=client_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(data['project'].get('name'),
                         'Fyyur office wall painting')

    def test_create_new_project_no_json(self):
        res = self.client().post('/projects', headers=client_auth_header)
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 422)
        self.assertFalse(data['success'])

    def test_create_new_project_unauthorized(self):
        project = {
            'name': 'Fyyur office wall painting',
            'client_id': 1,
            'description': 'Paint a large wall in the Fyyur office'
        }
        res = self.client().post('/projects', json=project,
                                 headers=artist_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertFalse(data['success'])

# ----------------------------------------------------------------------------#
# Tests for POST /artists
# ----------------------------------------------------------------------------#
    def test_create_new_artist(self):

        artist = {
            'name': 'Veneer',
            'portfolio_link': 'http://dribble.com'
        }
        res = self.client().post('/artists', json=artist,
                                 headers=artist_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(data['artist'].get('name'),
                         'Veneer')

    def test_create_new_artist_no_json(self):
        res = self.client().post('/artists', headers=artist_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertFalse(data['success'])

    def test_create_new_artist_no_portfolio(self):
        artist = {
            'name': 'Vaneer'
        }
        res = self.client().post('/artists', json=artist,
                                 headers=artist_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertFalse(data['success'])

# ----------------------------------------------------------------------------#
# Tests for PATCH /project/<int:id>
# ----------------------------------------------------------------------------#
    def test_edit_project_detail_404(self):
        project_edit = {
            'name': 'Fyuur webpage background'
        }
        res = self.client().patch('/projects/10', json=project_edit,
                                  headers=client_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])

    def test_edit_project_deatil(self):
        res = self.client().get('/projects/1', headers=client_auth_header)
        data = json.loads(res.data)

        self.assertEqual(data['project'].get('name'),
                         'Fyyur website background')

        project_edit = {
            'name': 'Fyyur webpage background'
        }
        
        res = self.client().patch('/projects/1', json=project_edit,
                                  headers=client_auth_header)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(data['project'].get('name'),
                         'Fyyur webpage background')

# ----------------------------------------------------------------------------#
# Tests for PATCH /project/<int:id>
# ----------------------------------------------------------------------------#
    def test_delete_project_unauthorized(self):
        res = self.client().delete('/projects/1', headers=artist_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertFalse(data['success'])

    def test_delete_project(self):
        res = self.client().delete('/projects/1', headers=client_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(data['project'], 'Fyyur website background')

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
