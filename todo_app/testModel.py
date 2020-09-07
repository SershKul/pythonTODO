import datetime
import unittest

from todo_app import *

now = datetime.datetime.now()


class TestDB(unittest.TestCase):
    def setUp(self):
        Task.delete().execute()

    def test_create(self):
        insert = {'title':'newTitle','content':'newContent'}
        Task.create_todo(insert)
        result = Task.select().where(Task.id == 1).dicts().get()
        self.assertEqual(result.get('title'), insert.get('title'))
        self.assertEqual(result.get('content'), insert.get('content'))

    def test_read(self):
        insert = {'title':'newTitle','content':'newContent'}
        Task.create(title = 'newTitle', content = 'newContent' , created_at = now)
        result = Task.get_todo(1)
        self.assertEqual(result.get('title'), insert.get('title'))
        self.assertEqual(result.get('content'), insert.get('content'))
        with self.assertRaises(DoesNotExist):
            Task.select().where(Task.id == 2).dicts().get()

    def test_read_list(self):
        insert1 = {'title':'newTitle','content':'newContent'}
        insert2 = {'title':'newTitle2','content':'newContent2'}
        Task.create(title = 'newTitle', content = 'newContent' , created_at = now)
        Task.create(title = 'newTitle2', content = 'newContent2' , created_at = now)
        result = Task.get_all_todos()
        self.assertEqual(result[0].get('title'), insert1.get('title')) 
        self.assertEqual(result[1].get('title'), insert2.get('title'))

    def test_update(self):
        insert = {'title':'updatedTitle','content':'updatedContent'}
        Task.create(title = 'newTitle', content = 'newContent' , created_at = now)
        Task.update_todo(1, insert)
        result = Task.select().where(Task.id == 1).dicts().get()
        self.assertEqual(result.get('title'), insert.get('title'))
        self.assertEqual(result.get('content'), insert.get('content'))
        with self.assertRaises(DoesNotExist):
            Task.select().where(Task.id == 2).dicts().get()

    def test_delete(self):
        Task.create(title = 'newTitle', content = 'newContent' , created_at = now)
        Task.delete_todo(1)
        with self.assertRaises(DoesNotExist):
            Task.select().where(Task.id == 1).dicts().get()

if __name__ == '__main__':
    database.init('testDB.db')
    create_tables()
    unittest.main()








    
