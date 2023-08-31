from bs4 import BeautifulSoup

class Timetable:
    def __init__(self, client) -> None:
        self._logger = client._logger
        try:
            self._client = client
            self._logger.debug('Timetable module initialized successfully')
        except Exception as ex:
            self._logger.error(f'Error during initialization in Timetable module: {ex}')

    def get_timetable(self, week = None):

        if self._client._dispatcher.checkUID() is False:
            self._logger.error(f'Failed to get timetable: UID not found. Probably not authorized')
            return None

        else:
            pass

        subdomain = self._client._subdomain
        session = self._client._session
        uid = self._client.clientData['user_id']

        timetable_week = week

        self._logger.info(f'Getting actual timetable')

        url = f'https://{subdomain}.eljur.ru/journal-schedule-action/u.{uid}'

        TimetablePage = session.get(url)
        soup = BeautifulSoup(TimetablePage.text, 'lxml')
        
        timetable = {}

        days = soup.find_all("div", class_="schedule__day")

        for day in days:

            day_content = day.find("div", class_="schedule__day__content")
            column = day_content.find("div", class_="schedule__day__content__column")

            if day.find("p", class_="schedule__day__content__header__dayweek") is not None: day_name = day.find("p", class_="schedule__day__content__header__dayweek").contents[0].strip()

            lessons_dict = {}
            lessons = column.find_all("div", class_="schedule__day__content__lesson schedule__day__content__lesson--main")
            
            for lesson in lessons:
                
                if lesson.find("div", class_="schedule__day__content__lesson__num") is not None and lesson.find("div", class_="schedule__day__content__lesson__num") != '': lesson_num = lesson.find("div", class_="schedule__day__content__lesson__num").contents[0].strip()
                if lesson.find("div", class_="schedule__day__content__lesson__time") is not None: lesson_time = lesson.find("div", class_="schedule__day__content__lesson__time").contents[0].strip()
                if lesson.find("span", class_="schedule-lesson") is not None: lesson_name = lesson.find("span", class_="schedule-lesson").contents[0].strip()
                if lesson.find("div", class_="schedule-teacher") is not None: lesson_teacher = lesson.find("div", class_="schedule-teacher").contents[0].strip()
                if lesson.find("span", class_="schedule-group") is not None: lesson_group = lesson.find("span", class_="schedule-group").contents[0].strip()

                if lesson_num in lessons_dict.keys():
                    break

                lessons_dict[lesson_num] = {
                'lesson_time':lesson_time,
                'lesson_name':lesson_name,
                'lesson_group':lesson_group,
                'lesson_teacher':lesson_teacher
                }

            timetable[day_name] = lessons_dict

        self._logger.info(f'Got actual timetable')

        return timetable
