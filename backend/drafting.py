"""
Drafts a personalized outreach opener — never sends anything.

The prompt deliberately encodes the brief's own rules (professional greeting,
no link in the first message, identify as a SafeX Solutions intern, keep it
short and low-pressure) so every draft comes out compliant by default, rather
than relying on the person to remember the rules each time.
"""

import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv

load_dotenv()

_llm = None  # created lazily so the rest of the app works even before a key is set


def _get_llm():
    global _llm
    if _llm is None:
        _llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0.6)
    return _llm

PROMPT = ChatPromptTemplate.from_template("""
You draft a single short outreach opener message on behalf of a SafeX Solutions
AI/ML intern named Huma Aslam, reaching out to a real business for the first time.

Hard rules — never break these:
- Do NOT include any link or URL.
- Do NOT mention pricing, contracts, or make exaggerated claims.
- Must clearly identify the sender as an AI/ML intern at SafeX Solutions.
- Must be a genuine, low-pressure, professional greeting — not a sales pitch.
- End with a soft, no-obligation invitation (e.g. a quick intro call), never a hard ask.
- Keep it under 100 words.
- Tone should suit the platform: {platform} (e.g. Email can be slightly more formal;
  Instagram/TikTok/Telegram/X should be a bit more casual but still professional).

Business: {business_name}
Industry: {industry}
City: {city}
Extra context to personalize with (may be empty): {notes}

Write ONLY the message text, nothing else — no subject line, no explanation.
""")


def draft_message(business_name: str, industry: str, city: str, platform: str, notes: str | None) -> str:
    messages = PROMPT.format_messages(
        business_name=business_name,
        industry=industry,
        city=city,
        platform=platform,
        notes=notes or "none",
    )
    response = _get_llm().invoke(messages)
    return response.content.strip()
