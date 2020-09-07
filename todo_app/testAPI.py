import unittest
from todo_app import *

class TodoApiTestCase(unittest.TestCase):
    def setUp(self):
        Task.delete().execute()
        database.close()

    def test_get(self):
        example1 = {'title':'newTitle1','content':'newContent1'}
        example2 = {'title':'newTitle2','content':'newContent2'}
        Task.create(title = 'newTitle1', content = 'newContent1' , created_at = now)
        Task.create(title = 'newTitle2', content = 'newContent2' , created_at = now)
        database.close()
        with app.test_client() as c:
            response = c.get('/task/')
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.get_json()[0].get('title'), example1.get('title'))
            self.assertEqual(response.get_json()[1].get('title'), example2.get('title'))

    def test_post(self):
        example1 = {'title':'newTitle1','content':'newContent1'}
        database.close()
        with app.test_client() as c:
            response = c.post('/task/', json = {'title':'newTitle1','content':'newContent1'})
            result = Task.get_todo(1)
            self.assertEqual(result.get('title'), example1.get('title'))
            self.assertEqual(result.get('content'), example1.get('content'))
            self.assertEqual(response.status_code, 200)

    def test_get_detail(self):
        example1 = {'title':'newTitle1','content':'newContent1'}
        Task.create(title = 'newTitle1', content = 'newContent1' , created_at = now)
        database.close()
        with app.test_client() as c:
            response = c.get('/task/1')
            self.assertEqual(response.get_json().get('title'), example1.get('title'))
            self.assertEqual(response.get_json().get('content'), example1.get('content'))
            self.assertEqual(response.status_code, 201)

    def test_update(self):
        example1 = {'title':'newTitle1','content':'newContent1'}
        Task.create(title = 'newTitle1', content = 'newContent1' , created_at = now)
        database.close()
        with app.test_client() as c:
            response = c.put('/task/1', json = dict(
                title = 'updated_title',
                content = 'updated_title'))
            result = Task.get_todo(1)
            self.assertEqual(result.get('title'), 'updated_title')
            self.assertEqual(result.get('content'), 'updated_title')
            self.assertEqual(response.status_code, 200)

    def test_delete(self):
        example1 = {'title':'newTitle1','content':'newContent1'}
        Task.create(title = 'newTitle1', content = 'newContent1' , created_at = now)
        database.close()
        with app.test_client() as c:
            response = c.delete('/task/1')
            self.assertEqual(response.status_code, 204)
            response = c.delete('/task/1')
            self.assertEqual(response.status_code, 404)

if __name__ == '__main__':
    app.config['TESTING'] = True
    database.init('testDB.db')
    unittest.main()


