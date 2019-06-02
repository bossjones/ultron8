# uvicorn (ASGI ) Server | How to run it in a python script

```python
from starlette.applications import Starlette
from starlette.responses import JSONResponse
import uvicorn

app = Starlette(debug=True)


@app.route('/')
async def homepage(request):
    return JSONResponse({'hello': 'world'})

if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8000)

```


Will need to convert `web.py` or something like that later to run like this, maybe.
