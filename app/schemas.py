from pydantic import BaseModel, ConfigDict

class OrderSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    number: int
    client: str
    value: float