from JournalApi.auth import Authorization
from JournalApi.journal import Journal
import logging

class Client:
    def __init__(self, subdomain: str) -> None:
        self.subdomain = subdomain
        self._logger = logging.getLogger(__name__)
        self._logger.info(f'Started logging for EljurApi Client')
        self.auth = Authorization(self)
        self.journal = Journal(self)
