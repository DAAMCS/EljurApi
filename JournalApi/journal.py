from bs4 import BeautifulSoup

class Journal:
    def __init__(self, client) -> None:
        self._logger = client._logger
        try:
            self._client = client
            self._logger.debug('Journal module initialized successfully')
        except Exception as ex:
            self._logger.error(f'Error during initialization in Journal module: {ex}')

    def get_journal(self, week=0):

        subdomain = self._client._subdomain
        session = self._client._session
        journal_week = week

        self._logger.info(f'Getting Journal for week {journal_week}')

        url = f"https://{subdomain}.eljur.ru/journal-app/week.{week * -1}"

        JournalPage = session.post(url=url)

        soup = BeautifulSoup(JournalPage.text, 'lxml')
        info = {}

        for day in soup.find_all("div", class_="dnevnik-day"):
            title = day.find("div", class_="dnevnik-day__title")
            week, date = title.contents[0].strip().replace("\n", "").split(", ")

            if day.find("div", class_="page-empty"):
                info.update([(week, {"date": date, "isEmpty": True, "comment": "Нет уроков", "lessons": {}})])
                continue

            if day.find("div", class_="dnevnik-day__holiday"):
                info.update([(week, {"date": date, "isEmpty": True, "comment": "Выходной", "lessons": {}})])
                continue

            lessons = day.find_all("div", class_="dnevnik-lesson")
            
            lessonsDict = {}
            if lessons:
                for lesson in lessons:
                    lessonNumber = lesson.find("div", class_="dnevnik-lesson__number dnevnik-lesson__number--time")
                    if lessonNumber:
                        lessonNumber = lessonNumber.contents[0].replace("\n", "").strip()[:-1]

                    lessonTime = lesson.find("div", class_="dnevnik-lesson__time").contents[0].strip().replace("\n", "")
                    lessonName = lesson.find("span", class_="js-rt_licey-dnevnik-subject").contents[0]

                    lessonHomeTask = lesson.find("div", class_="dnevnik-lesson__task")
                    if lessonHomeTask:
                        lessonHomeTask = lessonHomeTask.contents[2].replace("\n", "").strip()

                    lessonMark = lesson.find("div", class_="dnevnik-mark")
                    if lessonMark:
                        lessonMark = lessonMark.contents[1].attrs["value"]

                    lessonsDict.update([(lessonNumber, {"time": lessonTime,
                                                        "name": lessonName,
                                                        "hometask": lessonHomeTask,
                                                        "mark": lessonMark})])

                info.update([(week, {"date": date, "isEmpty": False, "comment": "Выходной", "lessons": lessonsDict})])
        
        self._logger.info(f'Got journal for week {journal_week}')
        
        return info
    
    def get_day(self, journal, day:int):
        journal_day = day
        self._logger.info(f'Getting journal-day data for day {journal_day}')

        day = list(journal.items())[day-1]
        self._logger.info(f'Got journal-day data for day {journal_day}')

        return day