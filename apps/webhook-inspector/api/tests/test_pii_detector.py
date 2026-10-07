"""
Tests for PII Detection Module
"""

import pytest
from pii_detector import PIIDetector, PIIDetectionResult


@pytest.fixture
def detector():
    return PIIDetector()


class TestSSNDetection:
    """Test Social Security Number detection"""

    def test_detects_formatted_ssn(self, detector):
        payload = {"ssn": "123-45-6789"}
        result = detector.detect(payload)

        assert result.has_pii is True
        assert "ssn" in result.pii_types
        assert result.risk_level == "critical"
        assert len(result.matches) == 1
        assert result.matches[0].masked_value == "***-**-6789"

    def test_detects_ssn_without_dashes(self, detector):
        payload = {"social_security": "123456789"}
        result = detector.detect(payload)

        assert result.has_pii is True
        assert "ssn" in result.pii_types

    def test_rejects_invalid_ssn_patterns(self, detector):
        # All zeros in area
        payload = {"data": "000-45-6789"}
        result = detector.detect(payload)
        assert result.has_pii is False

        # All same digits
        payload = {"data": "111-11-1111"}
        result = detector.detect(payload)
        assert result.has_pii is False

    def test_detects_ssn_in_nested_json(self, detector):
        payload = {
            "customer": {
                "personal": {
                    "ssn": "123-45-6789"
                }
            }
        }
        result = detector.detect(payload)

        assert result.has_pii is True
        assert result.matches[0].location == "customer.personal.ssn"


class TestSINDetection:
    """Test Social Insurance Number (Canadian) detection"""

    def test_detects_formatted_sin(self, detector):
        payload = {"sin": "123-456-789"}
        result = detector.detect(payload)

        assert result.has_pii is True
        assert "sin" in result.pii_types
        assert result.risk_level == "critical"

    def test_detects_sin_without_dashes(self, detector):
        payload = {"social_insurance": "123456789"}
        result = detector.detect(payload)

        assert result.has_pii is True
        assert "sin" in result.pii_types


class TestCreditScoreDetection:
    """Test credit score detection"""

    def test_detects_credit_score_with_label(self, detector):
        payload = {"credit_score": "720"}
        result = detector.detect(payload)

        assert result.has_pii is True
        assert "credit_score" in result.pii_types
        assert result.risk_level == "high"
        assert result.matches[0].masked_value == "***"

    def test_detects_fico_score(self, detector):
        payload = {"fico": "credit_score: 680"}
        result = detector.detect(payload)

        assert result.has_pii is True
        assert "credit_score" in result.pii_types

    def test_rejects_invalid_credit_scores(self, detector):
        # Too low
        payload = {"score": "250"}
        result = detector.detect(payload)
        assert "credit_score" not in result.pii_types

        # Too high
        payload = {"score": "900"}
        result = detector.detect(payload)
        assert "credit_score" not in result.pii_types


class TestEmailDetection:
    """Test email address detection"""

    def test_detects_email(self, detector):
        payload = {"email": "customer@example.com"}
        result = detector.detect(payload)

        assert result.has_pii is True
        assert "email" in result.pii_types
        assert result.matches[0].masked_value == "***@example.com"

    def test_detects_multiple_emails(self, detector):
        payload = {
            "primary": "john@test.com",
            "secondary": "jane@test.com"
        }
        result = detector.detect(payload)

        assert result.has_pii is True
        assert len(result.matches) == 2


class TestPhoneDetection:
    """Test phone number detection"""

    def test_detects_formatted_phone(self, detector):
        payload = {"phone": "(555) 123-4567"}
        result = detector.detect(payload)

        assert result.has_pii is True
        assert "phone" in result.pii_types
        assert result.matches[0].masked_value == "***-***-4567"

    def test_detects_phone_with_country_code(self, detector):
        payload = {"mobile": "+1-555-123-4567"}
        result = detector.detect(payload)

        assert result.has_pii is True
        assert "phone" in result.pii_types

    def test_detects_phone_without_formatting(self, detector):
        payload = {"contact": "5551234567"}
        result = detector.detect(payload)

        assert result.has_pii is True
        assert "phone" in result.pii_types


class TestLoanAmountDetection:
    """Test loan amount detection"""

    def test_detects_loan_amount_with_commas(self, detector):
        payload = {"loan_amount": "$25,000.00"}
        result = detector.detect(payload)

        assert result.has_pii is True
        assert "loan_amount" in result.pii_types
        assert result.risk_level == "high"
        assert result.matches[0].masked_value == "$***"

    def test_detects_loan_amount_without_dollar_sign(self, detector):
        payload = {"principal": "loan_amount: 50000"}
        result = detector.detect(payload)

        assert result.has_pii is True
        assert "loan_amount" in result.pii_types

    def test_rejects_small_amounts(self, detector):
        # Less than $1,000 not considered a loan
        payload = {"amount": "500"}
        result = detector.detect(payload)
        assert "loan_amount" not in result.pii_types


class TestRiskLevelCalculation:
    """Test risk level calculation"""

    def test_critical_risk_with_ssn(self, detector):
        payload = {"ssn": "123-45-6789"}
        result = detector.detect(payload)

        assert result.risk_level == "critical"

    def test_critical_risk_with_multiple_high(self, detector):
        payload = {
            "credit_score": "720",
            "loan_amount": "$50,000"
        }
        result = detector.detect(payload)

        assert result.risk_level == "critical"

    def test_high_risk_with_single_high(self, detector):
        payload = {"credit_score": "680"}
        result = detector.detect(payload)

        assert result.risk_level == "high"

    def test_medium_risk_with_only_medium(self, detector):
        payload = {"email": "test@example.com"}
        result = detector.detect(payload)

        assert result.risk_level == "medium"


class TestComplexPayloads:
    """Test detection in complex real-world payloads"""

    def test_detects_multiple_pii_types(self, detector):
        payload = {
            "applicant": {
                "ssn": "123-45-6789",
                "email": "john@example.com",
                "phone": "555-123-4567",
                "credit_score": "720"
            },
            "loan": {
                "amount": "$35,000.00"
            }
        }
        result = detector.detect(payload)

        assert result.has_pii is True
        assert len(result.pii_types) == 5
        assert result.risk_level == "critical"
        assert len(result.matches) >= 5

    def test_detects_pii_in_string_payload(self, detector):
        payload = "Customer SSN: 123-45-6789, Credit Score: 720"
        result = detector.detect(payload)

        assert result.has_pii is True
        assert "ssn" in result.pii_types
        assert "credit_score" in result.pii_types

    def test_detects_pii_in_array(self, detector):
        payload = {
            "customers": [
                {"email": "customer1@test.com"},
                {"email": "customer2@test.com"}
            ]
        }
        result = detector.detect(payload)

        assert result.has_pii is True
        assert len(result.matches) == 2

    def test_no_pii_in_clean_payload(self, detector):
        payload = {
            "order_id": "12345",
            "product": "Widget",
            "quantity": 10,
            "status": "pending"
        }
        result = detector.detect(payload)

        assert result.has_pii is False
        assert len(result.matches) == 0
        assert result.risk_level == "low"


class TestConfidenceScoring:
    """Test confidence level calculation"""

    def test_high_confidence_with_matching_field_name(self, detector):
        payload = {"ssn": "123-45-6789"}
        result = detector.detect(payload)

        assert result.matches[0].confidence == "high"

    def test_medium_confidence_without_context(self, detector):
        payload = {"data": "123-45-6789"}
        result = detector.detect(payload)

        assert result.matches[0].confidence == "medium"


class TestMasking:
    """Test PII masking"""

    def test_masks_ssn_showing_last_4(self, detector):
        masked = detector.mask_value("123-45-6789", "ssn")
        assert masked == "***-**-6789"

    def test_masks_credit_score_completely(self, detector):
        masked = detector.mask_value("720", "credit_score")
        assert masked == "***"

    def test_masks_email_showing_domain(self, detector):
        masked = detector.mask_value("john@example.com", "email")
        assert masked == "***@example.com"

    def test_masks_phone_showing_last_4(self, detector):
        masked = detector.mask_value("555-123-4567", "phone")
        assert masked == "***-***-4567"

    def test_masks_loan_amount(self, detector):
        masked = detector.mask_value("$50,000", "loan_amount")
        assert masked == "$***"


@pytest.mark.integration
class TestIntegration:
    """Integration tests with realistic webhook data"""

    def test_dealership_loan_application_webhook(self, detector):
        """Simulate webhook from loan application system"""
        webhook_data = {
            "event": "application_submitted",
            "timestamp": "2024-10-06T10:30:00Z",
            "application": {
                "id": "APP-12345",
                "customer": {
                    "first_name": "John",
                    "last_name": "Doe",
                    "ssn": "123-45-6789",
                    "email": "john.doe@email.com",
                    "phone": "(555) 123-4567"
                },
                "credit": {
                    "score": 720,
                    "bureau": "Equifax"
                },
                "loan": {
                    "amount": 35000.00,
                    "term_months": 60,
                    "purpose": "auto"
                }
            }
        }

        result = detector.detect(webhook_data)

        assert result.has_pii is True
        assert result.risk_level == "critical"
        assert "ssn" in result.pii_types
        assert "credit_score" in result.pii_types
        assert "email" in result.pii_types
        assert "phone" in result.pii_types

        # Verify masking
        ssn_match = [m for m in result.matches if m.pii_type == "ssn"][0]
        assert ssn_match.masked_value == "***-**-6789"
