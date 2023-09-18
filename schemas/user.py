from pydantic import BaseModel


class User(BaseModel):
    """_summary_

    Args:
        BaseModel (_type_): _description_
    """
    email: str
    password: str