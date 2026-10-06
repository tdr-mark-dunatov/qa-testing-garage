#!/bin/bash

# 🏁 Webhook Pitstop - Test Script
# Send test webhooks to your local instance

# INSTRUCTIONS:
# 1. Open http://localhost:8080 in browser
# 2. Click "Open New Pit Lane"
# 3. Copy your pit ID from the URL
# 4. Replace YOUR_PIT_ID below with your actual pit ID
# 5. Run this script: bash test-webhooks.sh

PIT_ID="YOUR_PIT_ID"  # REPLACE THIS!
BASE_URL="http://localhost:8000"

echo "🏁 Testing Webhook Pitstop..."
echo "📍 Pit ID: $PIT_ID"
echo ""

# Test 1: Simple POST
echo "Test 1: Simple POST request..."
curl -X POST "$BASE_URL/pit/$PIT_ID" \
  -H "Content-Type: application/json" \
  -d '{
    "test": "simple_post",
    "message": "Hello from test script!"
  }'
echo ""
echo ""

sleep 1

# Test 2: Lender Integration Simulation (HMF)
echo "Test 2: Simulating HMF lender webhook..."
curl -X POST "$BASE_URL/pit/$PIT_ID" \
  -H "Content-Type: application/json" \
  -H "X-Lender: HMF" \
  -H "X-Request-ID: req-12345" \
  -d '{
    "event": "credit_decision",
    "dealId": "DEAL-2024-001",
    "status": "APPROVED",
    "customerName": "John Doe",
    "vehicleVIN": "1HGCM82633A123456",
    "approvedAmount": 35000,
    "apr": 5.99,
    "term": 60,
    "timestamp": "2024-10-06T16:30:00Z"
  }'
echo ""
echo ""

sleep 1

# Test 3: Webhook with Error Status
echo "Test 3: Error status webhook..."
curl -X POST "$BASE_URL/pit/$PIT_ID" \
  -H "Content-Type: application/json" \
  -H "X-Status: ERROR" \
  -d '{
    "event": "validation_failed",
    "errorCode": "INSUFFICIENT_INCOME",
    "errorMessage": "Customer income does not meet minimum requirements",
    "dealId": "DEAL-2024-002"
  }'
echo ""
echo ""

sleep 1

# Test 4: Large Payload
echo "Test 4: Large payload with multiple fields..."
curl -X POST "$BASE_URL/pit/$PIT_ID" \
  -H "Content-Type: application/json" \
  -d '{
    "event": "deal_submitted",
    "dealId": "DEAL-2024-003",
    "customer": {
      "firstName": "Jane",
      "lastName": "Smith",
      "email": "jane.smith@example.com",
      "phone": "+1-555-0123",
      "ssn": "***-**-1234",
      "dateOfBirth": "1985-03-15",
      "address": {
        "street": "123 Main St",
        "city": "Toronto",
        "province": "ON",
        "postalCode": "M5H 2N2"
      }
    },
    "vehicle": {
      "year": 2024,
      "make": "Toyota",
      "model": "Camry",
      "vin": "2T1BURHE8JC123456",
      "price": 32000,
      "mileage": 0
    },
    "financing": {
      "requestedAmount": 30000,
      "downPayment": 2000,
      "term": 72,
      "tradeInValue": 5000
    },
    "timestamp": "2024-10-06T16:35:00Z"
  }'
echo ""
echo ""

sleep 1

# Test 5: GET Request
echo "Test 5: GET request (different method)..."
curl -X GET "$BASE_URL/pit/$PIT_ID?source=test&action=verify"
echo ""
echo ""

sleep 1

# Test 6: PUT Request
echo "Test 6: PUT request (update)..."
curl -X PUT "$BASE_URL/pit/$PIT_ID" \
  -H "Content-Type: application/json" \
  -d '{
    "action": "update_status",
    "dealId": "DEAL-2024-001",
    "newStatus": "FUNDED"
  }'
echo ""
echo ""

sleep 1

# Test 7: Rapid Fire (Multiple Quick Requests)
echo "Test 7: Rapid fire - sending 5 quick requests..."
for i in {1..5}; do
  curl -X POST "$BASE_URL/pit/$PIT_ID" \
    -H "Content-Type: application/json" \
    -d "{\"event\": \"rapid_test\", \"sequence\": $i, \"timestamp\": \"$(date -Iseconds)\"}" &
done
wait
echo ""
echo ""

echo "✅ All tests completed!"
echo "👀 Check your browser at http://localhost:8080 to see the results!"
echo ""
echo "📊 View diagnostics: http://localhost:8000/api/pit/$PIT_ID/diagnostics"
echo "📋 View all requests: http://localhost:8000/api/pit/$PIT_ID/requests"
