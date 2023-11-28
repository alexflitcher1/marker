import json
import httpx
from httpx import AsyncClient

from config import *


client = AsyncClient()


async def is_auth_query(request):
    auth = request.headers.get('Authorization')

    if not auth:
        return (False, False, False)
    
    result = await client.get(AUTH_URL, headers={'Authorization': auth})
    r = json.loads(result.content)

    return (r, result.status_code, auth)