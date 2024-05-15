# Names and Id's
# Muhammed Burak Zeren - 20200601063
# Sinem Yeşil - 20200601061
# Elif İlkay Özkan - 20200601041

# Import part
from tkinter import ttk, messagebox
import requests
from bs4 import BeautifulSoup
from PIL import ImageTk, Image
import tkinter as tk
from datetime import date
from unidecode import unidecode

# Extensions corresponding to cities for the continuation of the url
cities = {
    "İzmir": "fe1876e1fd0d8cda3894eb7797379983e6591d215dbcd0279bc3181a8cf677f5",
    "Manisa": "ca1734833d25fb15fd8de8c52fae8352c220c7200a6414348b48b4be5bebbead",
    "Aydın": "311a74394ae5945f829ccc05285753af2c4c86a4d48121a905c0f066a314959d",
    "Denizli": "49a35992abb4873313d933a95ffbd42c6635f3625a99f1eb13c74a07847d5cdd",
    "Muğla": "7cb1814c2810b68458e9e07f35d21a270803a6e3b3b63892332f7c65d684d2e2",
    "Afyonkarahisar": "87ded05f9804f0a3868ef23a6903bd0b36b689284af2f2fa17ef03125d08be84",
    "Kütahya": "7f6fa23cdea85c6981fbac907239aa5158e0b5df73bb7250206ce9d8aa63dfda",
    "Uşak": "1503c10002c90b67560d9a23d837ee34402d3cffce4e207b0b63713ec2ebf174"
}
# Extensions corresponding to upcoming days of cities for the continuation of the url
citiesUpcomingDays = {
    "İzmir": "38.420;27.143",
    "Manisa": "38.616;27.426",
    "Aydın": "37.842;27.835",
    "Denizli": "37.772;29.084",
    "Muğla": "37.217;28.363",
    "Afyonkarahisar": "38.758;30.535",
    "Kütahya": "39.421;29.981",
    "Uşak": "38.681;29.403"
}
# pictures that will appear according to the weather conditions
weatherImage = {
    "partly": "weatherImage.jpeg",
    "cloudy": "cloudy.jpeg",
    "rain": "rainy.jpeg",
    "shower": "rainy.jpeg",
    "sunny": "sunny.jpeg"
}

# first opened gui
master = tk.Tk()
master.title("Weather App")
master.config(bg="white")
box_frame = ttk.Frame(master, padding="20")
box_frame.grid(row=0, column=0)

# Some default variables are defined at the highest level so that they can be used in many functions
newTodayTemperature = 0
temperatureToday = 0
dayTemp = 0
nightTemp = 0
newTemperatureTomorrow = 0
newTemperatureTomorrowNight = 0
newTemperatureAfterTomorrow = 0
newTemperatureAfterTomorrowNight = 0
weatherPrediction = ""
dayAndNight = ""
predict = ""
log = ""
tempInfoA = []
valueCity = []
holder = []
mainDict = dict()
flag = True
flag2 = True

# Almost everything about weather is rendered in below function
def weatherInformation(log):
    # Use of global variables
    global flag
    global flag2
    global valueCity
    global tempInfoA
    global mainDict
    global holder
    flag = True

    # Txt is checked to see if there is a default value given by the user
    file_path = "Settings.txt"
    try:
        with open(file_path, 'r') as file:
            for line in file:
                line = line.strip()
                if line:
                    tempInfo = line.split()
                    tempInfoA.append(tempInfo)
                    count = 2
                    for i in range(0,len(tempInfoA)):
                        if tempInfoA[i][count] not in valueCity:
                            valueCity.append(tempInfoA[i][count])
                            count += count
                    for key in cities.keys():
                        for insideFile in tempInfo:
                            if unidecode(key) == str(insideFile):
                                if key not in holder:
                                    holder.append(key)
                                elif len(valueCity) != len(holder):
                                    holder.append(key)

    except FileNotFoundError:
        pass

    # Txt contents are converted to dictionary
    mainDict = {k: v for k,v in zip(holder, valueCity)}


    # Since two different sites are used, the common point is also merged
    cityName =""
    windHolder = ""
    for key,value in cities.items():
        if value == log:
            for keyWind in citiesUpcomingDays.keys():
                if key == keyWind:
                    cityName = keyWind
                    windHolder = citiesUpcomingDays[keyWind]
    global predict

    # A new box related to the selected city opens
    popup_box = tk.Toplevel()
    popup_box.config(bg="#ffcccc")

    # For all information about weather except wind speed
    url = "https://weather.com/en-GB/weather/today/l/"

    # Function that converts Celsius to Fahrenheit
    def celsius_to_fahrenheit(celsius):
        fahrenheit = (celsius * 9 / 5) + 32
        return str(fahrenheit) + "°F"

    # Uses the celsius_to_fahrenheit function and creates a Celsius Fahrenheit dropdown toggle
    def changeTempreture(*args):
        global flag
        selectedItem = dropVar.get()
        if str(selectedItem) == "Fahrenheit":
            temperatureLabel.config(text=celsius_to_fahrenheit(newTodayTemperature))
            dayAndNightLabel.config(text=celsius_to_fahrenheit(dayTemp) +" / "+
                                         celsius_to_fahrenheit(nightTemp))
            tomorrowTemperatureLabel.config(text=celsius_to_fahrenheit(newTemperatureTomorrow) + " / "
                             + celsius_to_fahrenheit(newTemperatureTomorrowNight))
            tomorrowAfterTemperatureLabel.config(text=celsius_to_fahrenheit(newTemperatureAfterTomorrow) + " / "+
            celsius_to_fahrenheit(newTemperatureAfterTomorrowNight))

        else:
            if flag:
                temperatureLabel.config(text=temperatureToday)
            else:
                temperatureLabel.config(text=str(newTodayTemperature) + "°")
            dayAndNightLabel.config(text=str(dayTemp)+"° / "+str(nightTemp)+"°")
            tomorrowTemperatureLabel.config(text=str(newTemperatureTomorrow) + "° / " +
                                                 str(newTemperatureTomorrowNight) + "°")
            tomorrowAfterTemperatureLabel.config(text=str(newTemperatureAfterTomorrow) + "° / " +
                                                      str(newTemperatureAfterTomorrowNight) + "°")

    # Weather information related to the city, excluding wind speed, using the url
    def getWeather():
        # Use of global variables
        global flag
        global flag2
        global temperatureToday
        global newTodayTemperature
        global dayTemp
        global nightTemp
        global dayAndNight
        global predict
        global weatherPrediction
        page = requests.get(url+log)
        soup = BeautifulSoup(page.content, "html.parser")
        location = soup.find('h1', class_="CurrentConditions--location--1YWj_").text
        popup_box.title(location)
        locationHolder = location.split()
        locationName = str(locationHolder[0][:-1])
        if flag2:
            for key, value in mainDict.items():
                if locationName == key:
                    newTodayTemperature = int(value)
                    flag = False
                    temperatureLabel.config(text=str(newTodayTemperature) + "°")
        if flag:
            temperatureToday = soup.find('span', class_="CurrentConditions--tempValue--MHmYY").text
        weatherPrediction = soup.find('div', class_="CurrentConditions--phraseValue--mZC_p").text
        dayAndNight = soup.find('div', class_="CurrentConditions--tempHiLoValue--3T1DG").text
        if flag:
            newTodayTemperature = int(temperatureToday[:-1])
        predict = weatherPrediction
        result = dayAndNight.split()
        dayTemp = int(result[1][:-1])
        nightTemp = int(result[4][:-1])
        locationLabel.config(text=location)
        if flag:
            temperatureLabel.config(text=temperatureToday)
        weatherPredictionLabel.config(text=weatherPrediction)
        dayAndNightLabel.config(text=str(dayTemp)+"° / "+str(nightTemp)+"°")

    # Shows the city's upcoming days speed via another url
    def upcomingDays():
        # Use of global variables
        global newTemperatureTomorrow
        global newTemperatureTomorrowNight
        global newTemperatureAfterTomorrowNight
        global newTemperatureAfterTomorrow
        url = f"https://www.ventusky.com/{windHolder}"
        responsee = requests.get(url)
        soupp = BeautifulSoup(responsee.content, 'html.parser')
        temperatureTomorrow = soupp.find('a', onclick="return Detail.changeForecast(1, 1, 7)").text.split()
        temperatureTomorrowNight = soupp.find('b', id="t_3").text.split()
        temperatureAfterTomorrow = soupp.find('a', onclick="return Detail.changeForecast(2, 1, 7)").text.split()
        temperatureAfterTomorrowNight = soupp.find('b', id="t_6").text.split()
        windSpeed = soupp.find('div', class_="info_table").text.split()
        resultSet = windSpeed[3]+windSpeed[4]
        if resultSet == "forSensitive":
            windSpeed = soupp.find('span', id="vs_9").text
            resultSet = windSpeed
        windSpeedLabel.config(text="Wind Speed : "+resultSet)
        newTemperatureTomorrow = int(temperatureTomorrow[1])
        newTemperatureTomorrowNight = int(temperatureTomorrowNight[0])
        newTemperatureAfterTomorrow = int(temperatureAfterTomorrow[1])
        newTemperatureAfterTomorrowNight = int(temperatureAfterTomorrowNight[0])
        tomorrowTemperatureLabel.config(text=str(newTemperatureTomorrow) + "° / " + str(newTemperatureTomorrowNight) + "°")
        tomorrowAfterTemperatureLabel.config(text=str(newTemperatureAfterTomorrow) + "° / " +
                                                  str(newTemperatureAfterTomorrowNight) + "°")

    # Erase default variable entered by user
    def eraseFile():
        # Use of global variables
        global mainDict
        global flag
        global flag2
        # It will empty txt and dictionary
        file_path = "Settings.txt"
        try:
            with open(file_path, 'w') as file:
                mainDict = {}
                flag = True
                flag2 = False
                if temperatureToday[:-1] == 0:
                    temperatureLabel.config(text="Loading..")
                temperatureLabel.config(text=temperatureToday)
        except:
            pass

    # Allows the default temperature to be entered in the city selected by the user
    def open_popup_box():
        # Opens a new box for the user
        popup_box2 = tk.Toplevel()
        popup_box2.title("User Preferences")
        popup_box2.config(bg="#ffcccc")
        width = 300
        height = 200
        popup_box2.geometry(f"{width}x{height}")
        holderArea = tk.Label(popup_box2, bg="#ffcccc" ,pady=15)
        holderArea.pack()
        city_label = tk.Label(popup_box2, text="Selected City :", bg="#ffcccc")
        city_label.pack()
        text_box = tk.Text(popup_box2, width=15, height=1,padx=2)
        text_box.pack()
        text_box.insert(tk.END,cityName)
        temperature_user = tk.Label(popup_box2,text="Enter Temperature :", bg="#ffcccc")
        temperature_user.pack()
        temperature_user_entry = tk.Entry(popup_box2)
        temperature_user_entry.pack()

        # When you click the Save button, it directs you to the add_to_file function to be added to the file.
        ok_button = tk.Button(popup_box2, text="Save",command=lambda: add_to_file(cityName,temperature_user_entry))
        ok_button.pack(side=tk.LEFT, padx=10)
        buttonBack2 = ttk.Button(popup_box2, text="Back", command=popup_box2.destroy)
        buttonBack2.pack(side=tk.RIGHT, padx=10)

    # The value entered by the user is added to the txt
    # If there is no txt this function also create a txt
    def add_to_file(cityName,temperature_user_entry):
        global newTodayTemperature
        global flag
        # Thanks to unidecode, Turkish characters in the city can be avoided
        cityNameValue = unidecode(cityName)
        temperaturUserEntryValue = temperature_user_entry.get()
        # Check is there a txt and add informations into the txt
        file_path = "Settings.txt"
        try:
            file = open(file_path, 'r')
            file.close()
        except FileNotFoundError:
            messagebox.showinfo("File Station", "The file is creating...")
        finally:
            flag = False
            with open(file_path, 'a') as file:
                newTodayTemperature = int(temperaturUserEntryValue)
                file.write(f"{cityNameValue} - {temperaturUserEntryValue}\n")
                messagebox.showinfo("Information",f"{cityNameValue} and {temperaturUserEntryValue}° successfully uploaded !")
                temperatureLabel.config(text=temperaturUserEntryValue+"°")

    # Receives the day's information from the computer and determines tomorrow and the day after tomorrow
    today = date.today()
    execDate = str(today).split("-")
    holderDay = execDate[2]
    day = int(execDate[2])
    tomorrow = str(day + 1)
    afterTomorrow = str(day + 2)
    dateToday = holderDay + "/" + execDate[1] + "/" + execDate[0]
    dateTomorrow = tomorrow + "/" + execDate[1] + "/" + execDate[0]
    dateAfterTomorrow = afterTomorrow + "/" + execDate[1] + "/" + execDate[0]

    # Gui design, label parts
    dateTodayLabel = tk.Label(popup_box,font=("Calibri bold", 15), bg="#ffcccc")
    dateTodayLabel.config(text=f"{dateToday}")
    dateTodayLabel.grid(row=2, sticky='W', padx=10,pady=10)
    dateTomorrowLabel = tk.Label(popup_box,font=("Calibri bold", 15), bg="#ffcccc")
    dateTomorrowLabel.config(text=f"{dateTomorrow}")
    dateTomorrowLabel.grid(row=2, padx=10,pady=10)
    dateAfterTomorrowLabel = tk.Label(popup_box,font=("Calibri bold", 15), bg="#ffcccc")
    dateAfterTomorrowLabel.config(text=f"{dateAfterTomorrow}")
    dateAfterTomorrowLabel.grid(row=2,sticky='E',padx=25,pady=10)
    tomorrowTemperatureLabel = tk.Label(popup_box, font=("Calibri bold", 15), bg="#ffcccc")
    tomorrowTemperatureLabel.grid(row=3, padx=10, pady=10)
    tomorrowAfterTemperatureLabel = tk.Label(popup_box, font=("Calibri bold", 15), bg="#ffcccc")
    tomorrowAfterTemperatureLabel.grid(row=3, sticky='E', padx=34, pady=10)
    locationLabel = tk.Label(popup_box, font=("Calibri bold", 23), bg="#ffcccc")
    locationLabel.grid(row=0, sticky='N', padx=200)
    temperatureLabel = tk.Label(popup_box, font=("Calibri bold", 25), bg="#ffcccc")
    temperatureLabel.grid(row=1, sticky="W", padx=43)
    windSpeedLabel = tk.Label(popup_box, font=("Calibri bold", 15), bg="#ffcccc")
    windSpeedLabel.grid(row=4, padx=20,pady=10)
    weatherPredictionLabel = tk.Label(popup_box, font=("Calibri bold", 15), bg="#ffcccc")
    weatherPredictionLabel.grid(row=4, sticky="W", padx=10)
    dayAndNightLabel = tk.Label(popup_box, font=("Calibri bold", 15), bg="#ffcccc")
    dayAndNightLabel.grid(row=3, sticky='W', padx=20, pady=10)
    buttonBack = ttk.Button(popup_box,text="Back", command=popup_box.destroy)
    buttonBack.grid(row=4, column=0, sticky='E', padx=10, pady=5)
    buttonReset = ttk.Button(popup_box, text="Reset", command=eraseFile)
    buttonReset.grid(row=4, column=0, sticky='E', padx=90, pady=5)
    buttonUserPref = ttk.Button(popup_box, text="User Preference", command=open_popup_box)
    buttonUserPref.grid(row=1, column=0, sticky='S', padx=10, pady=30,)
    dropVar = tk.StringVar()
    dropVar.trace('w', changeTempreture)
    dropdown2 = ttk.Combobox(popup_box,textvariable=dropVar)
    dropdown2['values'] = ["Celsius"] + ["Fahrenheit"]
    dropdown2.current(0)
    dropdown2.grid(row=1, column=0, columnspan=3, padx=0, pady=30)
    getWeather()
    upcomingDays()

    # The processing of the picture to be put forward according to the weather
    holderImage = "weatherImage.jpeg"
    for key in weatherImage.keys():
        result = predict.lower()
        if result.find(key) > 0:
            holderImage = weatherImage[key]

    img = Image.open(f"{holderImage}")
    img = img.resize((130, 130))
    img = ImageTk.PhotoImage(img)
    # Img Label
    tk.Label(popup_box,image=img, bg="white").grid(row=1, sticky='E',padx=10)

    # The necessary logic to convert the temperature values and
    # update the displayed weather information accordingly
    temperatureLabel.after(6000,getWeather)
    dayAndNightLabel.after(6000,getWeather)
    popup_box.update()
    # Creates an infinite loop to be used until closed
    popup_box.mainloop()

# Used to declare the log that will go to weatherInformation
def updateTextBox(*args):
    selectedItem = dropdown_var.get()
    global log
    for key in cities.keys():
        if str(selectedItem) == 'City':
            break
        if str(key) == str(selectedItem):
            log=cities[key]
            break

# Created to be sent to use the selected city
def getWeatherTable():
    # Error section created in case the user chooses city
    if dropdown_var.get() == 'City':
        messagebox.showwarning("Choose City", "Please choose one city!")
    else:
        weatherInformation(log)

# The label created for the city selection part
selectCity = tk.Label(master, font=("Calibri bold", 12))
selectCity.grid(row=0, sticky='NW', padx=20)
selectCity.config(text="Select City : ")
dropdown_var = tk.StringVar()
dropdown_var.trace('w', updateTextBox)
dropdown = ttk.Combobox(box_frame, textvariable=dropdown_var)
dropdown['values'] = ["City"] + ["İzmir"] + ["Manisa"] + ["Aydın"] + ["Denizli"] + ["Muğla"] + [
        "Afyonkarahisar"] + ["Kütahya"] + ["Uşak"]
dropdown.current(0)
dropdown.grid(row=0, column=0, columnspan=3, padx=0, pady=10)
button1 = ttk.Button(box_frame, text="Select", command=getWeatherTable)
button1.grid(row=2, column=0, padx=30, pady=5)

# Creates an infinite loop to be used until closed
master.mainloop()