import os
import re
import requests
import hashlib
import argparse
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.cache import cache


origin = os.getenv('ORIGIN_URL', 'https://dummyjson.com')

def get_cache_key(path):
    return hashlib.sha256(path.encode()).hexdigest()


# def proxy_view(request, path=''):
#     cache_key = f'proxy:{path or "root"}'
#     response_data = cache.get(cache_key)

#     if response_data is None:
#         print('Cache miss:', cache_key)
#         origin_url = f'{origin}/{path}'
#         response = requests.get(origin_url)
#         cache.set(cache_key, response_data, timeout=60 * 5)

#         try:
#             response_data = response.json()
#             cache.set(cache_key, response_data, timeout=60 * 5)
#             return JsonResponse(response_data)

#         except ValueError:
#             print('Invalid JSON from origin:', response.text[:100])
#             return HttpResponse(response.text, status=response.status_code, content_type=response.headers.get('Content-Type', 'text/plain'))

#     print('Cache hit:', cache_key)
#     return JsonResponse(response_data)


def safe_cache_key(key):
    return re.sub(r'[^a-zA-Z0-9_-]', '_', key)

def proxy_view(request, path):
    cache_key = safe_cache_key(f'proxy:{path}')


    cached_response = cache.get(cache_key)
    if cached_response:
        print(f'[CACHE] HIT for {path}')
        return HttpResponse(cached_response['content'], content_type=cached_response['content_type'], status=200, headers={'X-Cache': 'HIT'})
    else:
        print(f'[CACHE] MISS for {path}')

    try:
        origin_response = requests.get(origin, timeout=5)
    except requests.exceptions.RequestException as e:
        print(f'[ERROR] Failed to fetch {origin}: {e}')
        return HttpResponse(
            f'Error fetching origin: {str(e)}',
            status=502,
            content_type='text/plain'
        )

    origin_response = requests.get(origin)
    content_type = origin_response.headers.get('Content-Type', '')

    cache.set(cache_key, {
        'content': origin_response.content,
        'content_type': content_type
    })

    headers = {'X-Cache': 'MISS'}
    if 'application/json' in content_type:
        try:
            data = origin_response.json()
            return JsonResponse(data, status=origin_response.status_code, headers=headers)
        except ValueError:
            return HttpResponse('Invalid JSON ', status=502, headers=headers)
    return HttpResponse(
        origin_response.content,
        content_type=content_type,
        status=origin_response.status_code,
        headers=headers
    )

def clear_cache(request):
    cache.clear()
    return HttpResponse('Cache cleared', status=200)
