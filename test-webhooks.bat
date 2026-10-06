@echo off
REM 🏁 Webhook Pitstop - Test Script (Windows)
REM Send test webhooks to your local instance

REM INSTRUCTIONS:
REM 1. Open http://localhost:8080 in browser
REM 2. Click "Open New Pit Lane"
REM 3. Copy your pit ID from the URL
REM 4. Edit this file and replace YOUR_PIT_ID below
REM 5. Run this script: test-webhooks.bat

SET PIT_ID=YOUR_PIT_ID
SET BASE_URL=http://localhost:8000

echo 🏁 Testing Webhook Pitstop...
echo 📍 Pit ID: %PIT_ID%
echo.

REM Test 1: Simple POST
echo Test 1: Simple POST request...
curl -X POST "%BASE_URL%/pit/%PIT_ID%" -H "Content-Type: application/json" -d "{\"test\": \"simple_post\", \"message\": \"Hello from test script!\"}"
echo.
echo.
timeout /t 1 /nobreak >nul

REM Test 2: Lender Integration
echo Test 2: Simulating HMF lender webhook...
curl -X POST "%BASE_URL%/pit/%PIT_ID%" -H "Content-Type: application/json" -H "X-Lender: HMF" -d "{\"event\": \"credit_decision\", \"dealId\": \"DEAL-2024-001\", \"status\": \"APPROVED\", \"approvedAmount\": 35000, \"apr\": 5.99}"
echo.
echo.
timeout /t 1 /nobreak >nul

REM Test 3: Error Status
echo Test 3: Error status webhook...
curl -X POST "%BASE_URL%/pit/%PIT_ID%" -H "Content-Type: application/json" -d "{\"event\": \"validation_failed\", \"errorCode\": \"INSUFFICIENT_INCOME\", \"dealId\": \"DEAL-2024-002\"}"
echo.
echo.
timeout /t 1 /nobreak >nul

REM Test 4: GET Request
echo Test 4: GET request...
curl -X GET "%BASE_URL%/pit/%PIT_ID%?source=test"
echo.
echo.
timeout /t 1 /nobreak >nul

REM Test 5: PUT Request
echo Test 5: PUT request...
curl -X PUT "%BASE_URL%/pit/%PIT_ID%" -H "Content-Type: application/json" -d "{\"action\": \"update_status\", \"dealId\": \"DEAL-2024-001\"}"
echo.
echo.

echo ✅ All tests completed!
echo 👀 Check your browser at http://localhost:8080 to see the results!
echo.
echo 📊 View diagnostics: %BASE_URL%/api/pit/%PIT_ID%/diagnostics
echo 📋 View all requests: %BASE_URL%/api/pit/%PIT_ID%/requests
echo.
pause
