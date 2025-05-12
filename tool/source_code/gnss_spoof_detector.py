import pynmea2
import datetime
import math

# === CONFIG ===
GPS_LOG_FILE = 'sample_gps_log.txt'  # NMEA log file
MAX_JUMP_METERS = 500               # Max distance change allowed between points
MAX_TIME_JUMP = 10                  # Max time gap in seconds allowed

# === FUNCTIONS ===
def haversine(lat1, lon1, lat2, lon2):
    R = 6371000  # Radius of Earth in meters
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    delta_phi = math.radians(lat2 - lat1)
    delta_lambda = math.radians(lon2 - lon1)

    a = math.sin(delta_phi/2)**2 + \
        math.cos(phi1) * math.cos(phi2) * math.sin(delta_lambda/2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    return R * c

def parse_gps_log(filename):
    spoof_flags = []
    last_point = None

    with open(filename, 'r') as f:
        for line in f:
            if line.startswith('$GPRMC'):  # Use RMC sentences
                try:
                    msg = pynmea2.parse(line, check=False)
                    print(" Parsed:", line.strip())
                    if msg.status != 'A':
                        continue  # Skip invalid data

                    time = datetime.datetime.combine(msg.datestamp, msg.timestamp)
                    lat = msg.latitude
                    lon = msg.longitude

                    if last_point:
                        delta_time = (time - last_point['time']).total_seconds()
                        distance = haversine(lat, lon, last_point['lat'], last_point['lon'])

                        if distance > MAX_JUMP_METERS or delta_time > MAX_TIME_JUMP:
                            spoof_flags.append({
                                'time': time,
                                'distance': distance,
                                'delta_time': delta_time,
                                'location': (lat, lon)
                            })

                    last_point = {'time': time, 'lat': lat, 'lon': lon}

                except Exception as e:
                    print(f"Error parsing line: {e}")
    return spoof_flags

# === MAIN ===
if __name__ == "__main__":
    print(" GNSS Spoofing Detector Started")
    flags = parse_gps_log(GPS_LOG_FILE)

    if flags:
        print(f"\n Potential spoofing detected at {len(flags)} point(s):")
        for f in flags:
            print(f"[{f['time']}] Distance jump: {f['distance']:.2f} m | Time gap: {f['delta_time']:.2f}s | Location: {f['location']}")
    else:
        print(" No spoofing detected.")
