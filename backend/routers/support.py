from fastapi import APIRouter

from schemas.support import (
    ContactSupportRequest,
    ContactSupportResponse,
)

from services.support_service import (
    contact_support_service,
)

router = APIRouter(
    prefix="/support",
    tags=["Support"],
)


@router.post(
    "/contact",
    response_model=ContactSupportResponse,
)
def contact_support(
    request: ContactSupportRequest,
):

    return contact_support_service(request)