For this challenge I've used Python 3.6.5
For the external libraries I've used flask and uuid

To run the server just navigate to your local repository and in the command line do "python app.py". 
The app will run on http://127.0.0.1:5000

I've added a postman collection to the repository - Novastone.postman_collection.json

From the requirements, I've created the following endpoints:

- LOGIN - 
http://127.0.0.1:5000/login/
    Accepts POST method and json structure like:
      {
       "username": "user1",
       "password": "password1"
      }

- ADD TASK -
http://127.0.0.1:5000/user1/todo/add
    Accepts POST method and json structure like:
      {"message": "test message 1"}  

- RETRIEVE TODO LIST -
http://127.0.0.1:5000/user1/todo/
    Accepts GET method

- COMPLETE TASK -
http://127.0.0.1:5000/user1/todo/complete/1
    Accepts GET method

- DELETE TASK -
http://127.0.0.1:5000/user1/todo/delete/1
    Accepts GET method

- LOGOUT -
http://127.0.0.1:5000/logout
    Accepts GET method

## Observations

The app testing is done in the tests.py file. 
For easier testing and tracking all the endpoints apart from login and logout are tested in the same test method
