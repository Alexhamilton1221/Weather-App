# -*- coding: utf-8 -*-
import tkinter as tk
import requests
import matplotlib.pyplot as plot
import tkinter.font as font
from tkinter import messagebox
from PIL import Image,ImageTk


Height=650
Width=1200
root=tk.Tk()
temps = []
dates = []
def get_weather(city):
    temps.clear()
    dates.clear()
    try:
        display.delete(1.0,"end")
        weather_key='d1263330ca114cf770bddd71819f87a5'
        url='https://api.openweathermap.org/data/2.5/forecast'
        params = {'APPID': weather_key, 'q': city, 'units': 'metric'}
        response=requests.get(url,params=params)
        data=response.json()
        temp_list=data['list']
        output=''
        output += '%15s%25s%20s%15s%14s%20s' % ('Date', 'Temp(°C)', 'Feels Like(°C)', 'Pressure(Pa)', 'Humidity', 'Description')
        output += '\n--------------------------------------------------------------------------------------------------------------------------------------\n'

        for details in temp_list:
            dt=details['dt_txt']
            plotdt=dt.replace(':00','')
            plotdt=plotdt.split('-')
            plotdt='/'.join(plotdt[1:])

            dates.append(plotdt)

            temp=str(details['main']['temp'])
            temps.append(float(temp))
            feels_like=str(details['main']['feels_like'])
            pressure=str(details['main']['pressure'])
            humidity=str(details['main']['humidity'])
            #main= details['weather'][0]['main']
            description= str(details['weather'][0]['description'])
            output+='%20s%10s%20s%20s%20s%27s'%(dt,temp,feels_like,pressure,humidity,description)
            output+='\n'
        display.insert(1.0, output)

    except:
        messagebox.showwarning("Unknown City", "Please enter a valid city.")

def draw_graph(output,dates,temps):
    fig = plot.gcf()
    fig.set_size_inches(18.5, 10.5)
    plot.clf()
    plot.plot(dates, temps)
    plot.xticks(dates[::2], rotation=70)
    plot.suptitle('5 Day Temperature Graph')
    #fig.canvas.set_window_title('Temperature Graph')
    fig.canvas.manager.set_window_title('Temperature Graph')



    plot.xlabel = 'Time'
    plot.ylabel = 'Temperature'
    plot.show()
def resize_image(event):

    new_width = event.width
    new_height = event.height
    #print(new_height,new_width)
    image = img_copy.resize((new_width, new_height))

    background_image = ImageTk.PhotoImage(image)
    background_label.configure(image =background_image)
    background_label.image=background_image
canvas =tk.Canvas(root,height=0,width=800)
root.title('Weather App')
root.geometry("1920x1080")
canvas.pack()
main_image=Image.open('cloudy_sky.jpg')
img_copy=main_image.copy()
font_1 = font.Font(family="Helvetica",size=20)
font_2 = font.Font(family="Sitka Banner",size=20,weight='bold')
font_3 = font.Font(family="Sitka Banner",size=20)
font_4 = font.Font(family="Eccentric Std",size=20)
#Roman Modern
background_image=ImageTk.PhotoImage(main_image)
background_label=tk.Label(root,image=background_image)
background_label.pack(fill='both',expand='yes')
background_label.bind('<Configure>',resize_image)


frame=tk.Frame(root,bg='#80c1ff',bd=5)
frame.place(relx=0.5,rely=0.1,relwidth=0.75,relheight=0.1,anchor='n')

entry=tk.Entry(frame,font=font_4)
entry.place(relwidth=0.65,relheight=1)

button=tk.Button(frame,text="Get Weather",font=font_2,command=lambda:get_weather(entry.get()))
button.place(relx=0.66,relwidth=0.15,relheight=1)

button2=tk.Button(frame,text="Weather Graph",font=font_2,command=lambda:draw_graph(entry.get(),dates,temps))
button2.place(relx=0.82,relwidth=0.16,relheight=1)

lower_frame=tk.Frame(root,bg='#80c1ff',bd=10)
lower_frame.place(relx=0.5,rely=0.25,relwidth=0.75,relheight=0.6,anchor='n')

label= tk.Label(lower_frame)
label.place(relwidth=1,relheight=1)

display=tk.Text(lower_frame,height=10,font=font_1)
display.place(relwidth=1,relheight=1)

#display.config(state='disabled')

root.mainloop()