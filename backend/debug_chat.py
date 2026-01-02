"""
Debug script to test chatbot functions directly
Run this to identify where the issue is
"""

import logging
import sys

# Set up detailed logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

print("=" * 60)
print("CHATBOT DEBUG SCRIPT")
print("=" * 60)

# Test 1: Import modules
print("\n[TEST 1] Importing modules...")
try:
    from model import chatbot_enhanced, vectorizer, model
    from session_manager import session_manager
    print("✓ Imports successful")
except Exception as e:
    print(f"✗ Import failed: {e}")
    sys.exit(1)

# Test 2: Check if model is loaded
print("\n[TEST 2] Checking model...")
if vectorizer is None or model is None:
    print("✗ Model not loaded!")
    print("Run: python train_model_script.py")
    sys.exit(1)
else:
    print("✓ Model loaded successfully")

# Test 3: Create test session
print("\n[TEST 3] Creating test session...")
try:
    test_session_id = session_manager.create_session()
    print(f"✓ Session created: {test_session_id[:8]}...")
except Exception as e:
    print(f"✗ Session creation failed: {e}")
    sys.exit(1)

# Test 4: Get session
print("\n[TEST 4] Getting session...")
try:
    session = session_manager.get_session(test_session_id)
    print(f"✓ Session retrieved: {session}")
except Exception as e:
    print(f"✗ Get session failed: {e}")
    sys.exit(1)

# Test 5: Test with empty message
print("\n[TEST 5] Testing empty message...")
try:
    response, intent, email = chatbot_enhanced("", session)
    print(f"✓ Empty message handled")
    print(f"  Response: {response}")
except Exception as e:
    print(f"✗ Empty message test failed: {e}")
    import traceback
    traceback.print_exc()

# Test 6: Test with simple greeting
print("\n[TEST 6] Testing simple greeting 'Hello!'...")
try:
    response, intent, email = chatbot_enhanced("Hello!", session)
    print(f"✓ Greeting handled")
    print(f"  Response: {response}")
    print(f"  Intent: {intent}")
    print(f"  Email: {email}")
except Exception as e:
    print(f"✗ Greeting test failed: {e}")
    import traceback
    traceback.print_exc()

# Test 7: Test session update
print("\n[TEST 7] Testing session update...")
try:
    if intent:
        session_manager.update_session(test_session_id, last_intent=intent)
        print("✓ Session update successful")
    else:
        print("⚠ No intent to update")
except Exception as e:
    print(f"✗ Session update failed: {e}")
    import traceback
    traceback.print_exc()

# Test 8: Verify session was updated
print("\n[TEST 8] Verifying session update...")
try:
    updated_session = session_manager.get_session(test_session_id)
    print(f"✓ Session after update: {updated_session}")
except Exception as e:
    print(f"✗ Session verification failed: {e}")

# Test 9: Test with various messages
print("\n[TEST 9] Testing various messages...")
test_messages = [
    "Bonjour",
    "What time is it?",
    "Calculate 5+3",
    "My email is test@example.com"
]

for msg in test_messages:
    print(f"\n  Testing: '{msg}'")
    try:
        response, intent, email = chatbot_enhanced(msg, session)
        print(f"  ✓ Response: {response[:50]}...")
        print(f"    Intent: {intent}, Email: {email}")
    except Exception as e:
        print(f"  ✗ Failed: {e}")
        import traceback
        traceback.print_exc()

# Test 10: Cleanup
print("\n[TEST 10] Cleaning up...")
try:
    session_manager.clear_session(test_session_id)
    print("✓ Session cleaned up")
except Exception as e:
    print(f"✗ Cleanup failed: {e}")

print("\n" + "=" * 60)
print("DEBUG TESTS COMPLETED")
print("=" * 60)
print("\nIf all tests passed, the issue might be in:")
print("1. Flask request handling")
print("2. CORS configuration")
print("3. Network/timing issue")
print("\nIf tests failed, check the error messages above.")