import urllib.request
import caldav
import passwordsAndStuff.py

# preparation - print to cmd or log to file
logfile = ''#"spaceweatherToCalendar.log" # empty string for cmd printing
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
year = 2023

# loop over days
entries = []
days = [int(table[0][1]),int(table[0][3]),int(table[0][5])]

for day_index, day in enumerate(days):
    month = months.index(table[0][day_index*2]) + 1
    for time_index in range(8):
        Kp_index = float(table[time_index + 1][day_index + 1])
        start_time = time_index * 3
        end_time = (time_index + 1) * 3 - 1 # idea is to go up to 2:59
        log("On "+str(year)+"-"+str(month)+"-"+str(day)+", between " +
            str(start_time) + ":00 UTC and " + str(end_time) +
            ":59 UTC, the expected Kp_index is " + str(Kp_index))
        entries.append([year,month,day,start_time,Kp_index])
        # create a calendar entry, append to list
    #end loop times
#end loop days


## calDav preparation
url=passwordsAndStuff.calendarUrl()
username=passwordsAndStuff.calendarUsername()
password=passwordsAndStuff.calendarPassword()

#get the calendar
with caldav.DAVClient(url=url, username=username, password=password) as client:
   cal = client.calendar(url=url)
   the_same_calendar.events()
# create events
