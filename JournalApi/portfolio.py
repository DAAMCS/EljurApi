from bs4 import BeautifulSoup

class Portfolio:
    def __init__(self, client) -> None:
        try:
            self._client = client
            self._logger = client._logger
            self._logger.debug('Portfolio module initialized successfully')
        except Exception as ex:
            self._logger.error(f'Error during initialization in Portfolio module: {ex}')

    def get_quarter_grades(self, quarter="I"):

        if self._client._dispatcher.checkUID() is False:
            self._logger.error(f'Failed to get report card: UID not found. Probably not authorized')
            return None
        
        else:
            pass
        
        user_id = self._client.clientData['user_id']
        subdomain = self._client._subdomain

        url = f"https://{subdomain}.eljur.ru/journal-student-grades-action/u.{user_id}/sp.{quarter}+четверть"

        req = self._client._session.get(url)

        soup = BeautifulSoup(req.text, 'lxml')

        card = {}

        subjects = soup.find_all("div", class_="text-overflow lhCell offset16")

        for subject in subjects:
            scores = []
            for score in soup.find_all("div", class_=["cell blue", "cell"], attrs={"name": subject.contents[0]}):
                if "mark_date" in score.attrs and score.attrs["id"] != "N":
                    scores.append({score.attrs["mark_date"], score.contents[1].contents[0]})
            card[subject.contents[0]] = scores
        card["result"] = True
    
        return card
        
    def get_final_grades(self, year):
        
        if self._client._dispatcher.checkUID() is False:
            self._logger.error(f'Failed to get report card: UID not found. Probably not authorized')
            return None
        else: pass
        
        user_id = self._client.clientData['user_id']
        subdomain = self._client._subdomain

        url = f"https://{subdomain}.eljur.ru/journal-student-resultmarks-action/u.5600/view.results/?year={year}"

        req = self._client._session.get(url)

        soup = BeautifulSoup(req.text, 'lxml')
        
        columns_dict = {
            'I': None,
            'II': None,
            'III': None,
            'IV': None,
            'Year': None,
            'Final': None
        }

        quarters_columns = soup.find_all("div", class_="cells cells_marks")
        year_column = soup.find("div", class_="cells red id_yearly cells_marks")
        final_column = soup.find("div", class_="cells cells_marks cells_red_bg id_results")

        for i, key in enumerate(columns_dict):
            if i < len(quarters_columns):
                columns_dict[key] = quarters_columns[i]
            else:
                break

        columns_dict["Year"] = year_column
        columns_dict["Final"] = final_column
        
        
        for quarter, column in columns_dict.items():
            column_dict = {}
            
            cells = column.find_all("div", class_="cell")

            for cell in cells:
                try:
                    cell_mark = cell.find("div", class_="cell-data").contents[0]
                    cell_name = cell.get("name")
                    column_dict[cell_name] = cell_mark
                except: 
                    pass

            columns_dict[quarter] = column_dict
        return columns_dict