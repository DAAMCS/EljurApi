from bs4 import BeautifulSoup
from requests import get, post, Session

class Authorization():

    def __init__(self, client) -> None:
        try:
            self._logger = client._logger
            self._client = client
            self._logger.debug('Auth module initialized successfully')
        except Exception as ex:
            self._logger.error(f'Error during initialization in Auth module: {ex}')

    def open_session(self):
        auth_session = Session()
        self._client.session = auth_session
    
    def login(self, user: str, password: str) -> None:

        auth_data = {
        'username': user,
        'password': password
                }
        
        subdomain = self._client.subdomain

        with self._client.session as login_session:
            #login_url = f'https://{subdomain}.eljur.ru/authorize'
            auth_url = f"https://{subdomain}.eljur.ru/ajaxauthorize"
            login_session.post(url=auth_url, data = auth_data)

            login_url = f"https://{subdomain}.eljur.ru/authorize"
            login_session.get(url = login_url)

        return login_session