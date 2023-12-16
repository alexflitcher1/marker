import json
from httpx import AsyncClient

from config import AUTH_URL


client = AsyncClient()


async def is_auth_query(request):
    auth = request.headers.get('Authorization')

    if not auth:
        return (False, False, False)

    result = await client.get(AUTH_URL, headers={'Authorization': auth})
    r = json.loads(result.content)

    return (r, result.status_code, auth)
