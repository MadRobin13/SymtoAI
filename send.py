import requests

# Define the URL of the server
url = 'http://127.0.0.1:5000/predict'

# Path to the image file
image_path = r'images\11071-infected_blackhead-648x364-body.webp'

# Open the image file in binary mode
with open(image_path, 'rb') as image_file:
    files = {'file': image_file}
    
    # Send the POST request with the image file
    response = requests.post(url, files=files)

# Print the server's response
print(response.json())
