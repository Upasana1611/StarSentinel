from skyfield.api import load, EarthSatellite
import matplotlib.pyplot as plt

# === Real TLE for ISS
tle_lines = [
    "ISS (ZARYA)",
    "1 25544U 98067A   24120.54791667  .00007192  00000-0  13358-3 0  9999",
    "2 25544  51.6406 101.6565 0001652  96.0704  24.3030 15.50356669398196"
]

# === Spoofed object (pretends to be another satellite in close orbit)
spoofed_tle_lines = [
    "FakeSat",
    "1 99999U 24120A   24120.54791667  .00000001  00000-0  00000-0 0  9999",
    "2 99999  51.6406 101.6565 0001652  97.0704  25.3030 15.50356669398196"
]

# === Load satellites
ts = load.timescale()
time = ts.now()
real_sat = EarthSatellite(tle_lines[1], tle_lines[2], tle_lines[0], ts)
spoofed_sat = EarthSatellite(spoofed_tle_lines[1], spoofed_tle_lines[2], spoofed_tle_lines[0], ts)

# === Get positions
real_pos = real_sat.at(time).position.km
spoofed_pos = spoofed_sat.at(time).position.km

# === Calculate 3D distance
def distance_km(pos1, pos2):
    return ((pos1[0] - pos2[0]) ** 2 + (pos1[1] - pos2[1]) ** 2 + (pos1[2] - pos2[2]) ** 2) ** 0.5

risk = distance_km(real_pos, spoofed_pos)

# === Output
print("🚀 Space Traffic Threat Simulation")
print(f"\nReal satellite position (km):     {real_pos}")
print(f"Spoofed satellite position (km):  {spoofed_pos}")
print(f"\n🚨 Distance between them: {risk:.2f} km")

if risk < 50:
    print("⚠️  Potential collision risk! Malicious spoof detected.")
else:
    print("✅ No immediate threat.")

# === Optional: Plot
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.scatter(*real_pos, color='blue', label='Real Sat')
ax.scatter(*spoofed_pos, color='red', label='Spoofed Sat')
ax.legend()
ax.set_title("Satellite Position Simulation (km)")
plt.show()
