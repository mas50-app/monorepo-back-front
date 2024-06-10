from typing import Optional
from pydantic import BaseModel


class PaymentCreate(BaseModel):
    amount: int = 1000
    apiKey: str = "API_KEY"
    commerceOrder: str = "12345"
    currency: str = "CLP"
    email: str = "pagos@mas50.cl"
    merchantId: Optional[str] = None
    optional: Optional[str] = None
    # payment_currency: str = "CLP"
    payment_method: int = 9
    subject: str = ""
    timeout: Optional[int] = None
    urlConfirmation: str = "https://www.google.com"
    urlReturn: str = "https://www.google.com"
    s: str = ""


class RefundCreate(BaseModel):
    amount: int = 1000
    apiKey: str = ""
    commerceTrxId: str = ""
    flowTrxId: str = ""
    receiverEmail: str = ""
    refundCommerceOrder: str = ""
    urlCallBack: str = ""
    s: str = ""
