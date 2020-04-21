## Run
First, you'll want to clone the repo.  The codebase is using pipenv, so go install w/ pipenv.  In pipenv, we're using a custom command `serve`.

Once the server is running, you should be able to load [http://127.0.0.1:8000](http://127.0.0.1:8000).  This will display the swagger docs for the endpoint.

```bash
# Clone the repo & go into it.
git clone https://github.com/bossjones/ultron8.git
cd ultron8

# We're using pipenv, so install using that.
pipenv install

# Copy the .env.dist to .env, the dev server will grab envs from here
# You'll want to update the .env to point to your redis instance & db
cp .env.dist .env

# Run migration if you haven't already.
pipenv run migrate

# Run things and navigate to http://127.0.0.1:8000 for the API specs.
pipenv run serve
```

## Test
The tests are integration tests.  They use sqlite for the db & a memory cache (instead of redis) for the cache.
```
pipenv install -d
pipenv run test
```

# Testing w/ pytest and Visual Studio Code

### Note

Unit test debugging with `pytest` only works when code-coverage is disabled:
```
{
    "python.testing.pytestEnabled": true,
    "python.testing.pytestArgs": [ "--no-cov" ]
}
{
    "python.testing.pytestEnabled": true,
    "python.testing.pytestArgs": [ "--cov-config=.coveragerc", "--cov=./westac", ]
}
```
See [issue](https://github.com/microsoft/vscode-python/issues/693) and [issue](https://github.com/kondratyev-nv/vscode-python-test-adapter/issues/123).
