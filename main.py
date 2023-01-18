# -*- coding: utf-8 -*-
import math
import tkinter as tk
import requests
import matplotlib.pyplot as plot
import tkinter.font as font
from tkinter import messagebox
from PIL import Image,ImageTk
import customtkinter
import pyautogui
import datetime
#from datetime import datetime

#Global Variables
Width, Height = pyautogui.size()
WIDTH = Width // 3
HEIGHT = Height // 3
#Setup Window
root=tk.Tk()
#Arrays for weather
temps = []
dates = []
#Tkinter variables
current_value = tk.IntVar()
current_value.set(1)
entry_text = tk.StringVar()
entry_text.set('')

def get_weather(city):
    #Empty weather data arrays
    temps.clear()
    dates.clear()
    try:
        #Update city label
        display_forecast.configure(text=get_current_value_day_forecast(city))
        num_rot=0
        #Clear weather display
        display.config(state='normal')
        display.delete(1.0,"end")

        #Get weather data from website
        weather_key='d1263330ca114cf770bddd71819f87a5'
        url='https://api.openweathermap.org/data/2.5/forecast'
        params = {'APPID': weather_key, 'q': city, 'units': 'metric'}
        response=requests.get(url,params=params)
        data=response.json()
        temp_list=data['list']
        output=''
        time_stamp=''
        for details in temp_list:
            test_dt = details['dt_txt']
            test_date_spliced = test_dt.rsplit(' ', 1)
            test_date=test_date_spliced[0]
            #This logic tracks dates for day range
            if test_date !=time_stamp:
                num_rot+=1

            if num_rot<current_value.get()+1:
                dt = details['dt_txt']
                date_spliced = dt.split()
                time_stamp=date_spliced[0]
                date_arr=time_stamp.split('-')
                time_arr=dt.split()
                #Change 24 hr time to 12 hr
                clock_time = datetime.datetime.strptime(time_arr[1][:-3], "%H:%M")

                dt_new=datetime.date(int(date_arr[0]), int(date_arr[1]), int(date_arr[2])).strftime("%b %d %Y")+" "+clock_time.strftime("%I:%M %p")

                #Set up graph
                plotdt = dt.replace(':00', '')
                plotdt = plotdt.split('-')
                plotdt = '/'.join(plotdt[1:])
                dates.append(plotdt)

                #Get weather api data
                temp = str(details['main']['temp'])
                temps.append(float(temp))
                feels_like = str(details['main']['feels_like'])
                pressure = str(details['main']['pressure'])
                humidity = str(details['main']['humidity'])
                # main= details['weather'][0]['main']
                description = str(details['weather'][0]['description'])

                #Setup output data
                output += '%12s%10s%20s%20s%26s%29s' % (
                dt_new, str(math.trunc(float(temp))) + chr(176) + "C", str(math.trunc(float(feels_like))) + chr(176) + "C", pressure + "Pa", humidity + "g.m⁻³", description)

                output += '\n'

        #Dont allow user to edit data display
        display.insert(1.0, output)
        display.config(state='disabled')

        city_title=entry_text.get()
    except:
        messagebox.showwarning("Unknown City", "Please enter a valid city.")
        entry_text.set("")
    #Error Checking
    # except Exception as e:
    #     print(e)
    #     entry_text.set('')

#draw graph using weather data
def draw_graph(output,dates,temps,city):
    #Create Graph
    fig = plot.gcf()
    fig.set_size_inches(15.5, 10.5)
    plot.clf()
    #string=chr(176)+"C"
    #my_new_list = [str(math.trunc(float(x))) + string for x in temps]
    #list2 = list(map(lambda orig_string: str(orig_string) + string, temps))

    #Plot data
    plot.plot(dates, temps)
    plot.xticks(dates[::2], rotation=70)

    #Customize Graph
    plot.suptitle(f'{current_value.get()} Day Temperature Graph for {city.capitalize()}')
    #fig.canvas.set_window_title('Temperature Graph')
    fig.canvas.manager.set_window_title('Temperature Graph')
    plot.xlabel = 'Time'
    plot.ylabel = 'Temperature'
    plot.show()

#Resizeing images, for background
def resize_image(event):
    new_width = event.width
    new_height = event.height
    #print(new_height,new_width)
    image = img_copy.resize((new_width, new_height))

    background_image = ImageTk.PhotoImage(image)
    background_label.configure(image =background_image)
    background_label.image=background_image

#clear data fields
def clear_fields():
    entry_text.set('')
    display.config(state='normal')
    display.delete(1.0, "end")
    display.config(state='disabled')
    get_current_value_day_forecast('')
    display_forecast.configure(text='{: .0f} Day Forecast'.format(current_value.get()))
    #display_forecast.setvar('{: .0f} Day Forecast'.format(current_value.get()))

def get_current_value_day_range():
    return 'Day Range: {: .0f}'.format(current_value.get())

def get_current_value_day_forecast(city):
    return city.capitalize()+'{: .0f} Day Forecast'.format(current_value.get())

def slider_changed(event):
    display_range.configure(text=get_current_value_day_range())

#settup main page
canvas =tk.Canvas(root,height=0,width=800)
root.title('Weather App')
root.geometry("1920x1080")
canvas.pack()
main_image=Image.open('cloudy_sky.jpg')
img_copy=main_image.copy()

#create fonts
font_1 = font.Font(family="Helvetica",size=15)
font_2 = font.Font(family="Sitka Banner",size=20)

#Setup background with image, bind image to resize function
background_image=ImageTk.PhotoImage(main_image)
background_label=tk.Label(root,image=background_image)
background_label.pack(fill='both',expand='yes')
background_label.bind('<Configure>',resize_image)


frame=tk.Frame(root,bg='#80c1ff',bd=5)
frame.place(relx=0.5,rely=0.1,relwidth=0.75,relheight=0.1,anchor='n')

entry=tk.Entry(frame,font=font_2,textvariable=entry_text)
entry.place(relwidth=0.65,relheight=1)


button_1 = customtkinter.CTkButton(master=frame,text="Get Weather",font=("Sitka Banner",20,"bold"),text_color="black",command=lambda: get_weather(entry.get()))
button_1.place(relx=0.66,relwidth=0.15,relheight=1)




button_2 = customtkinter.CTkButton(master=frame,text="Weather Graph",font=("Sitka Banner",20,"bold"),text_color="black",command=lambda:draw_graph(entry.get(),dates,temps,city=entry_text.get()))
button_2.place(relx=0.82,relwidth=0.16,relheight=1)


#For displaying Weather Data
lower_frame=tk.Frame(root,bg='#80c1ff',bd=10)
lower_frame.place(relx=0.5,rely=0.35,relwidth=0.75,relheight=0.6,anchor='n')

display=tk.Text(lower_frame,font=font_1,background='#80c1ff')
display.place(relwidth=1,relheight=0.8,rely=0.2)


text_legend = customtkinter.CTkLabel(master=lower_frame,text='%10s%30s%25s%25s%25s%40s' % ('Date', 'Temp(°C)', 'Feels Like(°C)', 'Pressure(Pa)', 'Humidity(g.m⁻³)', 'Description'),
                                      font=("Roboto Medium",-15,"bold"))  # font name and size in px
text_legend.place(relwidth=1,relheight=0.1,relx=0.00001,rely=0.1)


slider_frame=tk.Frame(root,bg='#80c1ff',bd=10)

button_3 = customtkinter.CTkButton(master=slider_frame,text="Clear",font=("Sitka Banner",20,"bold"),text_color="black",command=lambda:clear_fields())
button_3.place(relx=0.47,rely=0.01,relwidth=0.16,relheight=1)

slider_frame.place(relx=0.5,rely=0.2,relwidth=0.75,relheight=0.15,anchor='n')
slider = customtkinter.CTkSlider(master=slider_frame,  from_=1,
                                                to=5,
                                                number_of_steps=4,command=slider_changed,
                                                variable=current_value)

slider.place(relwidth=0.3,relheight=0.3,relx=0.67,rely=0.5)

display_range = customtkinter.CTkLabel(master=slider_frame,text=get_current_value_day_range(),
                                      font=("Roboto Medium",-18))  # font name and size in px

display_range.place(relwidth=0.17,relheight=0.4,relx=0.74,rely=0.1)

display_forecast = customtkinter.CTkLabel(master=slider_frame,text=get_current_value_day_forecast(city=entry_text.get()),
                                      font=("Franklin Gothic Demi",-18))  # font name and size in px

display_forecast.place(relwidth=0.30,relheight=0.5,relx=0.07,rely=0.3)

root.mainloop()
