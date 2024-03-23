from pydantic import BaseModel


class FactsResponse(BaseModel):
    status: bool = False
    text: str = "Fact not found"


class ChatResponse:
    companion = None
    message_start_id: int = 0

    # This crutch here just because companion must be User
    # ..but this User class is from the methods.user
    # ..so when I'm import user, it throws "circular import"
    # Need fix to get rid of this shit.
    def __init__(self, *, companion=None, message_start_id: int = 0) -> None:
        self.companion = companion
        self.message_start_id = message_start_id
