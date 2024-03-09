from datetime import datetime
from models.cube_position import CubePosition
import requests


class SubmissionService:
    def __init__(self, submission_base_url, team, datetime_format):
        self.__submission_base_url = submission_base_url
        self.__team = team
        self.__datetime_format = datetime_format

    def submit(self, cubes: (CubePosition, str)):
        url = f'{self.__submission_base_url}/cubes/team{self.__team}'

        headers = {
            'Content-Type': 'application/json',
            'Auth': 'test1234'
        }

        body = {
            'time': datetime.now().strftime(self.__datetime_format),  # UTC or local?
            'config': {
                cube_position.value: color
                for cube_position, color in cubes.items()
            }
        }

        response = requests.post(url, json=body, headers=headers)
        return response
