"""
Unit tests for PII masking/detection patterns
Critical for compliance features
"""
import pytest
from main import mask_sensitive_data


@pytest.mark.unit
@pytest.mark.compliance
class TestPIIMasking:
    """Test PII detection and masking patterns"""

    def test_ssn_masking(self):
        """Test SSN masking (US Social Security Number)"""
        text = "Customer SSN: 123-45-6789 should be masked"
        masked = mask_sensitive_data(text)

        assert "123-45-6789" not in masked
        assert "***-**-6789" in masked
        assert "should be masked" in masked  # Other text unchanged

    def test_ssn_without_dashes(self):
        """Test SSN without dashes"""
        text = "SSN: 123456789"
        masked = mask_sensitive_data(text)

        assert "123456789" not in masked

    def test_credit_card_masking(self):
        """Test credit card masking"""
        text = "Card: 1234-5678-9012-3456"
        masked = mask_sensitive_data(text)

        assert "1234-5678-9012-3456" not in masked
        assert "****-****-****-3456" in masked

    def test_email_masking(self):
        """Test email masking"""
        text = "Contact: john.doe@example.com for info"
        masked = mask_sensitive_data(text)

        assert "john.doe@example.com" not in masked
        assert "j***@example.com" in masked
        assert "example.com" in masked  # Domain kept for context

    def test_phone_masking(self):
        """Test phone number masking"""
        text = "Call (555) 123-4567 for support"
        masked = mask_sensitive_data(text)

        assert "(555) 123-4567" not in masked
        assert "(***) ***-4567" in masked

    def test_multiple_pii_types(self):
        """Test multiple PII types in same text"""
        text = """
        Customer Info:
        SSN: 987-65-4321
        Email: customer@example.com
        Phone: (555) 999-8888
        """
        masked = mask_sensitive_data(text)

        # All PII should be masked
        assert "987-65-4321" not in masked
        assert "***-**-4321" in masked
        assert "customer@example.com" not in masked
        assert "c***@example.com" in masked
        assert "(555) 999-8888" not in masked
        assert "(***) ***-8888" in masked

    def test_no_pii_unchanged(self):
        """Test that text without PII is unchanged"""
        text = "Just a normal message with no sensitive data"
        masked = mask_sensitive_data(text)

        assert masked == text

    def test_json_with_pii(self):
        """Test PII masking in JSON-like text"""
        import json

        payload = {
            "ssn": "111-22-3333",
            "email": "test@example.com",
            "message": "Normal text"
        }
        text = json.dumps(payload)
        masked = mask_sensitive_data(text)

        assert "111-22-3333" not in masked
        assert "test@example.com" not in masked
        assert "Normal text" in masked

    def test_empty_text(self):
        """Test masking with empty/None text"""
        assert mask_sensitive_data("") == ""
        assert mask_sensitive_data(None) is None

    def test_credit_score_pattern(self):
        """Test that credit scores (300-850) are NOT masked by card pattern"""
        text = "Credit score: 720 is good"
        masked = mask_sensitive_data(text)

        # Credit score should remain (it's not a card number)
        assert "720" in masked


@pytest.mark.unit
@pytest.mark.compliance
class TestPIIDetectionPatterns:
    """Test patterns that will be used for PII detection (not just masking)"""

    def test_ssn_pattern_matches(self):
        """Test SSN regex pattern"""
        import re

        ssn_pattern = r'\b\d{3}-\d{2}-\d{4}\b'

        assert re.search(ssn_pattern, "SSN: 123-45-6789")
        assert re.search(ssn_pattern, "123-45-6789")
        assert not re.search(ssn_pattern, "12-345-6789")  # Wrong format

    def test_sin_pattern_matches(self):
        """Test SIN (Canadian) pattern"""
        import re

        sin_pattern = r'\b\d{3}-\d{3}-\d{3}\b'

        assert re.search(sin_pattern, "SIN: 123-456-789")
        assert re.search(sin_pattern, "123-456-789")

    def test_credit_score_pattern_matches(self):
        """Test credit score pattern (300-850)"""
        import re

        # Credit scores are 300-850
        credit_pattern = r'\b[3-8]\d{2}\b'

        assert re.search(credit_pattern, "Score: 720")
        assert re.search(credit_pattern, "300")  # Min
        assert re.search(credit_pattern, "850")  # Max
        assert not re.search(credit_pattern, "999")  # Too high
        assert not re.search(credit_pattern, "200")  # Too low

    def test_email_pattern_matches(self):
        """Test email pattern"""
        import re

        email_pattern = r'\b[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}\b'

        assert re.search(email_pattern, "test@example.com")
        assert re.search(email_pattern, "user.name+tag@example.co.uk")
        assert not re.search(email_pattern, "@example.com")  # Missing username

    def test_vin_pattern_matches(self):
        """Test VIN (Vehicle Identification Number) pattern"""
        import re

        # VIN is 17 characters, no I, O, Q
        vin_pattern = r'\b[A-HJ-NPR-Z0-9]{17}\b'

        assert re.search(vin_pattern, "1HGCM82633A123456")
        assert len("1HGCM82633A123456") == 17
        assert not re.search(vin_pattern, "1HGCM82633A12345")  # Too short
