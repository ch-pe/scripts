import urllib.request

print("spaceweather copy script, v1.0")

# preparation
months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
          'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

space_weather_url = "https://services.swpc.noaa.gov/text/3-day-forecast.txt"
print("opening " + space_weather_url)
page = urllib.request.urlopen(space_weather_url)
answer = str(page.read())
print(answer)

tableBlock = answer.split("\\n\\n")[3]
#print (tableBlock)
table = [i.split() for i in tableBlock.split('\\n')]


#Day 1
year = 2023
month = months.index(table[0][0]) + 1
day = int(table[0][1])
time_start = 0 #UTC
time_end = 3 #UTC
Kp_index = table [1][1]

print ("On " + str(year) + "-" + str(month) + "-" + str(day) + " from "
    + str(time_start) + ":00:00 (UTC) to " + str(time_end)
    + ":00:00 (UTC) the expected Kp index is " + str(Kp_index))
