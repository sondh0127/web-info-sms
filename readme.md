# Development setup

- I use docker for create mysql server. So, please install docker-compose for the setting up env.
- https://docs.docker.com/compose/install/
- We also need to stop mysql-services on local system to free 3306 port.

## Install library requirement

`pip install -r requirements.txt`

## Create and connect to mysql-server

`docker-compose up`

- Note: The seed database also provided in docker container.

# Account for login:

- For tutor:

```
test1@gmail.com/1secret
test2@gmail.com/2secret
...
test6@gmail.com/6secret
```

- For student:

```
student1@gmail.com/1secret
student2@gmail.com/2secret
student3@gmail.com/3secret
```

## Run app

`python app.py`

## User API end-point

```
<!-- Login for all user -->
api.add_resource(UserLogin, '/login')

<!-- Tutor resgister -->
api.add_resource(TutorRegistration, '/register/tutor')

<!-- Class CRUD function (for tutor only) -->
api.add_resource(Class, '/class/<string:name>')

<!-- Class list of tutor, or all active class for student -->
api.add_resource(ClassList, '/classes')

<!-- Remove student from class (for tutor only) -->
api.add_resource(RemoveStudent, '/class/<string:name>/<int:student_id>')

<!-- Student register -->
api.add_resource(StudentRegistration, '/register')

<!-- Classes enrollment (for student) -->
api.add_resource(Enroll, '/enroll/<string:name>')
api.add_resource(StudentEnroll, '/enrolls')
```
