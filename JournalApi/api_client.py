from JournalApi.dispatcher import Dispatcher
from JournalApi.auth import Authorization
from JournalApi.journal import Journal
from JournalApi.portfolio import Portfolio
from JournalApi.timetable import Timetable
#from JournalApi.status import Status
import logging

class Client:
    def __init__(self, subdomain: str) -> None:
        self._logger = logging.getLogger(__name__)
        self._logger.info(f'Started logging for EljurApi Client')

        #self._status = Status(self)
        self._dispatcher = Dispatcher(self)

        self.auth = Authorization(self)
        self.journal = Journal(self)
        self.portfolio = Portfolio(self)
        self.timetable = Timetable(self)

        if self._dispatcher.checkSubdomain(subdomain): self._subdomain = subdomain
        self.clientData = {
            "subdomain": self._subdomain,
            "user_id": None,
            "username": None,
            "role": None,
        }

    def __str__(self) -> str:
        str = f"""
JournalApi.api_client.Client object, params:
{self.clientData}
        """
        return str
    
    def __repr__(self) -> str:
        return f'Client({self._subdomain})'
    
    def __getitem__(self, key):
        return self.clientData[key]