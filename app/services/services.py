import httpx


async def url_validation(url,client:httpx.AsyncClient):
    try:   
            response = await client.get(url)

            return {
                "url": url,
                "status_code": response.status_code,
                "elapsed_time": response.elapsed.total_seconds(),
                "Status": response.reason_phrase,
                 "Additional_Info":(
                    "Server_Error" if response.status_code >= 500 else
                    "Client_Error" if response.status_code >= 400 else
                    response.headers.get('location') if response.status_code == 302 else
                    "Success")
            }
    except httpx.TimeoutException:
           return{
                  "url":url,
                  "Status": False,
                  "status_code": "Timeout",
                  "error":"request Timed out"
           }
    except httpx.HTTPStatusError as e:
           return{
                  "url":url,
                  "status": False,
                  "status_code": e.response.status_code,
                  "error":f"http error{e.response.status_code}"
           }
    except httpx.NetworkError as e:
           return{
                "url":url,
                "status": False,
                "status_code": "Network Error",
                "error":f"Network Error {str(e)}"
                  
           }
    except httpx.RequestError as e:
            return {
                "url": url,
                "status": False,
                "status_code": "Unexpected Error",      
                "error":f"unexpected error{str(e)}"
            }

