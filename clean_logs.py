def celsius_converter(f_temp):
    f_temp = float(f_temp)
    c_temp = (f_temp - 32) * 5 / 9
    return round(c_temp, 2)


def parse_and_clean(line):
    line = line.strip()

    if line == "":
        return None

    parts = line.split("|")


    if len(parts) != 5:
        return None

    #Extra spaces are removed
    timestamp = parts[0].strip()
    station_id = parts[1].strip()
    temperature = parts[2].strip()
    humidity = parts[3].strip()
    sensor_status = parts[4].strip()

    #Finding missing fields 
    if (
        timestamp == ""
        or station_id == ""
        or temperature == ""
        or humidity == ""
        or sensor_status == ""
    ):
        return None

    
    if sensor_status != "ACTIVE":
        return None

    if temperature == "ERROR" or temperature == "N/A":
        return None


    try:
        float(temperature)
    except ValueError:
        return None

    return timestamp, station_id, temperature, humidity, sensor_status


skipped_lines = 0

with open("environmental_raw.txt", "r") as input_file, \
     open("environmental_clean.csv", "w") as output_file:


    output_file.write(
        "Timestamp,StationID,Temp_C,Humidity,Sensor_Status\n"
    )

    for line in input_file:

        cleaned = parse_and_clean(line)

        if cleaned is None:
            skipped_lines += 1
            continue

        timestamp, station_id, temperature, humidity, sensor_status = cleaned

        temperature_c = celsius_converter(temperature)

        output_file.write(
            f"{timestamp},{station_id},{temperature_c},{humidity},{sensor_status}\n"
        )


print("Corrupted lines skipped:", skipped_lines)