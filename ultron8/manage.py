# SOURCE: https://gitlab.com/euri10/euri10_fastapi_base/blob/master/backend/app/manage.py
# import asyncio
# import functools
# import logging.config

# import click
# from faker import Faker

# import uvicorn
# from applog.utils import read_logging_config, setup_logging
# from models import users
# from settings import database
# from utils.password import get_password_hash

# logconfig_dict = read_logging_config("applog/logging.yml")
# setup_logging(logconfig_dict)

# logger = logging.getLogger(__name__)


# def async_adapter(wrapped_func):
#     @functools.wraps(wrapped_func)
#     def run_sync(*args, **kwargs):
#         loop = asyncio.get_event_loop()
#         task = wrapped_func(*args, **kwargs)
#         return loop.run_until_complete(task)

#     return run_sync


# @click.group()
# def cli():
#     logger.info("Using manage.py cli")


# @cli.command()
# def setuplog():
#     logconfig_dict = read_logging_config("applog/logging.yml")
#     setup_logging(logconfig_dict)


# @cli.command()
# def rundev():
#     logger.info("Running rundev command")
#     uvicorn.run("main:app", host="0.0.0.0", reload=True)


# @cli.command()
# @click.option("--count", default=10)
# @async_adapter
# async def seedfake(count):
#     fake = Faker()
#     fake_user_list = [
#         {
#             "name": fake.user_name(),
#             "email": fake.email(),
#             "password": get_password_hash(fake.password()),
#         }
#         for _ in range(count)
#     ]
#     async with database:
#         query = users.insert()
#         await database.execute_many(query, fake_user_list)


# if __name__ == "__main__":
#     cli()
