from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
import google.generativeai as genai

# Configure API key and model
genai.configure(api_key="")
model = genai.GenerativeModel("gemini-1.5-flash")

# Initialize FastAPI app
app = FastAPI()
templates = Jinja2Templates(directory="templates")


# Home Route
@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


# Pydantic model for input
class TranslationRequest(BaseModel):
    text: str  # Text to translate
    source: str  # Source Language code
    target: str  # Target Language code


# Translation Route
@app.post("/api/translate")
async def translate_text(request: TranslationRequest):
    try:
        input_text = request.text
        source_lang = request.source
        target_lang = request.target

        # Call Gemini Flash api
        prompt = f"Translate the following text from {source_lang} to {target_lang}: {input_text}\nPlease note: Only respond with the translated text."
        response = model.generate_content(prompt)
        translation = response.text
        print(translation)

        return {"translation": translation}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to translate: {str(e)}")
