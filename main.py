from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from user_routes import router as user_router
from event_routes import router as event_router
from qr_routes import router as qr_router

app = FastAPI()

app.include_router(user_router, prefix="/api")
app.include_router(event_router, prefix="/api")
app.include_router(qr_router, prefix="/api")

@app.get("/", response_class=HTMLResponse)
async def home():
    return """
    <h1>Event Check-In System</h1>
    <h3>Follow these steps:</h3>
    <ol>
        <li>Register at <code>/api/register</code></li>
        <li>Login at <code>/api/login</code></li>
        <li>Browse events at <code>/api/events</code></li>
        <li>Register for event at <code>/api/events/register</code></li>
        <li>Get QR code at <code>/api/qrcode</code></li>
    </ol>
    """