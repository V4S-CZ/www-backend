from fastapi import APIRouter  # , HTTPException
from app.services import mail as mail_service
from app.services import recaptcha
from app.schemas.forms import ContactFormInput, FormResponse


router = APIRouter(
    prefix="/forms",
    tags=["forms"],
    # dependencies=[Depends(get_token_header)],
    responses={404: {"description": "Not found"}},
)


@router.post("/contact", response_model=FormResponse)
def contact_form(
    data: ContactFormInput
):
    valid_captcha = recaptcha.verify_recaptcha(data.recaptcha_token)
    if not valid_captcha:
        return {
            "status": "Invalid captcha"
        }
    client = mail_service.get_mail_client()
    client.send(
        subject="Contact form",
        sender=mail_service.get_default_sender(),
        receivers=["v4s@lukasmatuska.cz", "lmatuska@v4s.cz"],
        text=f"Name: \"{data.name}\"\nE-mail: \"{data.email}\"\nMessage:\n{data.message}",
    )
    return {"status": "ok"}
