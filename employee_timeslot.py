from datetime import time, timedelta, datetime
from db import DBInterface


## Можно сделать основным классом TimeSlot(Calendar) и делать композицию через него с работником

time_format = "%Y-%m-%d %H:%M"


class Timeslot:
    """
    учитывать , что слоты используют фиксированное время или нет ?
    проверка, что слоты не пересекаются по времени 
    """
    def __init__(self, start: datetime, end: datetime):
        if start > end:
            raise ValueError("Timeslot cannot be negative")
        self.start = start
        self.end = end

    def __repr__(self):
        return f"Timeslot {self.start} {self.end}"

    # @property
    def duration(self) -> timedelta:
        return self.end - self.start

    def __lt__(self, other: object) -> bool:
        # для сортировки слотов 
        if isinstance(other, Timeslot):
            return self.start < other.start
        else:
            raise TypeError(
                "operator not supported between instaces of '{}' and '{}'".format(
                    type(self), type(other)
                )
            )

    def overlaps(self, other: "Timeslot") -> bool:
        # не доделана проверка пересечения слотов
        return (
            self.start <= other.start < self.end
            or self.start < other.end <= self.end
            or self in other
        )


class Employee:
    def __init__(self, fio: str, position: str, start_working=datetime(2022, 11, 22, 9, 0), end_working=datetime(2022, 11, 22, 18, 0)):
        self.fio = fio
        self.position = position
        self._timeslots = [] # list of Timeslots
        self._timeslots_duration = timedelta(minutes=0)
        self.start_working = start_working
        self.end_working = end_working

    def __str__(self):
        return f"employee name {self.fio} at position {self.position}, day starts at {self.start_working.time()} ends at {self.end_working.time()}"

    def get_working_time(self):
        # получить рабочее время
        return (self.end_working - self.start_working)

    def get_free_slots(self):
        # получить свободные слоты 
        if not self._timeslots:
            print(f"all timeslots available from {self.start_working.time()} until {self.end_working.time()}")
        # TODO: не завершена 
        else:
            free_slots = []
            sorted_slots = sorted(self._timeslots)
            for i in sorted_slots:
                free_slots.append([self.start_working, i.start])
                # ......

    def check_can_add_timeslots(self, timeslot: Timeslot):
        # проверить можно ли еще назначить встречу
        if self._timeslots_duration + timeslot.duration() < self.get_working_time():
            self._timeslots_duration += timeslot.duration()
            return True
        print("cant add new slot , out of working time!")
        return False

    def books_slot(self, timeslot: Timeslot):
        # забронить время
        if timeslot.start < self.start_working or timeslot.end > self.end_working:
            print(f"uncorrect timeslot, time slot must be in interval {self.start_working.time()} - {self.end_working.time()}")
        if self.check_can_add_timeslots(timeslot):
            print("check_can_add_timeslots TRUE, will append")
            self._timeslots.append(timeslot)
        else:
            print("check_can_add_timeslots FALSE, will NOT append")


def get_free_slots_from_all_employees(lst_employees: list) -> list:
    """
    принимает list[Employee]
    TODO: не доделан . использовать функцию overlap и возможно надо еще использовать set
    """
    pass
    
    

if __name__ == "__main__":
    e1 = Employee("employee1", "position1", start_working=datetime(2022,11,22,9,0))

    # записать в базу 
    # ---- write/read to db ----
    # with DBInterface() as cursor:
    #     cursor.execute("""
    #     INSERT INTO calendar.employees(columns) VALUES(%s columns)
    #     """, (e1.columns))
    #        ---------


    t1 = Timeslot(start=datetime(2022,11,22,10,0), end=datetime(2022,11,22,10,15))
    t2 = Timeslot(start=datetime(2022,11,22,11,0), end=datetime(2022,11,22,11,30))
    t3 = Timeslot(start=datetime(2022,11,22,10,15), end=datetime(2022,11,22,17,30))
    t4 = Timeslot(start=datetime(2022,11,22,16,40), end=datetime(2022,11,22,16,50))
    t5 = Timeslot(start=datetime(2022,11,22,15,0), end=datetime(2022,11,22,18,0))

    e1.books_slot(t2)
    e1.books_slot(t1)
    print(e1.get_free_slots())

    # e1.books_slot(t2)
    # print("-----")
    # e1.books_slot(t3)
    # e1.books_slot(t4)
    # print(t1.duration)
    # e1.books_slot(t5)


    
