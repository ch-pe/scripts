import urllib.request
import caldav
import passwordsAndStuff

# preparation - print to cmd or log to file
logfile = "spaceweatherToCalendar.log" # empty string for cmd printing
def log(text):
    if logfile == '':
        print(text)
    else:
        with open(logfile, 'a') as f:
            f.write(str(text)+'\n')
        #end open file
    #end if/else
#end definition

log("\n\nspaceweather copy script, v1.0")


months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
          'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

space_weather_url = "https://services.swpc.noaa.gov/text/3-day-forecast.txt"
log("opening " + space_weather_url)
page = urllib.request.urlopen(space_weather_url)
answer = str(page.read())
log(answer)

tableBlock = answer.split("\\n\\n")[3]
#print (tableBlock)
table = [i.split() for i in tableBlock.split('\\n')]

#todo: will need to change this at some point *shrug*
year = "2023"

# loop over days
entries = []
days = [table[0][1],table[0][3],table[0][5]]

for day_index, day in enumerate(days):
    month = str(months.index(table[0][day_index*2]) + 1).rjust(2,"0")
    for time_index in range(8):
        Kp_index = table[time_index + 1][day_index + 1]
        start_time = str(time_index * 3).rjust(2,"0")
        end_time = str((time_index + 1) * 3 - 1).rjust(2,"0") # idea is to go up to 2:59
        log("On "+year+"-"+month+"-"+day+", between " +
            start_time + ":00 UTC and " + end_time +
            ":59 UTC, the expected Kp_index is " + Kp_index)
        entries.append([year,month,day,start_time, end_time,Kp_index])
        # create a calendar entry, append to list
    #end loop times
#end loop days

# function to create events
def new_calendar_string(year, month, day, start_time, end_time, Kp_index):
    # I'm open for suggestions for better ways of doing this
    dateString = year + month + day

    # begin event
    vevent  = "BEGIN:VEVENT\n"
    vevent += "CREATED:20230321T195612Z\n"
    vevent += "DTSTAMP:20230321T195612Z\n"
    vevent += "LAST-MODIFIED:20220301T112233Z\n"
    vevent += "UID:" + dateString + "T" + start_time + "0000Z\n"
    vevent += "DTSTART:"+dateString+"T" + start_time + "0000Z\n"
    vevent += "DTEND:"  + dateString+"T" + end_time + "5900Z\n"
    vevent += "STATUS:CONFIRMED\n"
    vevent += "SUMMARY:" + Kp_index + "\n"
    vevent += "END:VEVENT\n"

    return(vevent)

## calDav preparation
url=passwordsAndStuff.calendarUrl()
username=passwordsAndStuff.calendarUsername()
password=passwordsAndStuff.calendarPassword()

#get the calendar
with caldav.DAVClient(url=url, username=username, password=password) as client:
    cal = client.calendar(url=url)
    for [year,month,day,start_time, end_time,Kp_index] in entries:
        cal.save_event(new_calendar_string(year,month,day,start_time, end_time,Kp_index))

#get a second calendar for only the high values
url=passwordsAndStuff.calendar2Url()
with caldav.DAVClient(url=url, username=username, password=password) as client:
    cal = client.calendar(url=url)
    for [year,month,day,start_time, end_time,Kp_index] in entries:
        if (float(Kp_index) >= 5):
            cal.save_event(new_calendar_string(year,month,day,start_time, end_time,Kp_index))
