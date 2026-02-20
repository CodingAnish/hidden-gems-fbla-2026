import requests
import json

session = requests.Session()

# Get the home page to check server
print("Checking server...")
server_check = session.get("http://localhost:5001/")
print(f"Server status: {server_check.status_code}")

# Login with demo user
print("Logging in with demo user...")
login_response = session.post("http://localhost:5001/login", data={"identifier": "demo@hiddengems.local", "password": "demo1234"}, allow_redirects=True)
print(f"Login response: {login_response.status_code}")

# Get map page
print("Getting /map page...")
response = session.get("http://localhost:5001/map")

# Save to file for inspection
with open("/tmp/map_page.html", "w") as f:
    f.write(response.text)

print(f"Saved {len(response.text)} bytes to /tmp/map_page.html")

# Check for key content
if "businessesData" in response.text:
    print("✅ Found businessesData")
else:
    print("❌ NO businessesData found")

if "Discover Businesses" in response.text:
    print("✅ Found hero section text")
else:
    print("❌ NO hero section")

# Check opening of map div
if '<div id="map"' in response.text:
    print("✅ Found map container div")
else:
    print("❌ NO map container")

# Look for script tags
scripts = response.text.count("<script")
print(f"Found {scripts} script tags")

# Print first 2000 chars
print("\nFirst 1000 characters of response:")
print(response.text[:1000])
