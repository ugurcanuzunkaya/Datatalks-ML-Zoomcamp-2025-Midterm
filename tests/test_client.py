"""
Test client for SWaT intrusion detection API
Uses real samples from validation set
"""

import httpx

API_URL = "http://localhost:9696"

# Real normal operation from validation set (predicted correctly as Normal with 0.02% attack probability)
normal_reading = {
    "FIT101": 2.600327,
    "LIT101": 528.9309,
    "MV101": 0.0,
    "P101": 2,
    "P102": 1,
    "AIT201": 0.0,
    "AIT202": 8.380415,
    "AIT203": 330.0948,
    "FIT201": 2.441547,
    "MV201": 0.0,
    "P201": 0.0,
    "P202": 0.0,
    "P203": 2,
    "P204": 0.0,
    "P205": 2,
    "P206": 1,
    "DPIT301": 19.92445,
    "FIT301": 2.217852,
    "LIT301": 973.9891,
    "MV301": 1,
    "MV302": 2,
    "MV303": 0.0,
    "MV304": 1,
    "P301": 1,
    "P302": 2,
    "AIT401": 148.8032,
    "AIT402": 156.7034,
    "FIT401": 1.728382,
    "LIT401": 977.6724,
    "P401": 1,
    "P402": 2,
    "P403": 1,
    "P404": 1,
    "UV401": 2,
    "AIT501": 7.878621,
    "AIT502": 145.3986,
    "AIT503": 264.2271,
    "AIT504": 12.45834,
    "FIT501": 1.738272,
    "FIT502": 1.299219,
    "FIT503": 0.7323241,
    "FIT504": 0.3045831,
    "P501": 2,
    "P502": 1,
    "PIT501": 250.7049,
    "PIT502": 1.137347,
    "PIT503": 189.4867,
    "FIT601": 6.407587e-05,
    "P601": 1,
    "P602": 1,
    "P603": 1,
}

# Real attack from validation set (predicted correctly as Attack with 100% probability)
attack_reading = {
    "FIT101": 0.0,
    "LIT101": 813.3956,
    "MV101": 1.0,
    "P101": 1,
    "P102": 1,
    "AIT201": 192.8993,
    "AIT202": 8.582287,
    "AIT203": 354.1656,
    "FIT201": 0.0,
    "MV201": 1.0,
    "P201": 1.0,
    "P202": 1.0,
    "P203": 1,
    "P204": 1.0,
    "P205": 1,
    "P206": 1,
    "DPIT301": 2.010372,
    "FIT301": 0.0,
    "LIT301": 1016.246,
    "MV301": 1,
    "MV302": 1,
    "MV303": 1.0,
    "MV304": 2,
    "P301": 1,
    "P302": 1,
    "AIT401": 148.8128,
    "AIT402": 332.1712,
    "FIT401": 0.0,
    "LIT401": 248.2825,
    "P401": 1,
    "P402": 1,
    "P403": 1,
    "P404": 1,
    "UV401": 1,
    "AIT501": 7.515573,
    "AIT502": 225.7626,
    "AIT503": 268.1043,
    "AIT504": 15.57293,
    "FIT501": 0.000897206,
    "FIT502": 0.000896631,
    "FIT503": 0.000896201,
    "FIT504": 0.0,
    "P501": 1,
    "P502": 1,
    "PIT501": 10.01346,
    "PIT502": 0.0,
    "PIT503": 3.733017,
    "FIT601": 0.0,
    "P601": 1,
    "P602": 1,
    "P603": 1,
}

print("=" * 80)
print("SWaT INTRUSION DETECTION - API TEST CLIENT (REAL DATA)")
print("=" * 80)

# Test health check
print("\n" + "=" * 80)
print("Testing Health Check")
print("=" * 80)
response = httpx.get(f"{API_URL}/health")
if response.status_code == 200:
    print(f"✅ Health check passed: {response.json()}")
else:
    print(f"❌ Health check failed: {response.status_code}")

# Test normal operation
print("\n" + "=" * 80)
print("Testing: Normal Operation (Real Validation Sample)")
print("=" * 80)
response = httpx.post(f"{API_URL}/predict", json=normal_reading)
if response.status_code == 200:
    result = response.json()
    print("✅ Prediction received:")
    print(f"   Classification: {result['classification']}")
    print(f"   Attack Probability: {result['attack_probability']:.4f}")
    print(f"   Confidence: {result['confidence']:.4f}")

    # Check if correct
    if result["classification"] == "Normal":
        print("   ✅ CORRECT: This sample is truly normal")
    else:
        print("   ⚠️  INCORRECT: This sample is truly normal but predicted as attack")
else:
    print(f"❌ Prediction failed: {response.status_code}")

# Test attack
print("\n" + "=" * 80)
print("Testing: Attack (Real Validation Sample)")
print("=" * 80)
response = httpx.post(f"{API_URL}/predict", json=attack_reading)
if response.status_code == 200:
    result = response.json()
    print("✅ Prediction received:")
    print(f"   Classification: {result['classification']}")
    print(f"   Attack Probability: {result['attack_probability']:.4f}")
    print(f"   Confidence: {result['confidence']:.4f}")

    # Check if correct
    if result["classification"] == "Attack":
        print("   ✅ CORRECT: This sample is truly an attack")
    else:
        print("   ⚠️  INCORRECT: This sample is truly an attack but predicted as normal")
else:
    print(f"❌ Prediction failed: {response.status_code}")

print("\n" + "=" * 80)
print("Testing complete!")
print("=" * 80)
