from __future__ import print_function
from __future__ import absolute_import
from __future__ import unicode_literals

import calendar

from collections import defaultdict

from dateutils.dateutils import *
from dataaccess.utils import get_data_store
from actions.utils import reportingutils
def action_calview(colorizer, month):
    print('Displaying all entries for month ', colorizer.yellow(month), ' grouped by day:', sep='')
    
    report = generate_day_based_report()
    year=2019
    month_cal = calendar.monthcalendar(year,int(month))
    
    print("+--------------------------+--------------------------+--------------------------+--------------------------+--------------------------+")
    print("|         Monday           |         Tuesday          |         Wednesday        |         Thursday         |           Friday         |")
    print("+--------------------------+--------------------------+--------------------------+--------------------------+--------------------------+")
    for week in range(len(month_cal)):
        weekdays = month_cal[week]
        #skip empty weeks completely
        if weekdays[0] == 0 and weekdays[4] == 0:
            continue
        print("",  end="|")
        for day_index in range(len(weekdays)-2):
            day_cell_header=""
            if weekdays[day_index] != 0:
                day_cell_header=" "+ str(year)+"-"+month.zfill(2)+"-"+str(weekdays[day_index]).zfill(2)
            print(day_cell_header.ljust(26, ' '),  end="|")
        print()
        print("+--------------------------+--------------------------+--------------------------+--------------------------+--------------------------+")
        print_week_activity(weekdays,  5,  report,  year,  month)
        #print("WEEK DONE")
        print("+--------------------------+--------------------------+--------------------------+--------------------------+--------------------------+")
        

def print_week_activity(current_week,  height_in_rows,  report,  year,  month):
   for curr_row in range(height_in_rows):
       print_activity_at_index(curr_row,  current_week, report,  year,  month)
       print("") #one week row done

def print_activity_at_index(curr_row,  current_week,  report,  year,  month):
    print("",  end="|")    
    for day_index in range(len(current_week)-2):
        if current_week[day_index] == 0:
            print("".rjust(26, ' '),  end="|")
        else:
            activity_str =  get_activity(report,  curr_row, current_week[day_index],  year,  month)
            print(activity_str.rjust(26, ' '),  end="|")

def get_activity(report,  curr_row,  day_key,  year,  month):
        report_key=str(year)+"-"+month.zfill(2)+"-"+str(day_key).zfill(2)
        try:
            activity_dict = report[report_key]
            if curr_row < len(list(activity_dict)):
                activity_key = list(activity_dict)[curr_row]
                activity_duration = report[report_key][activity_key]
                return activity_key + " : " + format_time(activity_duration) + " "
        except:
            return ""
        return ""
        
def print_current_day(current_day_dict):
    string_report=' '
    for activity in current_day_dict.iterkeys():
        curr_act_duration=current_day_dict[activity]
        string_report+=activity+":"+format_time(curr_act_duration)+";"
    return string_report

def generate_day_based_report():
    data = get_data_store().load()
    work = data['work']
    report=dict()
    for item in work:
        if 'end' in item:
            day = reportingutils.extract_day(item['start'])
            duration = parse_isotime(item['end']) - parse_isotime(item['start'])
            try:
                report[day]
            except KeyError:
                report[day] = defaultdict(lambda: timedelta())
            report[day][item['name']] += duration 
            #print ('report[', day,  "][", item['name'], "]=" ,  report[day][item['name']])
    return report

def format_time(duration_timedelta):
    return format_time_seconds(duration_timedelta.seconds)


def format_time_seconds(duration_secs ):
    hours, rem = divmod(duration_secs, 3600)
    mins, secs = divmod(rem, 60)
    formatted_time_str = str(hours).rjust(2, str('0')) + ':' + str(mins).rjust(2, str('0'))
    return formatted_time_str
    
