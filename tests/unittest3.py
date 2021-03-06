# python3 ./tests/unittest3.py

import unittest
import warnings
import json
import node
import sess
from eosf import *

set_verbose(False)

class Test1(unittest.TestCase):

    contract = None

    def run(self, result=None):
        """ Stop after first error """      
        if not result.failures:
            super().run(result)

    
    @classmethod
    def setUpClass(cls):
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            node.reset()
        sess.init()
        cls.contract = ContractFromTemplate("_e4b2ffc804529ce9c6fae258197648cc2", remove_existing = True)

        
    def setUp(self):
        self.assertTrue(node.is_running(), "testnet failure")
        self.contract = self.__class__.contract
        self.assertTrue(self.contract.is_created(), "contract failure")

        
    def test_01(self):
        self.assertTrue(self.contract.build(), "build")

    
    def test_02(self):
        self.assertTrue(self.contract.deploy(), "deploy")


    def test_03(self):
        self.assertTrue(self.contract.get_code(), "get_code")


    def test_04(self):
        self.assertTrue(
            self.contract.push_action(
            "hi", 
            '{"user":"alice"}',
            sess.alice),
            "push_action hi 1")

        self.assertTrue(
            self.contract.push_action(
            "hi", 
            '{"user":"carol"}',
            sess.carol),
            "push_action hi 2")


    def test_05(self):
        """ This should fail due to authority mismatch """
        set_suppress_error_msg(True)
        self.assertFalse(
            self.contract.push_action(
            "hi", 
            '{"user":"carol"}',
            sess.alice),
            "push_action hi")
        set_suppress_error_msg(False)


    def tearDown(self):
        pass


    @classmethod
    def tearDownClass(cls):
        cls.contract.delete()
        node.stop()


if __name__ == "__main__":
    unittest.main()