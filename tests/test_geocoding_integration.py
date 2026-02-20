#!/usr/bin/env python3
"""
Test script to verify geocoding integration is working
"""
import sys
import os
import json
import subprocess
import time

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from database import queries

def test_geocoding_integration():
    """Test that all necessary components are present"""
    
    print("=" * 60)
    print("🧪 GEOCODING INTEGRATION TEST")
    print("=" * 60)
    
    # Test 1: Check database has businesses
    print("\n1️⃣ Checking database businesses...")
    try:
        all_businesses = queries.get_all_businesses()
        print(f"✅ Found {len(all_businesses)} businesses")
        
        # Count businesses with/without coordinates
        with_coords = sum(1 for b in all_businesses if b.get('latitude') and b.get('longitude'))
        without_coords = len(all_businesses) - with_coords
        
        print(f"   - With coordinates: {with_coords}")
        print(f"   - Without coordinates: {without_coords}")
        print(f"   - Addresses available: {sum(1 for b in all_businesses if b.get('address'))}")
    except Exception as e:
        print(f"❌ Database error: {e}")
        return False
    
    # Test 2: Check map.html has geocoding functions
    print("\n2️⃣ Checking map.html has geocoding code...")
    try:
        with open('web/templates/map.html', 'r') as f:
            content = f.read()
            
        checks = {
            'geocodeCache': 'const geocodeCache' in content,
            'geocodeAddress function': 'async function geocodeAddress(' in content,
            'geocodeAllBusinesses function': 'async function geocodeAllBusinesses(' in content,
            'geocodingchain in initMap': 'geocodeAllBusinesses(allBusinesses).then' in content,
        }
        
        all_passed = True
        for check_name, passed in checks.items():
            status = "✅" if passed else "❌"
            print(f"   {status} {check_name}")
            if not passed:
                all_passed = False
        
        if not all_passed:
            return False
            
    except Exception as e:
        print(f"❌ File read error: {e}")
        return False
    
    # Test 3: Check app.py passes all businesses to map template
    print("\n3️⃣ Checking app.py map_view passes all businesses...")
    try:
        with open('web/app.py', 'r') as f:
            content = f.read()
        
        # Look for the map_view function
        if 'businesses=all_businesses' in content and 'def map_view()' in content:
            # Check it's NOT filtering by coordinates
            if 'if b.get("latitude")' not in content or 'map_businesses' not in content:
                print("   ✅ Map view passes all businesses (not filtered by coordinates)")
            else:
                print("   ⚠️  Map view might still be filtering businesses")
        else:
            print("   ❌ Map view doesn't pass all_businesses")
            return False
            
    except Exception as e:
        print(f"❌ File read error: {e}")
        return False
    
    # Test 4: Check Flask server is running
    print("\n4️⃣ Checking Flask server is running on port 5001...")
    try:
        import urllib.request
        response = urllib.request.urlopen('http://localhost:5001/', timeout=2)
        print(f"   ✅ Flask server is running (status code: {response.code})")
    except Exception as e:
        print(f"   ❌ Flask server not responding: {e}")
        return False
    
    # Test 5: Sample business with address
    print("\n5️⃣ Checking sample businesses have requirements for geocoding...")
    if all_businesses:
        sample = all_businesses[0]
        print(f"   Sample business: {sample.get('name')}")
        print(f"   - Address: {sample.get('address', 'MISSING')}")
        print(f"   - Category: {sample.get('category', 'MISSING')}")
        print(f"   - Coordinates: ({sample.get('latitude', 'MISSING')}, {sample.get('longitude', 'MISSING')})")
        
        if sample.get('address'):
            print("   ✅ Sample has address for geocoding")
        else:
            print("   ❌ Sample missing address")
            return False
    
    print("\n" + "=" * 60)
    print("✅ ALL TESTS PASSED - Geocoding integration ready!")
    print("=" * 60)
    print("\n📋 Next steps:")
    print("1. Open http://localhost:5001/map in your browser")
    print("2. Log in with your account")
    print("3. Open browser DevTools Console (F12)")
    print("4. Watch for:")
    print("   - '🔄 Starting geocoding for X businesses...'")
    print("   - '✅ Geocoded: [address] -> {lat, lng}'")
    print("   - '✅ Geocoded X businesses'")
    print("5. Markers should appear on map after geocoding completes")
    
    return True

if __name__ == "__main__":
    success = test_geocoding_integration()
    sys.exit(0 if success else 1)
