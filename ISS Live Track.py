from tkinter import Canvas, PhotoImage, Tk
import requests


# --------------------- GET ISS LOCATION ---------------------- #

def distance():
    response = requests.get(url="https://api.wheretheiss.at/v1/satellites/25544")
    response.raise_for_status()
    data = response.json()

    long = float(data["longitude"]) + 180  # It will start from 0, to make calculation easier.
    lat = float(data["latitude"]) + 90

    # long coordinates = 3-363
    # lat coordinates = 3-183

    # 532/180 = 2.955555555555556  > The rate to convert longitude to x coordinate
    # 183/lat = x > 531 - 531/x  > The rate to convert latitude to y coordinate

    x = round(long * 2.955555555555556)
    if lat == 0:  # In case zero division error if lat is exactly 0, very low chance though.
        y = 3
    else:
        lat_rate = 180/lat
        y = 531 - round(531 / lat_rate)
    canvas.moveto(iss, x, y)

    window.after(10000, distance)


# ----------------------- WINDOW SETUP ------------------------ #

window = Tk()
window.config(padx=10, pady=10, bg="black")
window.geometry("1100x564+230+130")
world = PhotoImage(file="World.png")
window.title("Live ISS Location")

canvas = Canvas(width=1080, height=544)
canvas.create_image(540, 272, image=world)
iss = canvas.create_oval(537, 268, 544, 275, fill="red", width=1)
# 3-1067 is the x coordinate range when the dot is on the edge.
# 3-531 is the y coordinate range when the dot is on the edge.

canvas.pack(expand=True)

distance()

window.mainloop()
