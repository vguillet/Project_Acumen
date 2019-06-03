"""
Test file, contains the test functions for testing Compatibility_script
"""

from src.Compatibility_script import compile_data_bank
from dbinterface.DBAlgoAPI import KeyCodeTools


def test_compile_data_bank():
    data_bank = compile_data_bank(['CapitalsOfTheAmericas'])
    q = KeyCodeTools().get_all_questions('CapitalsOfTheAmericas')
    assert len(data_bank) == len(q)
