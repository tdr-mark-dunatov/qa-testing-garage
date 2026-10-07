"""
PII Detection Module - Test Data Compliance Guardian

Scans webhook payloads for sensitive personally identifiable information (PII):
- Social Security Numbers (SSN)
- Social Insurance Numbers (SIN - Canadian)
- Credit scores
- Email addresses
- Phone numbers
- Loan amounts

Returns detected PII types and their locations for alerting and compliance tracking.
"""

import re
import json
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict


@dataclass
class PIIMatch:
    """Represents a detected PII match"""
    pii_type: str
    value: str
    masked_value: str
    location: str
    confidence: str  # "high", "medium", "low"


@dataclass
class PIIDetectionResult:
    """Result of PII detection scan"""
    has_pii: bool
    pii_types: List[str]
    matches: List[PIIMatch]
    risk_level: str  # "critical", "high", "medium", "low"

    def to_dict(self) -> Dict:
        return {
            "has_pii": self.has_pii,
            "pii_types": self.pii_types,
            "matches": [asdict(m) for m in self.matches],
            "risk_level": self.risk_level
        }


class PIIDetector:
    """Detects PII in webhook payloads"""

    # Regex patterns for different PII types
    PATTERNS = {
        "ssn": {
            "pattern": r"\b\d{3}[-\s]?\d{2}[-\s]?\d{4}\b",
            "description": "Social Security Number",
            "risk": "critical"
        },
        "sin": {
            "pattern": r"\b\d{3}[-\s]?\d{3}[-\s]?\d{3}\b",
            "description": "Social Insurance Number (Canadian)",
            "risk": "critical"
        },
        "credit_score": {
            "pattern": r"\b(?:credit[_\s-]?score|fico|score)[\s:=-]*([3-8]\d{2})\b",
            "description": "Credit Score (300-850)",
            "risk": "high"
        },
        "email": {
            "pattern": r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b",
            "description": "Email Address",
            "risk": "medium"
        },
        "phone": {
            "pattern": r"\b(?:\+?1[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}\b",
            "description": "Phone Number",
            "risk": "medium"
        },
        "loan_amount": {
            "pattern": r"\b(?:loan[_\s-]?amount|principal|amount[_\s-]?financed)[\s:=-]*\$?\s*(\d{1,3}(?:,\d{3})*(?:\.\d{2})?)\b",
            "description": "Loan Amount",
            "risk": "high"
        }
    }

    @staticmethod
    def mask_value(value: str, pii_type: str) -> str:
        """Mask PII value for safe display"""
        if pii_type in ["ssn", "sin"]:
            # Show last 4 digits: XXX-XX-1234
            return f"***-**-{value[-4:]}" if len(value) >= 4 else "***"
        elif pii_type == "credit_score":
            # Mask completely: ***
            return "***"
        elif pii_type == "email":
            # Show domain: ***@example.com
            parts = value.split("@")
            if len(parts) == 2:
                return f"***@{parts[1]}"
            return "***"
        elif pii_type == "phone":
            # Show last 4 digits: ***-***-1234
            digits = re.sub(r'\D', '', value)
            return f"***-***-{digits[-4:]}" if len(digits) >= 4 else "***"
        elif pii_type == "loan_amount":
            # Show currency symbol only: $***
            return "$***" if "$" in value else "***"
        return "***"

    @staticmethod
    def flatten_json(data: Any, parent_key: str = "", sep: str = ".") -> Dict[str, str]:
        """Flatten nested JSON for scanning"""
        items = {}
        if isinstance(data, dict):
            for key, value in data.items():
                new_key = f"{parent_key}{sep}{key}" if parent_key else key
                if isinstance(value, (dict, list)):
                    items.update(PIIDetector.flatten_json(value, new_key, sep))
                else:
                    items[new_key] = str(value)
        elif isinstance(data, list):
            for idx, item in enumerate(data):
                new_key = f"{parent_key}[{idx}]"
                if isinstance(item, (dict, list)):
                    items.update(PIIDetector.flatten_json(item, new_key, sep))
                else:
                    items[new_key] = str(item)
        else:
            items[parent_key] = str(data)
        return items

    def detect(self, payload: Any) -> PIIDetectionResult:
        """
        Detect PII in webhook payload

        Args:
            payload: Webhook payload (dict, str, or any JSON-serializable data)

        Returns:
            PIIDetectionResult with detected PII information
        """
        matches: List[PIIMatch] = []

        # Convert payload to searchable format
        if isinstance(payload, str):
            searchable = {"raw": payload}
        elif isinstance(payload, dict):
            searchable = self.flatten_json(payload)
        else:
            try:
                searchable = {"raw": json.dumps(payload)}
            except (TypeError, ValueError):
                searchable = {"raw": str(payload)}

        # Scan each field for PII patterns
        for location, value in searchable.items():
            value_lower = value.lower()

            for pii_type, config in self.PATTERNS.items():
                pattern = config["pattern"]
                flags = re.IGNORECASE if pii_type in ["credit_score", "loan_amount"] else 0

                for match in re.finditer(pattern, value, flags):
                    matched_value = match.group(0)

                    # Additional validation
                    if self._validate_match(pii_type, matched_value, value_lower):
                        confidence = self._calculate_confidence(pii_type, matched_value, location)

                        matches.append(PIIMatch(
                            pii_type=pii_type,
                            value=matched_value,
                            masked_value=self.mask_value(matched_value, pii_type),
                            location=location,
                            confidence=confidence
                        ))

        # Calculate risk level
        risk_level = self._calculate_risk_level(matches)

        # Get unique PII types
        pii_types = list(set([m.pii_type for m in matches]))

        return PIIDetectionResult(
            has_pii=len(matches) > 0,
            pii_types=pii_types,
            matches=matches,
            risk_level=risk_level
        )

    def _validate_match(self, pii_type: str, value: str, context: str) -> bool:
        """Additional validation to reduce false positives"""

        if pii_type == "ssn":
            # Remove formatting
            digits = re.sub(r'\D', '', value)
            # Must be exactly 9 digits
            if len(digits) != 9:
                return False
            # Check for invalid patterns (000-xx-xxxx, xxx-00-xxxx, etc.)
            if digits[:3] == "000" or digits[3:5] == "00" or digits[5:] == "0000":
                return False
            # Check for sequential/repeated digits (111-11-1111)
            if len(set(digits)) == 1:
                return False
            return True

        elif pii_type == "sin":
            # Similar validation for Canadian SIN
            digits = re.sub(r'\D', '', value)
            if len(digits) != 9:
                return False
            if digits[:3] == "000" or len(set(digits)) == 1:
                return False
            return True

        elif pii_type == "credit_score":
            # Extract numeric value
            score_match = re.search(r'([3-8]\d{2})', value)
            if score_match:
                score = int(score_match.group(1))
                # Valid range: 300-850
                return 300 <= score <= 850
            return False

        elif pii_type == "phone":
            # Must have 10 digits
            digits = re.sub(r'\D', '', value)
            return len(digits) == 10 or len(digits) == 11  # With/without country code

        elif pii_type == "loan_amount":
            # Must be a reasonable loan amount (> $1,000)
            amount_match = re.search(r'(\d{1,3}(?:,\d{3})*(?:\.\d{2})?)', value)
            if amount_match:
                amount_str = amount_match.group(1).replace(",", "")
                try:
                    amount = float(amount_str)
                    return amount >= 1000  # Minimum $1,000 to be considered a loan
                except ValueError:
                    return False
            return False

        return True

    def _calculate_confidence(self, pii_type: str, value: str, location: str) -> str:
        """Calculate confidence level for detection"""
        location_lower = location.lower()

        # High confidence indicators in field names
        high_confidence_keys = {
            "ssn": ["ssn", "social_security", "socialsecurity"],
            "sin": ["sin", "social_insurance"],
            "credit_score": ["credit_score", "fico", "score"],
            "email": ["email", "email_address"],
            "phone": ["phone", "telephone", "mobile", "cell"],
            "loan_amount": ["loan_amount", "principal", "amount"]
        }

        # Check if location suggests high confidence
        if pii_type in high_confidence_keys:
            for keyword in high_confidence_keys[pii_type]:
                if keyword in location_lower:
                    return "high"

        # Medium confidence for formatted values
        if pii_type in ["ssn", "sin", "phone"] and ("-" in value or " " in value):
            return "medium"

        return "medium"

    def _calculate_risk_level(self, matches: List[PIIMatch]) -> str:
        """Calculate overall risk level based on detected PII"""
        if not matches:
            return "low"

        # Count by risk type
        critical_count = sum(1 for m in matches if self.PATTERNS[m.pii_type]["risk"] == "critical")
        high_count = sum(1 for m in matches if self.PATTERNS[m.pii_type]["risk"] == "high")

        if critical_count > 0:
            return "critical"
        elif high_count >= 2:
            return "critical"
        elif high_count > 0:
            return "high"
        else:
            return "medium"
