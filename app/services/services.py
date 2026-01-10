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
                  "error":"request Timed out"
           }
    except httpx.HTTPStatusError as e:
           return{
                  "url":url,
                  "status": False,
                  "error":f"http error{e.response.status_code}"
           }
    except httpx.NetworkError as e:
           return{
                "url":url,
                "status": False,
                "error":f"Network Error {str(e)}"
                  
           }
    except Exception as e:
            return {
                "url": url,
                "status": False,
                "error":f"unexpected error{str(e)}"
            }

