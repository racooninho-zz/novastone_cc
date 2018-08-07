import unittest
import json
import app
import utils

class TestFlaskApi(unittest.TestCase):
    def setUp(self):
        self.app = app.app.test_client()

    def test_login_success_and_cookies_dict(self):

        # login user1
        response = self.app.post('/login/', data=json.dumps(dict(username='user1', password='password1')),
                                 content_type='application/json')
        self.assertEqual(response.json, {'success': True})

        number_of_cookies = len(utils.cookie_dict)
        self.assertEqual(number_of_cookies, 1)

        # login user2
        self.app.post('/login/', data=json.dumps(dict(username='user2', password='password2')),
                      content_type='application/json')

        number_of_cookies = len(utils.cookie_dict)
        # Test number of cookies after 2 login
        self.assertEqual(number_of_cookies, 2)

    def test_login_fail(self):

        # Test with wrong password
        response = self.app.post('/login/', data=json.dumps(dict(username='user1', password='password2')),
                                 content_type='application/json')
        self.assertEqual(response.json, {'success': False})

    def test_login_success_and_logout(self):
        ##############
        # Test login #
        ##############
        response = self.app.post('/login/', data=json.dumps(dict(username='user1', password='password1')),
                                 content_type='application/json')
        self.assertEqual(response.json, {'success': True})

        number_of_cookies = len(utils.cookie_dict)
        self.assertEqual(number_of_cookies, 2)

        ###############
        # Test logout #
        ###############
        response = self.app.get('/logout/')
        self.assertEqual(response.json,
                         {"message": "logout successful", "success": True})

        number_of_cookies = len(utils.cookie_dict)
        self.assertEqual(number_of_cookies, 1)

    def test_login_success_and_create_tasks_and_complete_and_delete(self):
        # login user1
        response = self.app.post('/login/', data=json.dumps(dict(username='user1', password='password1')),
                                 content_type='application/json')
        self.assertEqual(response.json, {'success': True})

        #####################
        # Test create tasks #
        #####################
        response = self.app.post('/user1/todo/add', data=json.dumps(dict(message="test message 1")),
                                 content_type='application/json')
        self.assertEqual(response.json,
                         {'message': 'task created', 'success': True})

        todo_list = utils.todo_list
        self.assertEqual(todo_list['user1'][1]['message'], 'test message 1')
        self.assertEqual(todo_list['user1'][1]['completed'], False)

        # Create another task for user1
        self.app.post('/user1/todo/add', data=json.dumps(dict(message="test message 2")),
                      content_type='application/json')

        length_todo_list = len(utils.todo_list['user1'])
        self.assertEqual(length_todo_list, 2)
        self.assertEqual(todo_list['user1'][2]['message'], 'test message 2')

        ############################
        # Test retrieve to.do list #
        ############################

        response = self.app.get('/user1/todo/')
        self.assertEqual(response.json,
                         {'1': {'completed': False, 'message': 'test message 1', 'username': 'user1'},
                          '2': {'completed': False, 'message': 'test message 2', 'username': 'user1'}})

        ################################
        # Test delete inexisting entry #
        ################################

        response = self.app.get('/user1/todo/delete/100/')

        self.assertEqual(response.json,
                         {"message": "we could not find the comment id 100 for user user1",
                          "success": False})

        response = self.app.get('/user1/todo/delete/2/')
        self.assertEqual(list(response.json), ['message', 'success'])

        ############################################
        # Test create task after delete last entry #
        ############################################
        # The app keeps a log of the total amount of tasks already created for the user. This is to avoid the case
        # when the last entry is deleted

        self.app.post('/user1/todo/add', data=json.dumps(dict(message="test message 3")),
                      content_type='application/json')

        response = self.app.get('/user1/todo/')
        self.assertEqual(response.json['3'],
                         {'completed': False, 'message': 'test message 3', 'username': 'user1'})

        length_todo_list = len(utils.todo_list['user1'])
        self.assertEqual(length_todo_list, 2)

        #################
        # Test complete #
        #################
        response = self.app.get('user1/todo/complete/3')
        self.assertEqual(response.json,
                         {'message': 'task updated', 'success': True})

        response = self.app.get('/user1/todo/')
        self.assertEqual(response.json['3']['completed'], True)


if __name__ == "__main__":
    unittest.main()
