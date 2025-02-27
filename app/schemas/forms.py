from pydantic import BaseModel, EmailStr


class ContactFormInput(BaseModel):
    name: str
    email: EmailStr
    message: str
    recaptcha_token: str

    class Config:
        from_attributes = True


class FormResponse(BaseModel):
    status: str

    class Config:
        from_attributes = True
