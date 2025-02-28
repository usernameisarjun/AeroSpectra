import numpy as np
from PIL import Image, ImageDraw, ImageFont
import tkinter as tk
from tkinter import filedialog
from datetime import datetime
import pandas as pd
import os

# Function to calculate Euclidean distance between two colors
def color_distance(c1, c2):
    return np.sqrt(np.sum((np.array(c1) - np.array(c2))**2))

# Function to map RGB values to NO2 concentrations using Euclidean distance
def rgb_to_no2(rgb):
    closest_color = min(color_to_no2.keys(), key=lambda color: color_distance(color, rgb))
    return color_to_no2[closest_color]

# Create a tkinter root window and hide it
root = tk.Tk()
root.withdraw()

# Ask the user to upload an image file
file_path = filedialog.askopenfilename(title="Select an image file", filetypes=[("Image files", ".jpeg;.jpg;.png;.bmp;*.tiff")])

# Load the selected image
image = Image.open(file_path)

# Convert the image to a numpy array
image_array = np.array(image)

# Example of manual RGB to NO2 mapping (you can modify this based on your image legend)
color_to_no2 = {
    (255, 0, 0): 100,    # Red corresponds to 100 µg/m³
    (0, 255, 0): 50,     # Green corresponds to 50 µg/m³
    (0, 0, 255): 10,     # Blue corresponds to 10 µg/m³
    (255, 255, 0): 75,   # Yellow corresponds to 75 µg/m³
    # Add more mappings as needed
}

# Initialize a list to store NO2 values
no2_values = []

# Iterate over each pixel in the image
for y in range(image_array.shape[0]):
    for x in range(image_array.shape[1]):
        # Get the RGB value at the current pixel
        rgb = tuple(image_array[y, x, :3])
        # Convert the RGB value to NO2 concentration
        no2_value = rgb_to_no2(rgb)
        # Add the NO2 value to the list
        no2_values.append(no2_value)

# Calculate the average NO2 concentration
average_no2 = np.mean(no2_values)

# Draw the average NO2 concentration on the image
draw = ImageDraw.Draw(image)

# Load a font that supports Unicode characters
font_path = "arial.ttf"  # Adjust the path to the font file if needed
font = ImageFont.truetype(font_path, size=24)

# Prepare the text to display
text = f"Avg NO₂: {average_no2:.2f} µg/m³"

# Position the text in the bottom-right corner
text_size = draw.textsize(text, font=font)
text_position = (image.width - text_size[0] - 10, image.height - text_size[1] - 10)
draw.text(text_position, text, font=font, fill=(255, 255, 255))

# Show the image with the average NO2 concentration
image.show()

# Ask the user to input the name of the place after displaying the image
place_name = input("Please enter the name of the place: ")

# Get the current date
current_date = datetime.now().strftime("%Y-%m-%d")

# Create a dictionary with the data to be saved
data = {
    "Place Name": [place_name],
    "Date": [current_date],
    "Average NO2 Concentration (µg/m³)": [average_no2]
}

# Convert the dictionary to a DataFrame
df = pd.DataFrame(data)

# Specify the file name
file_name = "no2_concentration_data.xlsx"

# Try to append the data to the existing Excel file, or create a new one if it doesn't exist
try:
    existing_df = pd.read_excel(file_name)
    df = pd.concat([existing_df, df], ignore_index=True)
except FileNotFoundError:
    pass

# Save the DataFrame to an Excel file
df.to_excel(file_name, index=False)

# Display the result
print(f"Data saved successfully to {file_name}")
print(f"Average NO₂ concentration at {place_name} on {current_date}: {average_no2:.2f} µg/m³")

# Open the Excel file
os.system(f'start excel "{file_name}"')