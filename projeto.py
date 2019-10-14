import subprocess
import unittest


class TestCase(unittest.TestCase):
    @classmethod
    def setUpClass(TestCase):
        with open('creation_script.sql', 'rb') as f:
            res = subprocess.run('mysql -u root -proot'.split(),stdin=f)
            print(res)

    def test_teste(self):
        pass
    def test_teste2(self):
        pass
    def test_teste3(self):
        pass
    def test_teste4(self):
        pass
    def test_teste5(self):
        pass
    


if __name__=='__main__':
    unittest.main()