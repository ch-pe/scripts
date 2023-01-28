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

#todo: will need to change this at some point *shrug*
year = 2023

# loop over days
days = [int(table[0][1]),int(table[0][3]),int(table[0][5])]

for day_index, day in enumerate(days):
    month = months.index(table[0][day_index*2]) + 1
    for time_index in range(8):
        Kp_index = table[time_index + 1][day_index + 1]
        start_time = time_index * 3
        end_time = (time_index + 1) * 3
        print("On "+str(year)+"-"+str(month)+"-"+str(day)+", between " +
              str(start_time) + "UTC and " + str(end_time) +
              "UTC, the expected Kp_index is " + Kp_index)


