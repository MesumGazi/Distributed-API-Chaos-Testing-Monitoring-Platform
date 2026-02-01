import pytest
import httpx
from unittest.mock import Mock, AsyncMock
from services.services import url_validation
import asyncio


@pytest.fixture
def client():
    client = AsyncMock()
    return client



@pytest.fixture(params=[
    (200,"OK",0.123),
    (500,"Internal Server Error",0.10),
    (404,"Client_Error",0.10)
])

def server(request):
    status_code,reason_phrase,elapsed_time = request.param
    server = Mock()

    server.status_code = status_code
    server.reason_phrase = reason_phrase
    server.elapsed.total_seconds.return_value = elapsed_time
    return server



@pytest.mark.asyncio
async def test_ficture(client,server):
    
    client.get.return_value = server
    results = await url_validation("https://www.dummy.com",client)
    assert results["status_code"] == server.status_code
    assert results["Status"] ==  server.reason_phrase 
    assert results ["elapsed_time"]== server.elapsed.total_seconds()





#unit test to test the server for 200, 404 and 500
@pytest.mark.asyncio
@pytest.mark.parametrize(
    "status_code,status,elapsed_time",
    [
        (200,"OK",0.123),
        (500,"Internal Server Error",0.10),
        (404,"Client_Error",0.10),
    ],
    ids=['RETURNS OK FOR 200','INTERNAL SERVER ERROR FOR 500','CLIENT ERROR FOR 500']
)
async def test_server_health(status_code, status,elapsed_time):
    client = AsyncMock()
    server = Mock()

    server.status_code = status_code
    server.reason_phrase = status
    server.elapsed.total_seconds.return_value = elapsed_time

    client.get.return_value = server
    result = await url_validation("https://www.dummy.com",client)

    assert result["status_code"] == status_code
    assert result["Status"] ==status
    assert result["elapsed_time"]==elapsed_time

    




#test for testing semaphore limit
@pytest.mark.asyncio
async def test_semaphore_limit():
    url = "https://www.dummy.com"
    semaphore_limit = 25
    total_requests = 100

    semaphore = asyncio.Semaphore(semaphore_limit)
    running =0
    max_running =0

    async def fake_url_validation():
        nonlocal running , max_running

        running +=1 
        max_running = max(running, max_running)
        await asyncio.sleep(0.01)
        running -=1

    async def semaphore_wrapper():
        async with semaphore:
            return await fake_url_validation()
        
    tasks =[semaphore_wrapper() for _ in range(total_requests)]
    results = await asyncio.gather(*tasks)

    assert len(results) == total_requests
    assert max_running <= semaphore_limit

    


   







#test to check if endpoint is actually live and working
@pytest.mark.asyncio
async def test_live_endpoint():
    async with httpx.AsyncClient() as client:
        response = await client.get("http://127.0.0.1:8000/check")
        assert response.status_code ==200 
        data=response.json()
        assert "summary" in data
        assert "results" in data
