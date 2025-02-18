import httpx
import json

from .entity.song.SongResult import SongResult
from .entity.album.AlbumResult import AlbumResult
from .entity.EntityResult import EntityResult

BASE_URL = 'https://api.song.link'
API_VERSION = 'v1-alpha.1'
ROOT = f'{BASE_URL}/{API_VERSION}'
LINKS_ENDPOINT = 'links'

class Odesli():
    def __init__(self, key=None):
        self.key = key

    async def __get(self, params) -> EntityResult:
        if not self.key == None:
            params['key'] = self.key
        async with httpx.AsyncClient() as client:
            requestResult = await client.get(f'{ROOT}/{LINKS_ENDPOINT}', params=params, timeout=30)
        await requestResult.raise_for_status()
        result = json.loads(requestResult.content.decode())
        resultType = next(iter(result['entitiesByUniqueId'].values()))['type']
        if resultType == 'song':
            return await SongResult.parse(result)
        elif resultType == 'album':
            return await AlbumResult.parse(result)
        else:
            raise NotImplementedError(f'Entities with type {resultType} are not supported yet.')


    async def getByUrl(self, url) -> EntityResult:
        return await self.__get({ 'url': url })

    async def getById(self, id, platform, type) -> EntityResult:
        return await self.__get({
            'id': id,
            'platform': platform,
            'type': type
        })
