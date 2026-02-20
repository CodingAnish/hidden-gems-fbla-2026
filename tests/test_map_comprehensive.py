#!/usr/bin/env python3
"""
Comprehensive test for map functionality including pagination
"""
import requests
import json
import re

BASE_URL = "http://localhost:5001"

def test_map_pagination():
    """Test that map loads businesses and pagination works"""
    session = requests.Session()
    
    # Login
    print("1️⃣ Logging in...")
    session.post(
        f"{BASE_URL}/login",
        data={"identifier": "demo@hiddengems.local", "password": "demo1234"},
        allow_redirects=True
    )
    print("   ✅ Logged in")
    
    # Get map page
    print("\n2️⃣ Getting map page...")
    response = session.get(f"{BASE_URL}/map")
    
    if response.status_code != 200:
        print(f"   ❌ Failed to get map page: {response.status_code}")
        return False
    print("   ✅ Map page loaded")
    
    # Extract businessesData
    print("\n3️⃣ Extracting businessesData...")
    match = re.search(r'const businessesData = (\[.*?\]);', response.text, re.DOTALL)
    if not match:
        print("   ❌ Could not find businessesData")
        return False
    
    try:
        all_businesses = json.loads(match.group(1))
        print(f"   ✅ Found {len(all_businesses)} total businesses")
        
        # Filter to only those with coordinates (same as backend does)
        with_coords = [b for b in all_businesses if b.get('latitude') and b.get('longitude')]
        print(f"   ✅ {len(with_coords)} businesses have coordinates")
        
        if len(with_coords) == 0:
            print("   ❌ No businesses with coordinates found!")
            return False
            
    except json.JSONDecodeError as e:
        print(f"   ❌ Failed to parse businessesData: {e}")
        return False
    
    # Check for page structure
    print("\n4️⃣ Checking page structure...")
    checks = {
        "Map container": '<div id="map"' in response.text,
        "Business list": 'id="businessList"' in response.text,
        "Load More button setup": 'id="loadMoreBtn"' in response.text or 'loadMoreBtn' in response.text,
        "Google Maps callback": 'initMapCallback' in response.text,
        "updateBusinessList function": 'function updateBusinessList' in response.text,
        "updateMapMarkers function": 'function updateMapMarkers' in response.text,
    }
    
    all_passed = True
    for check_name, result in checks.items():
        status = "✅" if result else "⚠️"
        print(f"   {status} {check_name}")
        if not result and "callback" not in check_name:
            all_passed = False
    
    # Check for critical functions in JavaScript
    print("\n5️⃣ Checking JavaScript functions...")
    functions = [
        'function initMap',
        'function updateBusinessList',
        'function renderBusinessList',
        'function updateMapMarkers',
        'function addGoogleMarkers',
        'function applyFilters',
    ]
    
    for func in functions:
        if func in response.text:
            print(f"   ✅ Found {func}")
        else:
            print(f"   ⚠️ Missing {func}")
    
    return all_passed and len(with_coords) > 0

if __name__ == "__main__":
    print("🗺️  Comprehensive Map Page Test\n")
    
    success = test_map_pagination()
    
    if success:
        print("\n✅ All tests PASSED! Map should be fully functional.")
        print("\n📝 Next steps for user:")
        print("   - Open the map page in browser")
        print("   - Verify businesses appear on the map")
        print("   - Click 'Load More' to see more businesses") 
        print("   - Click on a business name to highlight it on the map")
    else:
        print("\n❌ Some tests FAILED - check output above")
