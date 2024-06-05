import threading
from datetime import datetime
from models.cube_position import CubePosition
import requests


class PrenService:
    def __init__(self, pren_api_base_url, team, datetime_format):
        self._pren_api_base_url = pren_api_base_url
        self._team = team
        self._datetime_format = datetime_format

    def submit(self, cubes: (CubePosition, str)):
        url = self._get_url() + '/config'
        headers = self._get_headers()

        body = {
            'time': datetime.now().strftime(self._datetime_format),  # UTC or local?
            'config': {
                cube_position.value: color
                for cube_position, color in cubes.items()
            }
        }

        response = requests.post(url, json=body, headers=headers)
        return response

    def start(self):
        url = self._get_url() + '/start'
        headers = self._get_headers()

        response = requests.post(url, headers=headers)
        return response

    def start_thread(self):
        thread = threading.Thread(target=self.start)
        thread.daemon = True  # Ensure the thread will exit when the main program exits
        thread.start()

    def end(self):
        url = self._get_url() + '/end'
        headers = self._get_headers()

        response = requests.post(url, headers=headers)
        return response

    def get(self):
        url = self._get_url()
        headers = self._get_headers()

        response = requests.get(url, headers=headers)
        return response

    def _get_url(self):
        return f'{self._pren_api_base_url}/cubes/team{self._team}'

    @staticmethod
    def _get_headers():
        return {
            'Content-Type': 'application/json',
            'Auth': 'z3u2dNeHQdlp'
        }

