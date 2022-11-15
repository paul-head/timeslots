# from datetime import time
from utils import convert_to_minutes, convert_to_readable_time
from db import DBInterface # , redisClient
from calendar import CalendarTimeslot

# не дописана функция конвертирования минут в удобочитаемый формат
# ee можно использовать в book_timeslot, get_available_timeslots

class Employee:
    def __init__(self, fio: str, position: str, start, end):
        self.fio = fio
        self.position = position
        self.start = start
        self.end = end
        self.working_time = CalendarTimeslot.get_working_time(self, self.start, self.end)
        self._initial_slots = CalendarTimeslot.initial_slots_in_minutes(self, self.start, self.end)

    def __str__(self):
        return f"employee name {self.fio} at position {self.position} working time -> {self.working_time}"


def get_all_timeslots(employees_slots):
    all_free_slots = list(set.intersection(*map(set, employees_slots)))
    timeslots = CalendarTimeslot.get_available_timeslots(all_free_slots)
    return timeslots

if __name__ == "__main__":

    e1 = Employee("employee1", "position1", start=[9,0], end=[18,0])
    e2 = Employee("employee2", "position2", start=[8,0], end=[17,0])

    # ---- write/read to db ----
    # with DBInterface() as cursor:
    #     cursor.execute("""
    #     INSERT INTO calendar.employees(columns) VALUES(%s columns)
    #     """, (e1.columns))
    #        ---------

    # записываем слоты кпо ключу в редис
    # redisClient.rpush("e1_slots", *e1_slots)
    # или
    # redisClient.hset("timeslots", e1.fio, e1_slots)


    e1_slots = CalendarTimeslot.book_timeslot(e1._initial_slots, [9,5], [9,15])
    e1_slots = CalendarTimeslot.book_timeslot(e1._initial_slots, [15,15], [16,00])

    e2_slots = CalendarTimeslot.book_timeslot(e2._initial_slots, [9,30], [10,00])
    e2_slots = CalendarTimeslot.book_timeslot(e2._initial_slots, [16,15], [16,40])

    # ---- слоты по ключу в редис ----
    # redisClient.rpush("e1_slots", *e1_slots)

    # redisClient.hset("timeslots", e1.fio, e1_slots)

    e1_available_slots = CalendarTimeslot.get_available_timeslots(e1_slots)

    all_timeslots = get_all_timeslots([e1_slots, e2_slots])
    print(f"all timeslots {all_timeslots}")
    




    
