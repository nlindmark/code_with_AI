import csv

# Read weather data
with open('weather_log.csv', 'r') as f:
    reader = csv.DictReader(f)
    data = list(reader)

# Filter for temperatures below -15°C
cold_readings = [row for row in data if float(row['temperature']) < -15]

# Calculate average complexity
if cold_readings:
    total_complexity = sum(float(row['complexity']) for row in cold_readings)
    average = total_complexity / len(cold_readings)
    result = round(average, 1)
else:
    result = 0.0

print(result)
