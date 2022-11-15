from datetime import time
from utils import convert_to_minutes


DAY = list(range(1440))
time_format = "%H:%M"


class CalendarTimeslot:
    def get_working_time(self, start, end):
        # получаем удобочитаемое рабочее время 
        start = time(self.start[0], self.start[1]).strftime(time_format)
        end = time(self.end[0], self.end[1]).strftime(time_format)
        return start, end

    def initial_slots_in_minutes(self, start, end):
        # переводим рабочее время в список минут
        start = convert_to_minutes(self.start)
        end = convert_to_minutes(self.end)
        return DAY[start:end+1]

    @staticmethod
    def book_timeslot(employee_slots, start, end):
        # бронируем время
        start_slot = convert_to_minutes(start)
        end_slot = convert_to_minutes(end)
        book_slots = list(range(start_slot, end_slot+1))
        for i in book_slots:
            if i in employee_slots:
                employee_slots.remove(i)
        return employee_slots

    @staticmethod
    def get_available_timeslots(employee_slots):
        # получем свободные слоты
        available_slots = []
        index = 0
        for i in range(len(employee_slots) - 1):
            if employee_slots[i + 1] - employee_slots[i] > 1:
                available_slots.append([employee_slots[index], employee_slots[i]])
                index = i + 1
            elif i + 1 == len(employee_slots) - 1:
                available_slots.append([employee_slots[index], employee_slots[i+1]])
        return available_slots
