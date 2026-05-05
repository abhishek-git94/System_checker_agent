# features/lab_report.py
import re
from dataclasses import dataclass
from typing import List, Optional

@dataclass
class LabValue:
    name: str
    value: float
    unit: str
    normal_range: str
    is_abnormal: bool
    severity: str

BLOOD_TEST_RANGES = {
    "hemoglobin": (12.0, 17.5, "g/dL"),
    "hb": (12.0, 17.5, "g/dL"),
    "rbc": (4.5, 6.5, "million/cmm"),
    "wbc": (4000, 11000, "/cmm"),
    "platelets": (150000, 450000, "/cmm"),
    "neutrophils": (40, 80, "%"),
    "lymphocytes": (20, 40, "%"),
    "eosinophils": (1, 6, "%"),
    "monocytes": (2, 10, "%"),
    "basophils": (0, 1, "%"),
    "fasting sugar": (70, 100, "mg/dL"),
    "blood sugar": (70, 100, "mg/dL"),
    "hba1c": (4.0, 5.6, "%"),
    "urea": (15, 45, "mg/dL"),
    "creatinine": (0.6, 1.2, "mg/dL"),
    "uric acid": (3.5, 7.2, "mg/dL"),
    "cholesterol": (0, 200, "mg/dL"),
    "triglycerides": (0, 150, "mg/dL"),
    "hdl": (40, 60, "mg/dL"),
    "ldl": (0, 100, "mg/dL"),
    "bilirubin": (0.2, 1.2, "mg/dL"),
    "sgot": (0, 40, "U/L"),
    "sgpt": (0, 40, "U/L"),
    "alkaline phosphatase": (20, 140, "U/L"),
    "total protein": (6.0, 8.3, "g/dL"),
    "albumin": (3.5, 5.5, "g/dL"),
    "tsh": (0.4, 4.0, "mIU/L"),
    "t3": (0.8, 2.0, "ng/dL"),
    "t4": (5.0, 12.0, "µg/dL"),
    "iron": (60, 170, "µg/dL"),
    "ferritin": (20, 200, "ng/mL"),
    "vitamin d": (30, 100, "ng/mL"),
    "vitamin b12": (200, 900, "pg/mL"),
    "sodium": (135, 145, "mEq/L"),
    "potassium": (3.5, 5.0, "mEq/L"),
    "chloride": (96, 106, "mEq/L"),
    "calcium": (8.5, 10.5, "mg/dL"),
}

def parse_lab_report(text: str) -> List[LabValue]:
    results = []
    text_lower = text.lower()
    
    for test_name, (min_val, max_val, unit) in BLOOD_TEST_RANGES.items():
        if test_name in text_lower:
            pattern = rf"{test_name}[^\d]*([0-9.]+)"
            match = re.search(pattern, text_lower)
            if match:
                value = float(match.group(1))
                is_abnormal = value < min_val or value > max_val
                
                if is_abnormal:
                    if test_name in ["wbc", "platelets"] and value < min_val:
                        severity = "high"
                    elif value < min_val:
                        severity = "low"
                    else:
                        severity = "high"
                else:
                    severity = "normal"
                
                results.append(LabValue(
                    name=test_name.title(),
                    value=value,
                    unit=unit,
                    normal_range=f"{min_val}-{max_val}",
                    is_abnormal=is_abnormal,
                    severity=severity
                ))
    
    return results

def analyze_lab_report(report_text: str) -> str:
    values = parse_lab_report(report_text)
    
    if not values:
        return "Mujhe report mein koi values nahi mili. Kripya report check karo ya values manually likho."
    
    abnormal = [v for v in values if v.is_abnormal]
    normal = [v for v in values if not v.is_abnormal]
    
    response = "📋 **Lab Report Analysis:**\n\n"
    
    if normal:
        response += "✅ **Normal Values:**\n"
        for v in normal:
            response += f"- {v.name}: {v.value} {v.unit} (Normal: {v.normal_range})\n"
        response += "\n"
    
    if abnormal:
        response += "⚠️ **Abnormal Values:**\n"
        for v in abnormal:
            status = "🟡 Low" if v.value < float(v.normal_range.split('-')[0]) else "🔴 High"
            response += f"- {v.name}: {v.value} {v.unit} - {status} (Normal: {v.normal_range})\n"
        response += "\n"
    
    response += "💊 **Suggestions:**\n"
    if abnormal:
        response += "- In abnormal values ke liye doctor se zaroor consult karo\n"
        response += "- Koi bhi medicine self nahi lena\n"
    else:
        response += "- Sab values normal hain, par regular checkup zarur karo\n"
    
    response += "\n⚠️ Ye analysis sirf informativo hai. Doctor se zaroor milo!"
    
    return response