from fastapi import FastAPI, Query
import httpx
from datetime import datetime

app = FastAPI()

# Track total requests processed by your Vercel API
total_api_counter = 0

@app.get("/numinfo/api")
@app.get("/api/index")
async def num_info(
    key: str = Query("FREE", description="API Key"),
    query: str = Query(..., description="Query / Phone Number")
):
    global total_api_counter
    total_api_counter += 1

    backend_key = "osintbyabhigyan" if key == "FREE" else key
    target_url = f"https://paid.originalapis.workers.dev/leak?key={backend_key}&query={query}"
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Referer": "https://paid.originalapis.workers.dev/"
    }

    try:
        async with httpx.AsyncClient(timeout=8.0) as client:
            response = await client.get(target_url, headers=headers)
            
            if response.status_code != 200:
                return {
                    "developer": "@coderpetro",
                    "expiry": "2026-09-29",
                    "query": query,
                    "result": "No data found"
                }
            
            try:
                backend_data = response.json()
            except Exception:
                backend_data = {}

            if isinstance(backend_data, dict):
                # Mask API_Developer to your custom handle
                backend_data["API_Developer"] = "@coderpetro"
                
                # Replace Today_Used with your own local counter from requests
                if "Today_Used" in backend_data:
                    backend_data["Today_Used"] = total_api_counter

            return {
                "developer": "@coderpetro",
                "expiry": "2026-09-29",
                "query": query,
                "result": backend_data
            }

    except httpx.TimeoutException:
        return {
            "developer": "@coderpetro",
            "expiry": "2026-09-29",
            "query": query,
            "result": "Timeout, refresh again"
        }
        
    except Exception as e:
        return {
            "developer": "@coderpetro",
            "expiry": "2026-09-29",
            "query": query,
            "result": "No data found"
        }
