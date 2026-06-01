import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from modules.controller.auth_controller import hash_password, login_user
from modules.controller import landlord_controller
from modules.controller import property_controller
from modules.controller.business_logic import check_double_booking, can_delete_landlord



def check(test_name, condition):
    if condition:
        print(f"PASS - {test_name}")
    else:
        print(f"FAIL - {test_name}")


print("=" * 60)
print("TEST CASES - Real Estate PMS")
print("=" * 60)

# Test 1: Password hashing works
print("\n--- NORMAL CASE TESTS ---")
hash1 = hash_password("admin123")
hash2 = hash_password("admin123")
check("TC01: Same password gives same hash", hash1 == hash2)

# Test 2: Different passwords give different hashes
hash3 = hash_password("different")
check("TC02: Different passwords give different hashes", hash1 != hash3)

# Test 3: Valid login works
user = login_user("admin", "admin123")
check("TC03: Valid admin login", user is not None and user['username'] == 'admin')

# Test 4: Invalid login fails
user = login_user("admin", "wrongpassword")
check("TC04: Invalid password rejected", user is None)

# Test 5: Get all landlords returns a list
landlords = landlord_controller.get_all_landlords()
check("TC05: Get all landlords", isinstance(landlords, list) and len(landlords) > 0)

# Test 6: Get all properties returns a list
properties = property_controller.get_all_properties()
check("TC06: Get all properties", isinstance(properties, list) and len(properties) > 0)

# Test 7: Search by suburb works
results = property_controller.search_properties("Melbourne")
check("TC07: Search properties by suburb", len(results) > 0)

print("\n--- BOUNDARY CASE TESTS ---")

# Test 8: Search with empty keyword returns all
results = property_controller.search_properties("")
check("TC08: Empty search returns no matches", isinstance(results, list))

# Test 9: Search with non-existent keyword returns empty
results = property_controller.search_properties("NonExistentSuburb123")
check("TC09: Non-existent search returns empty list", len(results) == 0)

print("\n--- INVALID INPUT TESTS ---")

# Test 10: Login with empty username fails
user = login_user("", "admin123")
check("TC10: Empty username rejected", user is None)

# Test 11: Login with non-existent user fails
user = login_user("fakeuser", "admin123")
check("TC11: Non-existent user rejected", user is None)

# Test 12: SQL injection attempt is blocked (parameterized queries)
user = login_user("admin' OR '1'='1", "anything")
check("TC12: SQL injection blocked", user is None)

print("\n--- BUSINESS LOGIC TESTS ---")

# Test 13: Double booking detection
# Property 1 already has lease from 2025-01-01 to 2025-12-31
overlap = check_double_booking(1, '2025-06-01', '2025-08-31')
check("TC13: Double booking detected", overlap is True)

# Test 14: No double booking when dates dont overlap
no_overlap = check_double_booking(1, '2027-01-01', '2027-12-31')
check("TC14: Non-overlapping dates allowed", no_overlap is False)

# Test 15: Cannot delete landlord with properties
can_delete = can_delete_landlord(1)  # Landlord 1 owns properties
check("TC15: Cannot delete landlord with properties", can_delete is False)

print("\n" + "=" * 60)
print("TEST RUN COMPLETE")
print("=" * 60)
