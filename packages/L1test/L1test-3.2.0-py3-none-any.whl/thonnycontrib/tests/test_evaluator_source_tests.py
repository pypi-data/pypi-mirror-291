from thonnycontrib.tests.fixtures.backend_mock import *
import unittest

from types import ModuleType

from thonnycontrib.backend.evaluator import Evaluator
from thonnycontrib.backend.ast_parser import L1DocTestFlag
from thonnycontrib.backend.verdicts.PassedVerdict import PassedVerdict
from thonnycontrib.backend.verdicts.FailedVerdict import FailedVerdict

class TestEvaluatorWithAdditionalSourceTest(unittest.TestCase):
    '''
    Test de la méthode evaluate quand des tests externes
    sont passés en paramètre.
    '''

    def setUp(self):
        self.evaluator = Evaluator(filename="<string>")
        self.mock_backend = backend_patch.start()
    
    def tearDown(self) -> None:
        del self.evaluator
        backend_patch.stop()
        
    def test_no_tests_in_source_additional_tests_no_additionnal_code(self):
        '''Teste le cas où les tests extérieurs ne sont pas accompagnés de
        code extérieur, et où inversement le code source n'est pas
        accompagné de tests.

        '''
        fake_source = \
"""
def foo(x : int, liste : list[int]) -> bool:
    '''
    $$$ 
    '''
    return x in liste
"""
        fake_source_tests = \
"""
def foo(x : int, liste : list[int]) -> bool:
    '''
    $$$ foo(3, [1, 3, 4])
    True
    $$$ foo(2, [1, 3, 4])
    True
    $$$ foo(2, [])
    False
    '''
    pass
"""                    
        self.evaluator.set_source(fake_source)
        self.evaluator.set_module(self.__build_module_from_source(fake_source))
        
        # ###########################################################
        
        # ###################################################
        # ------------- Vérification du verdict -------------
        l1doctests = self.evaluator.evaluate(fake_source_tests)
        
        # on assure qu'il existe un seul l1doctest avec ses examples
        self.assertEqual(len(l1doctests), 1)
        l1doctest = l1doctests[0]
        self.assertTrue(l1doctest.is_evaluated()) # s'assure que le l1doctest a été évalué
        self.assertEqual(l1doctest.get_flag(), L1DocTestFlag.FAILED_FLAG)
        
        examples = l1doctest.get_examples()
        self.assertEqual(len(examples), 3) 
        verdict1 = l1doctest.get_verdict_from_example(examples[0])
        self.assertTrue(isinstance(verdict1, PassedVerdict))
        verdict2 = l1doctest.get_verdict_from_example(examples[1])
        self.assertTrue(isinstance(verdict2, FailedVerdict))
        verdict3 = l1doctest.get_verdict_from_example(examples[2])
        self.assertTrue(isinstance(verdict3, PassedVerdict))


    def test_no_tests_in_source_additional_tests_additionnal_code(self):
        '''Teste le cas où les tests extérieurs sont accompagnés de code
        extérieur (qui n'est pas exécuté), et où le code
        source n'est pas accompagné de tests.

        '''
        fake_source = \
"""
def foo(x : int, liste : list[int]) -> bool:
    '''
    $$$ 
    '''
    return x in liste
"""
        fake_source_tests = \
"""
def foo(x : int, liste : list[int]) -> bool:
    '''
    $$$ foo(3, [1, 3, 4])
    True
    $$$ foo(2, [1, 3, 4])
    True
    $$$ foo(2, [])
    False
    '''
    return "nimportequoi"
"""                    
        self.evaluator.set_source(fake_source)
        self.evaluator.set_module(self.__build_module_from_source(fake_source))
        
        # ###########################################################
        
        # ###################################################
        # ------------- Vérification du verdict -------------
        l1doctests = self.evaluator.evaluate(fake_source_tests)
        
        l1doctest = l1doctests[0]
        examples = l1doctest.get_examples()
        self.assertEqual(len(examples), 3) 
        verdict1 = l1doctest.get_verdict_from_example(examples[0])
        self.assertTrue(isinstance(verdict1, PassedVerdict))
        verdict2 = l1doctest.get_verdict_from_example(examples[1])
        self.assertTrue(isinstance(verdict2, FailedVerdict))
        verdict3 = l1doctest.get_verdict_from_example(examples[2])
        self.assertTrue(isinstance(verdict3, PassedVerdict))
        

    def test_tests_in_source_additional_tests_additionnal_code(self):
        '''Teste le cas où les tests extérieurs sont accompagnés de code
        extérieur (qui n'est pas exécuté), et où le code
        source est accompagné de tests (qui ne sont pas exécutés).

        '''
        fake_source = \
"""
def foo(x : int, liste : list[int]) -> bool:
    '''
    $$$ 1/0
    False
    $$$ foo()
    False
    '''
    return x in liste
"""
        fake_source_tests = \
"""
def foo(x : int, liste : list[int]) -> bool:
    '''
    $$$ foo(3, [1, 3, 4])
    True
    $$$ foo(2, [1, 3, 4])
    True
    $$$ foo(2, [])
    False
    '''
    return "nimportequoi"
"""                    
        self.evaluator.set_source(fake_source)
        self.evaluator.set_module(self.__build_module_from_source(fake_source))
        
        # ###########################################################
        
        # ###################################################
        # ------------- Vérification du verdict -------------
        l1doctests = self.evaluator.evaluate(fake_source_tests)
        
        l1doctest = l1doctests[0]
        examples = l1doctest.get_examples()
        self.assertEqual(len(examples), 3) 
        verdict1 = l1doctest.get_verdict_from_example(examples[0])
        self.assertTrue(isinstance(verdict1, PassedVerdict))
        verdict2 = l1doctest.get_verdict_from_example(examples[1])
        self.assertTrue(isinstance(verdict2, FailedVerdict))
        verdict3 = l1doctest.get_verdict_from_example(examples[2])
        self.assertTrue(isinstance(verdict3, PassedVerdict))

    def test_tests_in_source_additional_tests_additionnal_bad_signature(self):
        '''Teste le cas où les tests extérieurs sont accompagnés de code
        extérieur (qui n'est pas exécuté) et d'une signature qui n'a
        pas de sens (on s'en fiche), et où le code source est
        accompagné de tests (qui ne sont pas exécutés).

        '''
        fake_source = \
"""
def foo(x : int, liste : list[int]) -> bool:
    '''
    $$$ 1/0
    False
    $$$ foo()
    False
    '''
    return x in liste
"""
        fake_source_tests = \
"""
def bar() -> None:
    '''
    $$$ foo(3, [1, 3, 4])
    True
    $$$ foo(2, [1, 3, 4])
    True
    $$$ foo(2, [])
    False
    '''
    return "nimportequoi"
"""                    
        self.evaluator.set_source(fake_source)
        self.evaluator.set_module(self.__build_module_from_source(fake_source))
        
        # ###########################################################
        
        # ###################################################
        # ------------- Vérification du verdict -------------
        l1doctests = self.evaluator.evaluate(fake_source_tests)
        
        l1doctest = l1doctests[0]
        examples = l1doctest.get_examples()
        self.assertEqual(len(examples), 3) 
        verdict1 = l1doctest.get_verdict_from_example(examples[0])
        self.assertTrue(isinstance(verdict1, PassedVerdict))
        verdict2 = l1doctest.get_verdict_from_example(examples[1])
        self.assertTrue(isinstance(verdict2, FailedVerdict))
        verdict3 = l1doctest.get_verdict_from_example(examples[2])
        self.assertTrue(isinstance(verdict3, PassedVerdict))


        
    def __build_module_from_source(self, source: str) -> ModuleType:
        """
        Build a module containing the functions declared in the given `source`.
        """
        from types import ModuleType
        fake_module = ModuleType(self.evaluator.get_filename())
        exec(source, fake_module.__dict__)
        return fake_module
