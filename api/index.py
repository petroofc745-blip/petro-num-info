from fastapi import FastAPI, Query
import httpx
from datetime import datetime

app = FastAPI()

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
    
    if request_tracker["date"] != current_date:
        request_tracker["date"] = current_date
        request_tracker["count"] = 0

    if request_tracker["count"] >= 2000:
        return {
            "developer": "@coderpetro",
            "expiry": "2026-09-29",
            "query": query,
            "result": "Daily limit of 2000 requests exceeded. Try again tomorrow."
        }

    request_tracker["count"] += 1
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

            if not backend_data or (isinstance(backend_data, dict) and len(backend_data) == 0):
                return {
                    "developer": "@coderpetro",
                    "expiry": "2026-09-29",
                    "query": query,
                    "result": "No data found"
                }

            # Backend-ൽ നിന്ന് വരുന്ന result ഒരു dict ആണെങ്കിൽ അതിലുള്ള 'API_Developer' നീക്കം ചെയ്യാം
            if isinstance(backend_data, dict):
                backend_data.pop("API_Developer", None)
                # അല്ലെങ്കിൽ 'result' എന്ന കീയ്ക്കുള്ളിൽ ആണെങ്കിൽ:
                if "result" in backend_data and isinstance(backend_data["result"], dict):
                    backend_data["result"].pop("API_Developer", None)

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
