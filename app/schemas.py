from pydantic import BaseModel

class ArithmeticRequest(BaseModel):
    number1: float
    number2: float
    operator: str
    secret_key: str