from fastapi import APIRouter  # , HTTPException
from app.services import mail as mail_service
from app.schemas.forms import ContactFormInput, FormResponse


router = APIRouter(
    prefix="/forms",
    tags=["forms"],
    # dependencies=[Depends(get_token_header)],
    responses={404: {"description": "Not found"}},
)


@router.post("/contact", response_model=FormResponse)
def contact_form(data: ContactFormInput):
    client = mail_service.get_mail_client()
    client.send(
        subject="Contact form",
        sender=mail_service.get_default_sender(),
        receivers=["matuska.lukas@lukasmatuska.cz"],
        text=f"Name: \"{data.name}\"\nE-mail: \"{data.email}\"\nMessage:\n{data.message}",
    )
    return {"status": "ok"}
