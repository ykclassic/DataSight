# app/main.py
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from app.api.upload import router as upload_router

app = FastAPI(title="DataSight")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(upload_router, prefix="/api")


@app.get("/", response_class=HTMLResponse)
async def dashboard():
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>DataSight Dashboard</title>
    </head>
    <body>
        <h2>Upload SQLite Databases</h2>
        <form id="uploadForm">
            <input type="file" id="files" multiple />
            <button type="submit">Analyze</button>
        </form>
        <pre id="output"></pre>

        <script>
            document.getElementById('uploadForm').onsubmit = async function(e) {
                e.preventDefault();
                const files = document.getElementById('files').files;
                const formData = new FormData();

                for (let i = 0; i < files.length; i++) {
                    formData.append("files", files[i]);
                }

                const response = await fetch("/api/upload", {
                    method: "POST",
                    body: formData
                });

                const text = await response.text();
                document.getElementById("output").textContent = text;
            };
        </script>
    </body>
    </html>
    """
