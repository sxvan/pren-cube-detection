from datetime import datetime
from models.cube_position import CubePosition
import requests


class PrenService:
    def __init__(self, pren_api_base_url, team, datetime_format):
        self.__pren_api_base_url = pren_api_base_url
        self.__team = team
        self.__datetime_format = datetime_format

    def submit(self, cubes: (CubePosition, str)):
        url = self.__get_url() + '/config'
        headers = self.__get_headers()

        body = {
            'time': datetime.now().strftime(self.__datetime_format),  # UTC or local?
            'config': {
                cube_position.value: color
                for cube_position, color in cubes.items()
            }
        }

        response = requests.post(url, json=body, headers=headers)
        return response

    def start(self):
        url = self.__get_url() + '/start'
        headers = self.__get_headers()

        response = requests.post(url, headers=headers)
        return response

    def end(self):
        url = self.__get_url() + '/end'
        headers = self.__get_headers()

        response = requests.post(url, headers=headers)
        return response

    def get(self):
        url = self.__get_url()
        headers = self.__get_headers()

        response = requests.get(url, headers=headers)
        return response

    def __get_url(self):
        return f'{self.__pren_api_base_url}/cubes/team{self.__team}'

    def __get_headers(self):
        return {
            'Content-Type': 'application/json',
            'Auth': 'aTdpCRIrI9CLS1'
        }

