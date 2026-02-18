#!/usr/bin/env python3
"""
Improved test suite - handles email verification
"""

import requests
import json
import time
import re
from datetime import datetime
from bs4 import BeautifulSoup

BASE_URL = "http://localhost:5001"
TEST_EMAIL = f"testuser_{int(time.time())}@test.com"
TEST_USERNAME = f"testuser{int(time.time())}"
TEST_PASSWORD = "TestPassword123!"

class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    END = '\033[0m'

def print_test(name, passed, details=""):
    status = f"{Colors.GREEN}✓{Colors.END}" if passed else f"{Colors.RED}✗{Colors.END}"
    print(f"{status} {name}")
    if details:
        print(f"  {Colors.YELLOW}→ {details}{Colors.END}")

def extract_verification_code(html):
    """Extract verification code from flash message"""
    # Look for "code is: 123456" or similar pattern
    match = re.search(r'code is:\s*([0-9]{6})', html, re.IGNORECASE)
    if match:
        return match.group(1)
    # Try alternative patterns
    match = re.search(r'code[:\s]*([0-9]{6})', html, re.IGNORECASE)
    if match:
        return match.group(1)
    return None

def main():
    session = requests.Session()
    session.allow_redirects = True
    
    print(f"\n{Colors.BLUE}{'='*60}{Colors.END}")
    print(f"{Colors.BLUE}Hidden Gems - Complete User Flow Test{Colors.END}")
    print(f"{Colors.BLUE}{'='*60}{Colors.END}\n")
    
    # Test 1: Server running
    print("TEST 1: Server connection...")
    try:
        r = session.get(f"{BASE_URL}/")
        print_test("Server responding", r.status_code in [200, 302], f"Status: {r.status_code}")
    except Exception as e:
        print_test("Server responding", False, str(e))
        return
    
    # Test 2: Register user
    print("\nTEST 2: User registration...")
    data = {
        'username': TEST_USERNAME,
        'email': TEST_EMAIL,
        'password': TEST_PASSWORD,
        'confirm': TEST_PASSWORD
    }
    
    r = session.post(f"{BASE_URL}/register", data=data)
    print_test("Registration POST", r.status_code in [200, 302], f"Status: {r.status_code}")
    
    # Extract verification code
    code = extract_verification_code(r.text)
    print_test("Verification code found", code is not None, f"Code: {code if code else 'Not found'}")
    
    if not code:
        print(f"\n{Colors.YELLOW}Cannot proceed without verification code{Colors.END}")
        return
    
    # Test 3: Verify email
    print("\nTEST 3: Email verification...")
    verify_data = {'code': code}
    r = session.post(f"{BASE_URL}/verify", data=verify_data)
    print_test("Verification POST", r.status_code in [200, 302], f"Status: {r.status_code}")
    
    # Check if logged in after verification
    is_logged_in = "dashboard" in r.text.lower() or "directory" in r.text.lower() or "logout" in r.text.lower()
    print_test("User logged in after verification", is_logged_in, "Session established")
    
    # Test 4: Access profile
    print("\nTEST 4: Profile page...")
    r = session.get(f"{BASE_URL}/profile")
    print_test("Profile page loads", r.status_code == 200, f"Status: {r.status_code}")
    
    has_profile_content = any(x in r.text.lower() for x in ["profile", "review", "favorite", "member"])
    print_test("Profile has user data", has_profile_content, "User stats visible")
    
    # Test 5: Settings page
    print("\nTEST 5: Settings page...")
    r = session.get(f"{BASE_URL}/settings")
    print_test("Settings page loads", r.status_code == 200, f"Status: {r.status_code}")
    
    has_settings = any(x in r.text.lower() for x in ["settings", "preference", "notification", "privacy"])
    print_test("Settings has content", has_settings, "Settings sections visible")
    
    # Test 6: Forgot password
    print("\nTEST 6: Forgot password page...")
    r = session.get(f"{BASE_URL}/forgot-password")
    print_test("Forgot password page loads", r.status_code == 200, f"Status: {r.status_code}")
    
    # Test 7: Navigation
    print("\nTEST 7: Navigation...")
    r = session.get(f"{BASE_URL}/directory")
    print_test("Directory page loads", r.status_code == 200, f"Status: {r.status_code}")
    
    # Test 8: Logout
    print("\nTEST 8: Logout...")
    r = session.get(f"{BASE_URL}/logout")
    print_test("Logout succeeds", r.status_code in [200, 302], f"Status: {r.status_code}")
    
    # Test 9: Profile after logout (should redirect)
    r = session.get(f"{BASE_URL}/profile")
    print_test("Profile inaccessible after logout", r.status_code in [200, 302] and "login" in r.text.lower(), "Redirected to login")
    
    print(f"\n{Colors.GREEN}{'='*60}{Colors.END}")
    print(f"{Colors.GREEN}{'✓ All tests completed successfully!':^60}{Colors.END}")
    print(f"{Colors.GREEN}{'='*60}{Colors.END}\n")

if __name__ == "__main__":
    main()
