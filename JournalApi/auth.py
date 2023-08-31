from bs4 import BeautifulSoup
from requests import get, post, Session

class Authorization:

    def __init__(self, client) -> None:
        try:
            self._logger = client._logger
            self._client = client
            self._logger.debug('Auth module initialized successfully')
        except Exception as ex:
            self._logger.error(f'Error during initialization in Auth module: {ex}')

    def _open_session(self):
        auth_session = Session()
        if self._client._dispatcher.checkSession(auth_session): self._client._session = auth_session
    
    def close_session(self):
        self._client.session.close() 
        del self._client.session

    def login(self, user: str, password: str) -> None:
        
        if not hasattr(self._client, '_session'): self._client.auth._open_session()

        auth_data = {
        'username': user,
        'password': password
                }
        
        subdomain = self._client._subdomain

        with self._client._session as login_session:
            auth_url = f"https://{subdomain}.eljur.ru/ajaxauthorize"
            login_session.post(url=auth_url, data = auth_data)

            login_url = f"https://{subdomain}.eljur.ru/authorize"
            resp = login_session.get(url = login_url)

            soup = BeautifulSoup(resp.text, 'lxml')

            sentryData = self._client._dispatcher.extractData(soup)

            self._client.clientData['user_id'] = sentryData['user']['uid']
            self._client.clientData['username'] = sentryData['user']['username']
            self._client.clientData['role'] = sentryData['user']['role']

            del soup

        return login_session