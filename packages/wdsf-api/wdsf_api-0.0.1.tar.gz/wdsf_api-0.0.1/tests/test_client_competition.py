import unittest
import os

from wdsf_api.client import WdsfApi
from wdsf_api.schema import *

class TestWdsfApi(unittest.TestCase):

    COMP_ID = 123

    def setUp(self) -> None:

        self.client = WdsfApi(
            'staging',
            auth=(os.getenv('WDSF_API_USERNAME'), os.getenv('WDSF_API_PASSWORD'))
            )
    
    def test_get_competition(self):

        data = self.client.get_competition(self.COMP_ID)
        self.assertIsInstance(data, list)

    
    def test_create_official(self):

        officials = {
            'A': 123,
            'B': 123,
            'C': 123
        }

        for letter, min in officials.items:
            
            self.client.create_official(Official(
                task=Official.Task.Adjudicator,
                letter=letter,
                min=min,
                competitionId=self.COMP_ID
                ))
    
    def test_create_participant(self):

        self.client.create_participant(Participant(
            number = 21,
            status = Participant.Status.Present,
            competitionId = self.COMP_ID,
            coupleId = 'rls-4588'
        ))