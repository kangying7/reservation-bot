from calendar import FRIDAY, MONDAY, SATURDAY, THURSDAY, TUESDAY, WEDNESDAY, SUNDAY, calendar, day_name
import datetime


onDay = lambda date, day: date + datetime.timedelta(days=(day-date.weekday())%7)

def dayOnNextWeek(target_day: datetime.datetime.day):
    today = datetime.datetime.today()
    diff_in_days_to_next_monday = datetime.timedelta(days=(MONDAY-today.weekday())%7)
    # print("Difference in days are", diff_in_days)
    next_monday_date = today + diff_in_days_to_next_monday

    # print("Target day is", target_day)
    next_week_date = next_monday_date + datetime.timedelta(days=target_day)
    return next_week_date.strftime("%d/%b/%Y")

def dayOnThisWeek(target_day: datetime.datetime.day):
    today = datetime.datetime.today()
    diff_in_days_to_this_monday = datetime.timedelta(days=(today.weekday()-MONDAY)%7)
    # print("Difference in days are", diff_in_days)
    this_monday_date = today - diff_in_days_to_this_monday

    # print("Target day is", target_day)
    this_week_date = this_monday_date + datetime.timedelta(days=target_day)
    return this_week_date.strftime("%d/%b/%Y")

# print(onDay(datetime, ))

if __name__ == "__main__":
    today = datetime.datetime.today()
    print("Today is", today.date())

    print("Next Monday is", dayOnNextWeek(MONDAY))
    print("Next Tuesday is", dayOnNextWeek(TUESDAY))
    print("Next Wednesdaay is", dayOnNextWeek(WEDNESDAY))
    print("Next Thursday is", dayOnNextWeek(THURSDAY))
    print("Next Friday is", dayOnNextWeek(FRIDAY))
    print("Next Saturday is", dayOnNextWeek(SATURDAY))
    print("Next Sunday is", dayOnNextWeek(SUNDAY))

    print(f"six_april is {day_name[TUESDAY]}")