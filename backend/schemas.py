from datetime import datetime, timezone
from typing import Optional
from pydantic import BaseModel, Field, model_validator

PLATFORMS = ["Instagram", "X (Twitter)", "Facebook", "Email", "TikTok", "Telegram"]

DAILY_TARGETS = {
    "Instagram": 30,
    "X (Twitter)": 30,
    "Facebook": 30,
    "Email": 40,
    "TikTok": 30,
    "Telegram": 50,
}


class DraftRequest(BaseModel):
    business_name: str = Field(..., description="Name of the business/organization")
    industry: str = Field(..., description="What they do, e.g. 'boutique clothing store'")
    city: str = Field(..., description="City the business is in")
    platform: str = Field(..., description="Which platform this message is for")
    notes: Optional[str] = Field(default=None, description="Anything specific you noticed about them, to personalize the message")


class DraftResponse(BaseModel):
    message: str
    platform: str


class LogEntryIn(BaseModel):
    business_name: str
    platform: str
    city: str
    message_sent: str
    date: Optional[str] = None
    response: str = "No response yet"
    notes: Optional[str] = ""

    @model_validator(mode="after")
    def default_date(self):
        if not self.date:
            self.date = datetime.now(timezone.utc).date().isoformat()
        return self


class LogEntryOut(LogEntryIn):
    id: str
