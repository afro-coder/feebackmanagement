
import unittest
from .. import create_app
class HomeTest(unittest.TestCase):
    """
    This class will test the home page along with login
    """
    def setUp(self):
        """
        Setup various variables
        """
        
        self.app=create_app(config_name='testing')
        self.client=self.app.test_client()

    def test_home_route(self):
        result=self.client.get('/home')
        self.assertEqual(result.status_code,200)

        result=self.client.get('/')
        self.assertEqual(result.status_code,200)

        result=self.client.get('/index/')
        self.assertEqual(result.status_code,200)

#if __name__=="__main__":
#    unittest.main()
