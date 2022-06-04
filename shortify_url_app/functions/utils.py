from django.conf import settings
from random import choice


def make_suffix():
    alpha = "qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM"
    return "".join([choice(alpha) for _ in range(5)])


def get_url(suffix):
    return f"{settings.HOST}/short/redirect/{suffix}"


if __name__ == "__main__":
    print(make_suffix())


