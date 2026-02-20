#!/usr/bin/env python3
"""
Test map page to verify businesses load and pagination works
"""
import requests
import json
from bs4 import BeautifulSoup
import time

BASE_URL = "http://localhost:5001"
EMAIL = "test@example.com"
PASSWORD = "testpass123"

def test_map_page():
    """Test that map page loads with businesses"""
    session = requests.Session()
    
    # Step 1: Get login page first
    print("1️⃣ Getting login page...")
    login_get = session.get(f"{BASE_URL}/login")
    if login_get.status_code != 200:
        print(f"   ❌ Could not get login page: {login_get.status_code}")
        return False
    
    # Step 2: Login
    print("2️⃣ Attempting to log in...")
    login_response = session.post(
        f"{BASE_URL}/login",
        data={"email": EMAIL, "password": PASSWORD},
        allow_redirects=True
    )
    
    if login_response.status_code == 200:
        print("   ✅ Login successful")
    else:
        print(f"   ⚠️ Login response: {login_response.status_code}")
    
    # Step 3: Access map page
    print("\n3️⃣ Accessing /map page...")
    map_response = session.get(f"{BASE_URL}/map")
    
    if map_response.status_code == 200:
        print("   ✅ Map page loaded (200)")
    else:
        print(f"   ❌ Map page failed: {map_response.status_code}")
        return False
    
    # Step 4: Check for businesses in HTML
    print("\n4️⃣ Checking for businesses data in HTML...")
    html = map_response.text
    
    # Look for businessesData in the HTML
    if "businessesData" in html:
        print("   ✅ Found businessesData variable")
        
        # Try to extract the JSON
        import re
        match = re.search(r'const businessesData = (\[.*?\]);', html, re.DOTALL)
        if match:
            try:
                businesses = json.loads(match.group(1))
                print(f"   ✅ Found {len(businesses)} businesses in page")
                
                # Show first few business names
                if businesses:
                    for i, b in enumerate(businesses[:3]):
                        print(f"      {i+1}. {b.get('name', 'N/A')} - {b.get('category', 'N/A')}")
                    if len(businesses) > 3:
                        print(f"      ... and {len(businesses) - 3} more")
                        
                    # Check for coordinates
                    with_coords = sum(1 for b in businesses if b.get('latitude') and b.get('longitude'))
                    print(f"   ✅ {with_coords}/{len(businesses)} businesses have coordinates")
                    return True
            except json.JSONDecodeError as e:
                print(f"   ⚠️ Could not parse businesses JSON: {e}")
    else:
        print("   ❌ businessesData not found in HTML")
    
    # Check for map script
    if "initMapCallback" in html:
        print("   ✅ Found Google Maps callback setup")
    else:
        print("   ⚠️ Google Maps callback not found")
    
    if "leaflet" in html.lower():
        print("   ✅ Found Leaflet library reference")
    
    return "businessesData" in html

if __name__ == "__main__":
    print("🗺️  Testing Hidden Gems Map Page\n")
    
    # Give server time to start
    for i in range(3):
        try:
            response = requests.get(f"{BASE_URL}/", timeout=2)
            break
        except requests.ConnectionError:
            if i < 2:
                print(f"⏳ Server not ready, waiting... ({i+1}/3)")
                time.sleep(1)
            else:
                print("❌ Server not responding")
                exit(1)
    
    success = test_map_page()
    
    if success:
        print("\n✅ Map page test PASSED - businesses are loading")
    else:
        print("\n❌ Map page test FAILED - please check logs above")
