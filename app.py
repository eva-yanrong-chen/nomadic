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
GET '/projects'
    - require permission 'get:projects'
    - return status code 200 and json {'success': True, 'projects': projects}
        projects: a list of open projects' names
'''
@app.route('/projects')
@requires_auth(permission='get:projects')
def get_projects(jwt):
    projects = Project.query.all()
    projects = [p.name for p in projects]
    return jsonify({'success': True, 'projects': projects})


'''
GET '/artists'
    - require permission 'get:artists'
    - return status code 200 and json {'success': true, 'artists': artists}
        artists: a paginated list of artists
'''
@app.route('/artists')
@requires_auth(permission='get:artists')
def get_artists(jwt):
    artists = Artist.query.all()
    artists = [a.name for a in artists]
    return jsonify({'success': True, 'artists': artists})


'''
GET '/projects/<int:id>'
    - require permission 'get:projects'
    - return status code 200 and json {'success': true, 'project': project}
        project: the project with id requested
    - return status code 404 if <id> is not found
'''
@app.route('/projects/<int:id>')
@requires_auth(permission='get:projects')
def get_project_detail(jwt, id):
    project = Project.query.filter_by(id=id).one_or_none()
    if (project is None):
        abort(404)
    return jsonify({'success': True, 'project': project.format()})


'''
POST '/clients'
    - require permission 'post:clients'
    - return status code 200 and json {'success': true, 'client': client_id}
        client: the client created
    - return status code 422 if request is unprocessable
'''
@app.route('/clients', methods=['POST'])
@requires_auth(permission='post:clients')
def post_client(jwt):
    body = request.get_json()
    if (body is None):
        abort(422)
    name = body.get('name')
    description = body.get('description')
    if (name is None or description is None):
        abort(422)

    client = Client(name=name, description=description)

    try:
        client.insert()
    except Exception as e:
        abort(422)
    client = Client.query.filter_by(name=name).one()
    return jsonify({'success': True, 'client': client.name})


'''
POST '/projects/'
    - require permission 'post:projects'
    - return status code 200 and json {'success': true, 'project': project}
        project: the project created
    - return status code 422 if request is unprocessable
'''
@app.route('/projects', methods=['POST'])
@requires_auth(permission='post:projects')
def post_project(jwt):
    body = request.get_json()
    if (body is None):
        abort(422)
    name = body.get('name')
    client_id = body.get('client_id')
    description = body.get('description')
    if (name is None or client_id is None or description is None):
        abort(422)
    project = Project(name=name, client_id=client_id, description=description)

    try:
        project.insert()
    except Exception:
        abort(422)
    return jsonify({'success': True, 'project': project.format()})


'''
POST '/artists/'
    - require permission 'post:artists'
    - return status code 200 and json {'success': true, 'artist': artist}
        artists: the artists just added
    - return status code 422 if request is unprocessable
'''
@app.route('/artists', methods=['POST'])
@requires_auth(permission='post:artists')
def post_artists(jwt):
    body = request.get_json()
    if (body is None):
        abort(422)
    name = body.get('name')
    portfolio_link = body.get('portfolio_link')
    if (name is None or portfolio_link is None):
        abort(422)
    artist = Artist(name=name, portfolio_link=portfolio_link)
    
    try:
        artist.insert()
    except Exception:
        abort(422)
    return jsonify({'success': True, 'artist': artist.format()})


'''
PATCH '/projects/<int:id>'
    - require permission 'patch:projects'
    - return status code 200 and json {'success': true, 'project': project}
        project: the project created
    - return status code 404 if <id> is not found
    - return status code 422 if request is unprocessable
'''
@app.route('/projects/<int:id>', methods=['PATCH'])
@requires_auth(permission='patch:projects')
def patch_project(jwt, id):
    project = Project.query.filter_by(id=id).one_or_none()
    if (project is None):
        abort(404)
    body = request.get_json()
    if (body is None):
        abort(422)
    name = body.get('name')
    client_id = body.get('client_id')
    description = body.get('description')
    if (name is not None):
        project.name = name
    if (client_id is not None):
        project.client_id = client_id
    if (description is not None):
        project.description = description
    try:
        project.update()
    except Exception as e:
        abort(422)
    return jsonify({'success': True, 'project': project.format()})


'''
DELETE '/projects/<int:id>'
    - require permission 'delete:projects'
    - return status code 200 and json {'success': true, 'deleted': name}
'''
@app.route('/projects/<int:id>', methods=['DELETE'])
@requires_auth(permission='delete:projects')
def delete_project(jwt, id):
    project = Project.query.filter_by(id=id).one_or_none()
    if (project is None):
        abort(404)
    name = project.name
    project.delete()
    return jsonify({'success': True, 'project': name})


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
