import re
from bs4 import BeautifulSoup
from requests import Session, get
import json

class Dispatcher:
    def __init__(self, client) -> None:
        self._logger = client._logger
        try:
            self._client = client
            self._logger.debug('Dispatcher module initialized successfully')
        except Exception as ex:
            self._logger.error(f'Error during initialization in Dispatcher module: {ex}')

    def extractData(self, soup):
        try:
            answer = next((content for tag in soup.find_all("script") 
                        for content in tag.contents if "sentryData" in content), None)[17:-1]

            self._logger.info('User data extracted successfully')
            return json.loads(answer)
        
        except Exception as ex:
            self._logger.error(f'Error during extracting user-data: {ex}')
            return None

    # def _checkPageContent(self, soup):

    #     answer = soup.find("div", class_="page-empty")

    #     if answer:
    #         return {"answer": answer.contents[0],
    #                 "result": False}


    def checkSubdomain(self, subdomain):
        self._logger.debug(f'Checking subdomain "{subdomain}" correctness')
        req = get(f'https://{subdomain}.eljur.ru/authorize')
        if req.status_code != 200:
            self._logger.error(f'Subdomain "{subdomain}" is incorrect')
            return False
        else:
            self._logger.debug(f'Subdomain "{subdomain}" is correct')
            del req
            return True
    
    def checkSession(self, session):
        self._logger.debug(f'Checking session instance')
        if not isinstance(session, Session):
            self._logger.error(f'Session instance is incorrect')
            return False
        else:
            self._logger.debug(f'Sessiom instance is correct')
            return True

    def checkUID(self):
        return True if self._client.clientData['user_id'] is not None else False 

    # def _fullCheck(self, session, url, data=None):
    #     subdomain = self._client.subdomain

    #     checkSession = self._checkInstance(session, Session)
    #     if "error" in checkSession:
    #         return checkSession
    #     del checkSession

    #     getInfo = session.post(url=url, data=data)

    #     checkStatus = self._checkStatus(getInfo, url)
    #     if "error" in checkStatus:
    #         return checkStatus
    #     del checkStatus

    #     soup = BeautifulSoup(getInfo.text, 'lxml')
    #     del getInfo, url

    #     sentryData = self._findData(soup)
    #     if not sentryData:
    #         return {"error": {"error_code": -104,
    #                         "error_msg": "Данные о пользователе не найдены."}}
    #     del sentryData

    #     return soup


    # def _smallCheck(self, subdomain, session, args):
    #     subdomain = self._checkSubdomain(subdomain)
    #     if "error" in subdomain:
    #         return subdomain

    #     checkSession = self._checkInstance(session, Session)
    #     if "error" in checkSession:
    #         return checkSession
    #     del checkSession

    #     checkDict = self._checkInstance(args, dict)
    #     if "error" in checkDict:
    #         return checkDict
    #     del checkDict