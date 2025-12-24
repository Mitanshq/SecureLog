import random
from typing import Dict
import os

MODEL_VERSION = os.getenv('MODEL_VERSION')

def classify_log(text: str) -> Dict:
    
    if not text:
        return {
            'classification': 'unknown',
            'confidence': 0.0,
            'risk_level': 'low',
            'Model Version': MODEL_VERSION
        }
        
    text_lower = text.lower()
    
    if any(word in text_lower for word in ["scam", "phishing", "malware", "attack"]):
        classification = "malicious"
        confidence = round(random.uniform(0.90, 0.99), 2)
        risk_level = "high"

    elif any(word in text_lower for word in ["ads", "tracking", "popup"]):
        classification = "useless"
        confidence = round(random.uniform(0.80, 0.90), 2)
        risk_level = "low"

    else:
        classification = "genuine"
        confidence = round(random.uniform(0.90, 0.99), 2)
        risk_level = "low"

    return {
        "classification": classification,
        "confidence": confidence,
        "risk_level": risk_level,
        "model_version": MODEL_VERSION
    }
