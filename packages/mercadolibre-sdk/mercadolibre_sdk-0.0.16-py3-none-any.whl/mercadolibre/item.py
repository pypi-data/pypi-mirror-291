from .api import MercadoLibreAPI

api = MercadoLibreAPI()


class Item:
    @classmethod
    def retrieve(cls, id: str) -> dict:
        return api.retrieve_request(path=f'/items', id=id)

    @classmethod
    def description(cls, id: str) -> dict:
        return api.action_request(path='/items', id=id, action='description')
