from fastapi import FastAPI, Query
import httpx
from datetime import datetime

app = FastAPI()

# Track total requests for daily limit (2000 per day)
request_tracker = {
    "date": datetime.now().strftime("%Y-%m-%d"),
    "count": 0
}

@app.get("/numinfo/api")
@app.get("/api/index")
async def num_info(
    key: str = Query("FREE", description="API Key"),
    query: str = Query(..., description="Query / Phone Number / Email")
):
    current_date = datetime.now().strftime("%Y-%m-%d")
    
    # Reset daily count if date changes
    if request_tracker["date"] != current_date:
        request_tracker["date"] = current_date
        request_tracker["count"] = 0

    # Increment request count
    request_tracker["count"] += 1
    current_today_used = request_tracker["count"]

    # Check API Expiry Date (Expiry: 2026-09-29)
    expiry_date = datetime.strptime("2026-09-29", "%Y-%m-%d").date()
    today_date = datetime.now().date()

    if today_date > expiry_date:
        return {
            "developer": "@coderpetro",
            "expiry": "2026-09-29",
            "query": query,
            "result": "API expired, contact admin @coderpetro"
        }

    # Check Daily Limit (2000 requests)
    if current_today_used > 2000:
        return {
            "developer": "@coderpetro",
            "expiry": "2026-09-29",
            "query": query,
            "result": "daily limit 2000"
        }

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
                backend_data["API_Developer"] = "@coderpetro"
                if "Today_Used" in backend_data:
                    backend_data["Today_Used"] = current_today_used

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
