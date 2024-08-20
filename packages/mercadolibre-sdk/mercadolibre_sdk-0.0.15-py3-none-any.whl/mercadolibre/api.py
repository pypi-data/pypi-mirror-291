from requests import request

from mercadolibre import Authentication


class MercadoLibreAPI:
    BASE_URL = 'https://api.mercadolibre.com'

    def make_request(self, method: str,
                     path: str,
                     params: dict = None,
                     data: dict = None) -> list | dict | bytes:
        access_token = Authentication().get_access_token()
        headers = {'Content-Type': 'application/json'}

        if access_token:
            headers.update({'Authorization': f'Bearer {access_token}'})

        url = f'{self.BASE_URL}{path}'
        response = request(method, url, headers=headers, params=params, data=data)

        if response.status_code // 100 != 2:
            raise Exception(f'Request failed with status code {response.status_code}: {response.text}')

        if response.headers.get('Content-Type') == 'text/csv':
            return response.content

        return response.json()

    def create_request(self, path: str, data: list | dict) -> dict:
        return self.make_request(method='POST', path=path, data=data)

    def list_request(self, path: str, limit: int = 50, offset: int = 0, params: dict = None) -> list | dict:
        params = self._set_pagination(limit, offset, params)
        return self.make_request(method='GET', path=path, params=params)

    @staticmethod
    def _set_pagination(limit, offset, params):
        if not params:
            params = dict()
        if limit:
            params['limit'] = limit
        if offset:
            params['offset'] = offset
        return params

    def retrieve_request(self, path: str, id: str, params=None):
        path = f'{path}/{id}'
        return self.make_request(method='GET', path=path, params=params)

    def action_request(self, path: str, action: str, id: str, limit: int = 50, offset: int = 0,
                       params: dict = None) -> list | dict:
        path = f'{path}/{id}/{action}'
        params = self._set_pagination(limit, offset, params)
        return self.make_request(method='GET', path=path, params=params)
