# Catching-Proxy-CLI-Tool

https://roadmap.sh/projects/caching-server

## command to run it:
>python manage.py runserver
- dummyjson is the default origin page and 8000 is the default port
- You can modify them with the following command:
  >ORIGIN_URL=(the url of the page) python manage.py runserver (port)

- to clear the cache: (on the url bar) http://127.0.0.1:3000/clear_cache/
- or you can write the following command in the terminal (although you cant use it while the terminal is running the server):
- >python manage.py clear_cache
