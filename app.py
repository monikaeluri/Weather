import tkinter as tk
from tkinter import messagebox
import requests
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt

API_KEY = "74943fa382de3423b71ec95f4c487143"  
BASE_URL = "http://api.openweathermap.org/data/2.5/weather"

root = tk.Tk()
root.title("Visual Weather App 🌦️")
root.geometry("900x600")
root.configure(bg="#e8f5e9")

tk.Label(root, text="Weather App with Graph 📊", font=("Helvetica", 20, "bold"), fg="green", bg="#e8f5e9").pack(pady=10)

search_frame = tk.Frame(root, bg="#e8f5e9")
search_frame.pack()
city_entry = tk.Entry(search_frame, font=("Helvetica", 14), width=30)
city_entry.grid(row=0, column=0, padx=10)
search_btn = tk.Button(search_frame, text="Search", font=("Helvetica", 12), command=lambda: get_weather(city_entry.get()), bg="#a5d6a7")
search_btn.grid(row=0, column=1)

output_frame = tk.Frame(root, bg="white", bd=2, relief="groove")
output_frame.pack(pady=20, fill=tk.BOTH, expand=True)

def get_weather(city):
    for widget in output_frame.winfo_children():
        widget.destroy()

    if not city:
        messagebox.showerror("Input Error", "Please enter a city name.")
        return

    params = {"q": city, "appid": API_KEY, "units": "metric"}
    response = requests.get(BASE_URL, params=params)
    data = response.json()

    if response.status_code != 200 or "main" not in data:
        messagebox.showerror("Error", f"City '{city}' not found.")
        return

    temp = data["main"]["temp"]
    humidity = data["main"]["humidity"]
    condition = data["weather"][0]["description"].title()

    tk.Label(output_frame, text=city.title(), font=("Helvetica", 24, "bold"), bg="white").pack(pady=10)

    info_frame = tk.Frame(output_frame, bg="white")
    info_frame.pack()

    tk.Label(info_frame, text=f"🌡 Temperature: {temp}°C", font=("Helvetica", 14), bg="white").grid(row=0, column=0, padx=30)
    tk.Label(info_frame, text=f"💧 Humidity: {humidity}%", font=("Helvetica", 14), bg="white").grid(row=0, column=1, padx=30)
    tk.Label(info_frame, text=f"🌥 Condition: {condition}", font=("Helvetica", 14), bg="white").grid(row=0, column=2, padx=30)

    # Simulated hourly temperature graph
    hours = ["12AM", "3AM", "6AM", "9AM", "12PM", "3PM", "6PM", "9PM"]
    temps = [temp - 3 + i for i in range(8)]

    fig, ax = plt.subplots(figsize=(8, 4))
    ax.plot(hours, temps, color="#ff9800", marker="o")
    ax.set_title("Hourly Forecast")
    ax.set_xlabel("Time of Day")  # Label for x-axis
    ax.set_ylabel("Temperature (°C)")  # Label for y-axis
    ax.grid(True)

    canvas = FigureCanvasTkAgg(fig, master=output_frame)
    canvas.draw()
    canvas.get_tk_widget().pack(pady=20)

root.mainloop()
