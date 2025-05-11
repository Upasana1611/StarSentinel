import time

# === Sample SatCom endpoints (simulated)
satcom_devices = {
    '192.168.100.1': {'open_ports': [23, 80], 'service': 'Telnet/HTTP'},
    '192.168.100.2': {'open_ports': [21], 'service': 'FTP'},
    '192.168.100.3': {'open_ports': [], 'service': 'None'},
}

# === Sample TLE entries (insecure or malformed)
sample_tle = [
    "ISS (ZARYA)",
    "1 25544U 98067A   24120.54791667  .00007192  00000-0  13358-3 0  9999",
    "2 25544  51.6406 101.6565 0001652  96.0704  24.3030 15.50356669398196"
]

# === Insecure keywords (mock config warnings)
insecure_keywords = ["default password", "plaintext telemetry", "open access"]


def scan_satcom_network():
    print(" Scanning simulated SatCom network...\n")
    for ip, info in satcom_devices.items():
        time.sleep(0.5)  # simulate scan time
        if info['open_ports']:
            print(f"[!] {ip} has open ports: {info['open_ports']} ({info['service']})")
        else:
            print(f" {ip} appears secure (no services exposed)")
    print()


def check_tle_data():
    print(" Checking TLE format integrity...")
    if len(sample_tle) == 3 and sample_tle[1].startswith("1 ") and sample_tle[2].startswith("2 "):
        print(" TLE format looks valid.")
    else:
        print(" TLE data may be malformed.")
    print()


def scan_configurations():
    print(" Checking for insecure configurations...")
    config_example = """
    Device: SatCom-X1000
    Login: admin
    Password: default password
    Telemetry: plaintext telemetry
    Access: open access
    """
    for keyword in insecure_keywords:
        if keyword in config_example:
            print(f"[!] Found insecure config: {keyword}")
    print()


# === MAIN ===
if __name__ == "__main__":
    print(" Satellite Communications Security Scanner Started\n")
    scan_satcom_network()
    check_tle_data()
    scan_configurations()
    print("\n Scan complete.")
