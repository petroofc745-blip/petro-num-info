from fastapi import FastAPI, Query
import httpx
from datetime import datetime

app = FastAPI()

# Simple In-Memory tracker for daily limit (2000 requests/day)
request_tracker = {
    "date": datetime.now().strftime("%Y-%m-%d"),
    "count": 0
}

@app.get("/numinfo/api")
@app.get("/api/index")
async def num_info(
    key: str = Query(..., description="API Key"),
    query: str = Query(..., description="Query / Phone Number")
):
    current_date = datetime.now().strftime("%Y-%m-%d")
    
    # Reset count if date changes
    if request_tracker["date"] != current_date:
        request_tracker["date"] = current_date
        request_tracker["count"] = 0

    # Check daily limit (2000 requests)
    if request_tracker["count"] >= 2000:
        return {
            "developer": "@coderpetro",
            "expiry": "2026-09-29",
            "query": query,
            "result": "Daily limit of 2000 requests exceeded. Try again tomorrow."
        }

    # Increment request count
    request_tracker["count"] += 1

    # Target backend API URL
    target_url = f"https://paid.originalapis.workers.dev/leak?key={key}&query={query}"
    
    try:
        async with httpx.AsyncClient(timeout=8.0) as client:
            response = await client.get(target_url)
            
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

            # Clean up unwanted metadata fields from the response
            if isinstance(backend_data, dict):
                backend_data.pop("API_Developer", None)
                if "result" in backend_data and isinstance(backend_data["result"], dict):
                    backend_data["result"].pop("API_Developer", None)

            # Check if the inner result is empty or missing data
            inner_result = backend_data.get("result")
            if not backend_data or inner_result == {} or inner_result is None:
                return {
                    "developer": "@coderpetro",
                    "expiry": "2026-09-29",
                    "query": query,
                    "result": "No data found"
                }

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
