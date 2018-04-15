from django import template

register = template.Library()


@register.filter
def hour_test(hourStr):
    # print "hourStr: {}".format(hourStr)
    x = hourStr.split(':')
    period = "AM";
    hour = x[0]
    if int(hour) > 12:
        period = "PM"
        hour = str(int(hour)-12)
    elif int(hour) == 0:
        hour = str(12)
    minutes = x[1]
    time = "{}:{} {}".format(hour,minutes,period)
    return time

@register.filter
def hour_diff(start,end):

    print "start: {}, end: {}".format(start,end)
    time1 = start.split(":")
    start_hour = int(time1[0])
    start_minutes = int(time1[1])

    time2 = end.split(":")
    end_hour = int(time2[0])
    end_minutes = int(time2[1])

    diff = end_hour - start_hour

    if diff < 0:
        end_hour += 24


    print "end_hour: {}, start_hour: {}".format(end_hour, start_hour)

    hourDiff = end_hour - start_hour

    if start_minutes == end_minutes:
        return "{} hours".format(hourDiff)
    else:
        if end_minutes > start_minutes:
            minutesDiff = end_minutes - start_minutes
            timeDiff = "{} hours {} minutes".format(hourDiff,minutesDiff)
        else:
            minutesDiff = start_minutes - end_minutes
            hourDiff = hourDiff - 1
            minutesDiff = 60 - minutesDiff
            timeDiff = "{} hours {} minutes".format(hourDiff,minutesDiff)
        return timeDiff
