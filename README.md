# Nomadic

**Udacity Full Stack Developer Nano-degree Program Capstone Project**

## Application URL:

https://nomadic-udacity.herokuapp.com/

## Existing Roles

There are 2 Roles with distinct permissions:
1. Client
   - get:artists: Can view a list of all artists
   - get:projects: Can view a list of all projects' names
   - post:clients: Can create a new client
   - post:project: Can create a new project
   - patch:project: Can edit an existing project
   - delete:project: Can delete an existing project
2. Artist
   - get:artists: Can view a list of all artists
   - get:projects: Can view a list of all projects' names
   - post:artists: Can create a new artist

Access Token for both roles are included in the `cofig.py` file.