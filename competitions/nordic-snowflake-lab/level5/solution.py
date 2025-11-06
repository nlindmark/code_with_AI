import json

# Read sensor data
with open('sensors.json', 'r') as f:
    data = json.load(f)

# Extract conditions
temp = data['conditions']['temperature']
humidity = data['conditions']['humidity']
wind_speed = data['conditions']['wind_speed']

# Apply prediction rules in order
if humidity > 85 and temp < -18:
    pattern = '*+#'
elif humidity > 75 and temp < -12:
    pattern = '*+*'
elif wind_speed < 5 and humidity > 80:
    pattern = '***'
else:
    pattern = '*-*'

print(pattern)
