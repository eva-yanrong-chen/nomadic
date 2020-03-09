import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

from models import setup_db, Client, Artist, Project
from auth import AuthError, requires_auth


app = Flask(__name__)
setup_db(app)
CORS(app)

'''
@TODO GET '/projects'
    - require permission 'get:projects'
    - return status code 200 and json {'success': True, 'projects': projects}
        projects: a list of open projects' names
'''


'''
@TODO GET '/artists'
    - require permission 'get:artists'
    - return status code 200 and json {'success': true, 'artists': artists}
        artists: a paginated list of artists
'''


'''
@TODO GET '/projects/<int:id>'
    - require permission 'get:projects'
    - return status code 200 and json {'success': true, 'project': project}
        project: the project with id requested
    - return status code 404 if <id> is not found
'''


'''
@TODO POST '/projects/'
    - require permission 'post:projects'
    - return status code 200 and json {'success': true, 'project': project}
        project: the project created
    - return status code 422 if request is unprocessable
'''


'''
@TODO POST '/artists/'
    - require permission 'post:artists'
    - return status code 200 and json {'success': true, 'artists': artists}
        artists: a paginated list of artists
    - return status code 422 if request is unprocessable
'''


'''
@TODO PATCH '/projects/<int:id>'
    - require permission 'patch:projects'
    - return status code 200 and json {'success': true, 'project': project}
        project: the project created
    - return status code 404 if <id> is not found
    - return status code 422 if request is unprocessable
'''


'''
@TODO DELETE '/projects/<int:id>'
    - require permission 'delete:projects'
    - return status code 200 and json {'success': true, 'deleted': name}
'''


# Default port:
if __name__ == '__main__':
    app.run()

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''

# Error Handling
'''
Example error handling for unprocessable entity
'''
@app.errorhandler(422)
def unprocessable(error):
    return jsonify({
        "success": False,
        "error": 422,
        "message": "unprocessable"
    }), 422


'''
Implement error handler for 404
    error handler should conform to general task above
'''
@app.errorhandler(404)
def unprocessable(error):
    return jsonify({
        "success": False,
        "error": 404,
        "message": "resource not found"
    }), 404


'''
Implement error handler for AuthError
    error handler should conform to general task above
'''
@app.errorhandler(AuthError)
def autherror(error):
    return jsonify({
        "success": False,
        "code": error.status_code,
        "error": error.error["code"],
        "description": error.error["description"]
    }), error.status_code
