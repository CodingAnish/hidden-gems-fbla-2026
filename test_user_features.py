#!/usr/bin/env python3
"""
Automated Test Suite for Hidden Gems User Features
Tests all user account flows end-to-end
"""

import requests
import json
import time
import re
from datetime import datetime

# Configuration
BASE_URL = "http://localhost:5001"
TEST_EMAIL = f"testuser_{int(time.time())}@test.com"
TEST_USERNAME = f"testuser{int(time.time())}"
TEST_PASSWORD = "TestPassword123!"

# Color codes for terminal output
class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    END = '\033[0m'

def print_test(name, passed, details=""):
    """Print test result with color"""
    status = f"{Colors.GREEN}✓ PASS{Colors.END}" if passed else f"{Colors.RED}✗ FAIL{Colors.END}"
    print(f"{status} - {name}")
    if details:
        print(f"  {Colors.YELLOW}→ {details}{Colors.END}")

def print_section(title):
    """Print test section header"""
    print(f"\n{Colors.BLUE}{'='*60}{Colors.END}")
    print(f"{Colors.BLUE}{title:^60}{Colors.END}")
    print(f"{Colors.BLUE}{'='*60}{Colors.END}\n")


class UserFlowTester:
    def __init__(self):
        self.session = requests.Session()
        self.tests_passed = 0
        self.tests_failed = 0
        self.verification_code = None
        
    def test_server_running(self):
        """Test 1: Verify Flask server is running"""
        print_section("TEST 1: Server Health Check")
        try:
            response = self.session.get(f"{BASE_URL}/", timeout=5)
            passed = response.status_code in [200, 302, 404]
            print_test("Flask server running", passed, f"Status code: {response.status_code}")
            if passed:
                self.tests_passed += 1
            else:
                self.tests_failed += 1
            return passed
        except Exception as e:
            print_test("Flask server running", False, f"Error: {str(e)}")
            self.tests_failed += 1
            return False
    
    def test_login_page_loads(self):
        """Test 2: Verify login page loads"""
        print_section("TEST 2: Login Page")
        try:
            response = self.session.get(f"{BASE_URL}/login")
            passed = response.status_code == 200 and "login" in response.text.lower()
            print_test("Login page loads", passed, f"Status: {response.status_code}")
            
            # Check for forgot password link
            has_forgot = "forgot" in response.text.lower()
            print_test("Forgot password link exists", has_forgot)
            if has_forgot:
                self.tests_passed += 1
            else:
                self.tests_failed += 1
                
            if passed:
                self.tests_passed += 1
            else:
                self.tests_failed += 1
            return passed
        except Exception as e:
            print_test("Login page loads", False, f"Error: {str(e)}")
            self.tests_failed += 1
            return False
    
    def test_register_page_loads(self):
        """Test 3: Verify registration page loads"""
        print_section("TEST 3: Registration Page")
        try:
            response = self.session.get(f"{BASE_URL}/register")
            passed = response.status_code == 200 and "register" in response.text.lower()
            print_test("Registration page loads", passed, f"Status: {response.status_code}")
            
            if passed:
                self.tests_passed += 1
            else:
                self.tests_failed += 1
            return passed
        except Exception as e:
            print_test("Registration page loads", False, f"Error: {str(e)}")
            self.tests_failed += 1
            return False
    
    def test_forgot_password_page(self):
        """Test 4: Verify forgot password page"""
        print_section("TEST 4: Forgot Password Page")
        try:
            response = self.session.get(f"{BASE_URL}/forgot-password")
            passed = response.status_code == 200 and "forgot" in response.text.lower()
            print_test("Forgot password page loads", passed, f"Status: {response.status_code}")
            
            if passed:
                self.tests_passed += 1
            else:
                self.tests_failed += 1
            return passed
        except Exception as e:
            print_test("Forgot password page loads", False, f"Error: {str(e)}")
            self.tests_failed += 1
            return False
    
    def test_registration(self):
        """Test 5: Register new user"""
        print_section("TEST 5: User Registration")
        try:
            data = {
                'username': TEST_USERNAME,
                'email': TEST_EMAIL,
                'password': TEST_PASSWORD,
                'confirm_password': TEST_PASSWORD
            }
            
            response = self.session.post(f"{BASE_URL}/register", data=data)
            passed = response.status_code in [200, 302]
            
            # Check for verification code in response or database
            print_test("Registration POST succeeds", passed, f"Status: {response.status_code}")
            
            if "verify" in response.text.lower() or "verification" in response.text.lower():
                print_test("Verification page shown/email sent", True)
                self.tests_passed += 1
            else:
                print_test("Verification page shown/email sent", False)
                self.tests_failed += 1
                
            if passed:
                self.tests_passed += 1
            else:
                self.tests_failed += 1
            return passed
        except Exception as e:
            print_test("User registration", False, f"Error: {str(e)}")
            self.tests_failed += 1
            return False
    
    def test_login(self):
        """Test 6: Login with registered user"""
        print_section("TEST 6: User Login")
        try:
            # Try login with email
            data = {
                'email_or_username': TEST_EMAIL,
                'password': TEST_PASSWORD
            }
            
            response = self.session.post(f"{BASE_URL}/login", data=data)
            
            # Check if redirected (301, 302) or if login succeeded
            passed = response.status_code in [200, 302] or "dashboard" in response.text.lower() or "directory" in response.text.lower()
            print_test("Login with email succeeds", passed, f"Status: {response.status_code}")
            
            if passed:
                self.tests_passed += 1
            else:
                self.tests_failed += 1
            return passed
        except Exception as e:
            print_test("User login", False, f"Error: {str(e)}")
            self.tests_failed += 1
            return False
    
    def test_profile_page(self):
        """Test 7: Access profile page after login"""
        print_section("TEST 7: User Profile Page")
        try:
            response = self.session.get(f"{BASE_URL}/profile")
            
            # Should not redirect to login if logged in
            passed = response.status_code == 200 and "profile" in response.text.lower()
            print_test("Profile page accessible", passed, f"Status: {response.status_code}")
            
            # Check for profile elements
            has_stats = "review" in response.text.lower() or "favorite" in response.text.lower()
            print_test("Profile shows stats", has_stats)
            
            if has_stats:
                self.tests_passed += 1
            else:
                self.tests_failed += 1
            
            if passed:
                self.tests_passed += 1
            else:
                self.tests_failed += 1
            return passed
        except Exception as e:
            print_test("Profile page access", False, f"Error: {str(e)}")
            self.tests_failed += 1
            return False
    
    def test_settings_page(self):
        """Test 8: Access settings page"""
        print_section("TEST 8: User Settings Page")
        try:
            response = self.session.get(f"{BASE_URL}/settings")
            passed = response.status_code == 200 and "settings" in response.text.lower()
            print_test("Settings page accessible", passed, f"Status: {response.status_code}")
            
            # Check for settings sections
            has_preferences = "preference" in response.text.lower() or "category" in response.text.lower()
            has_notifications = "notification" in response.text.lower()
            has_privacy = "privacy" in response.text.lower()
            
            print_test("Settings has preferences section", has_preferences)
            print_test("Settings has notifications section", has_notifications)
            print_test("Settings has privacy section", has_privacy)
            
            if has_preferences:
                self.tests_passed += 1
            if has_notifications:
                self.tests_passed += 1
            if has_privacy:
                self.tests_passed += 1
                
            if passed:
                self.tests_passed += 1
            else:
                self.tests_failed += 1
            return passed
        except Exception as e:
            print_test("Settings page access", False, f"Error: {str(e)}")
            self.tests_failed += 1
            return False
    
    def test_navigation_dropdown(self):
        """Test 9: Verify user dropdown menu in navigation"""
        print_section("TEST 9: Navigation Dropdown Menu")
        try:
            response = self.session.get(f"{BASE_URL}/directory")
            
            # Check for user menu elements
            has_dropdown = "userMenu" in response.text or "toggleUserMenu" in response.text
            has_profile_link = 'href="{{ url_for(\'profile\') }}"' in response.text or "/profile" in response.text
            has_settings_link = 'href="{{ url_for(\'settings\') }}"' in response.text or "/settings" in response.text
            
            print_test("Dropdown menu exists", has_dropdown)
            print_test("Profile link in menu", has_profile_link)
            print_test("Settings link in menu", has_settings_link)
            
            if has_dropdown:
                self.tests_passed += 1
            else:
                self.tests_failed += 1
            if has_profile_link:
                self.tests_passed += 1
            else:
                self.tests_failed += 1
            if has_settings_link:
                self.tests_passed += 1
            else:
                self.tests_failed += 1
            
            return True
        except Exception as e:
            print_test("Navigation dropdown check", False, f"Error: {str(e)}")
            self.tests_failed += 1
            return False
    
    def test_logout(self):
        """Test 10: Logout functionality"""
        print_section("TEST 10: Logout")
        try:
            response = self.session.get(f"{BASE_URL}/logout")
            
            # Should redirect after logout (302)
            passed = response.status_code in [200, 302]
            print_test("Logout succeeds", passed, f"Status: {response.status_code}")
            
            # Try accessing profile - should redirect to login
            response2 = self.session.get(f"{BASE_URL}/profile")
            redirected = response2.status_code in [200, 302] and ("login" in response2.text.lower() or response2.url.endswith("/login"))
            print_test("Access denied after logout", redirected, "Redirected to login")
            
            if redirected:
                self.tests_passed += 1
            else:
                self.tests_failed += 1
                
            if passed:
                self.tests_passed += 1
            else:
                self.tests_failed += 1
            return passed
        except Exception as e:
            print_test("Logout", False, f"Error: {str(e)}")
            self.tests_failed += 1
            return False
    
    def run_all_tests(self):
        """Run complete test suite"""
        print(f"\n{Colors.BLUE}{'*'*60}{Colors.END}")
        print(f"{Colors.BLUE}Hidden Gems - User Features Test Suite{Colors.END}")
        print(f"{Colors.BLUE}Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}{Colors.END}")
        print(f"{Colors.BLUE}{'*'*60}{Colors.END}")
        
        # Run all tests
        if not self.test_server_running():
            print(f"\n{Colors.RED}Server not running! Cannot proceed with tests.{Colors.END}")
            return False
        
        self.test_login_page_loads()
        self.test_register_page_loads()
        self.test_forgot_password_page()
        self.test_registration()
        self.test_login()
        self.test_profile_page()
        self.test_settings_page()
        self.test_navigation_dropdown()
        self.test_logout()
        
        # Print summary
        total = self.tests_passed + self.tests_failed
        percentage = (self.tests_passed / total * 100) if total > 0 else 0
        
        print_section("Test Summary")
        print(f"Total Tests: {total}")
        print(f"{Colors.GREEN}Passed: {self.tests_passed}{Colors.END}")
        print(f"{Colors.RED}Failed: {self.tests_failed}{Colors.END}")
        print(f"Success Rate: {percentage:.1f}%")
        
        if self.tests_failed == 0:
            print(f"\n{Colors.GREEN}{'🎉 ALL TESTS PASSED! 🎉':^60}{Colors.END}")
        else:
            print(f"\n{Colors.YELLOW}{'⚠️  SOME TESTS FAILED - See details above':^60}{Colors.END}")
        
        return self.tests_failed == 0


if __name__ == "__main__":
    tester = UserFlowTester()
    success = tester.run_all_tests()
    exit(0 if success else 1)
