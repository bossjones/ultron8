import random
import string

from typing import Tuple

import factory

from ultron8.api.models.user import UserCreate


def randomStringwithDigitsAndSymbols(stringLength: int = 10) -> str:
    """Generate a random password string with Special characters, letters, and digits.

    Keyword Arguments:
        stringLength {int} -- [description] (default: {10})

    Returns:
        [type] -- [description]
    """
    password_characters = string.ascii_letters + string.digits + string.punctuation
    return "".join(random.choice(password_characters) for i in range(stringLength))


def random_full_name(male_or_female: str = "male") -> Tuple[str, str]:
    if male_or_female == "male":
        first_name = factory.Faker("first_name_male")
        last_name = factory.Faker("last_name_male")
    else:
        first_name = factory.Faker("first_name_female")
        last_name = factory.Faker("last_name_female")

    return first_name.generate(), last_name.generate()


class RandomUserFactory(factory.Factory):
    class Meta:
        model = UserCreate

    full_name = factory.Faker("name_male")
    # is_active = True
    # is_superuser = False
    email = factory.Faker("free_email")
    password = factory.Faker("password")


def _MakeRandomNormalUserFactory() -> UserCreate:
    _rand_num = random.randrange(1000)
    _first_name, _last_name = random_full_name()
    _email = "{}.{}{}@example.org".format(_first_name, _last_name, _rand_num)
    _full_name = "{} {}".format(_first_name, _last_name)
    _password = randomStringwithDigitsAndSymbols()

    return RandomUserFactory(full_name=_full_name, email=_email, password=_password)
