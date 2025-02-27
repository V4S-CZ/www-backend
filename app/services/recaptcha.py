"""Google ReCaptcha service"""
from fastapi import HTTPException

import os
import requests

RECAPTCHA_SECRET = os.getenv("RECAPTCHA_SECRET")


def verify_recaptcha(token: str):
    response = requests.post(
        "https://www.google.com/recaptcha/api/siteverify",
        data={"secret": RECAPTCHA_SECRET, "response": token}
    )
    result = response.json()
    if not result.get("success") or result.get("score", 0) < 0.5:
        raise HTTPException(
            status_code=400,
            detail="Invalid reCAPTCHA"
        )
    return True
