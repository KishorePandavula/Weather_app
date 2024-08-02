import tkinter as tk
from tkinter import ttk, messagebox
import requests

# Your OpenWeatherMap API key
API_KEY = "3524e0142a2912c8938422e013e61e9c"

def get_coordinates(location, api_key):
    """Fetch latitude and longitude from location name using OpenWeatherMap Geocoding API."""
    base_url = "http://api.openweathermap.org/data/2.5/weather"
    params = {
        "q": location,
        "appid": api_key
    }
    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()  # Raises an HTTPError for bad responses
        data = response.json()
        if data.get("cod") == 200:
            return data["coord"]["lat"], data["coord"]["lon"]
        else:
            messagebox.showwarning("Location Error", "Location not found.")
            return None, None
    except requests.exceptions.HTTPError as http_err:
        messagebox.showerror("HTTP Error", f"HTTP error occurred: {http_err}")
    except Exception as err:
        messagebox.showerror("Error", f"An error occurred: {err}")

def get_forecast(lat, lon, api_key):
    """Fetch 5-day weather forecast data from the OpenWeatherMap API."""
    base_url = "http://api.openweathermap.org/data/2.5/forecast"
    params = {
        "lat": lat,
        "lon": lon,
        "appid": api_key,
        "units": "metric"  # Use 'imperial' for Fahrenheit
    }
    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()  # Raises an HTTPError for bad responses
        return response.json()
    except requests.exceptions.HTTPError as http_err:
        messagebox.showerror("HTTP Error", f"HTTP error occurred: {http_err}")
    except Exception as err:
        messagebox.showerror("Error", f"An error occurred: {err}")

def update_forecast():
    """Update the weather forecast in the GUI."""
    location = location_entry.get()
    if not location:
        messagebox.showwarning("Input Error", "Please enter a location.")
        return

    lat, lon = get_coordinates(location, API_KEY)
    if lat is not None and lon is not None:
        forecast_data = get_forecast(lat, lon, API_KEY)
        if forecast_data and forecast_data.get("cod") == "200":
            output_text.delete(1.0, tk.END)  # Clear previous text
            for item in forecast_data["list"]:
                dt_txt = item.get("dt_txt")
                temperature = item["main"].get("temp")
                humidity = item["main"].get("humidity")
                description = item["weather"][0].get("description")
                wind_speed = item["wind"].get("speed")
                pressure = item["main"].get("pressure")
                
                # Append forecast data to text widget
                weather_info = (
                    f"Date & Time: {dt_txt}\n"
                    f"Temperature: {temperature}°C\n"
                    f"Humidity: {humidity}%\n"
                    f"Pressure: {pressure} hPa\n"
                    f"Wind Speed: {wind_speed} m/s\n"
                    f"Condition: {description.capitalize()}\n"
                    f"{'-' * 40}\n"
                )
                output_text.insert(tk.END, weather_info)
        else:
            output_text.delete(1.0, tk.END)
            output_text.insert(tk.END, "Forecast data not available.")

# GUI setup
root = tk.Tk()
root.title("Weather Forecast App")
root.geometry("600x600")

# Create and place the location label and entry
location_label = tk.Label(root, text="Location (City):")
location_label.pack(pady=5)
location_entry = tk.Entry(root, width=30)
location_entry.pack(pady=5)

# Create and place the button to get the forecast
get_forecast_button = tk.Button(root, text="Get Forecast", command=update_forecast, font=("Arial", 12))
get_forecast_button.pack(pady=10)

# Create and place the text widget to display forecast data
output_text = tk.Text(root, wrap=tk.WORD, height=20, width=70)
output_text.pack(pady=10)

# Run the GUI event loop
root.mainloop()
