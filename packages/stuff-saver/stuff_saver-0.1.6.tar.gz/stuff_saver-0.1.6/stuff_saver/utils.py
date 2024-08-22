import errno
import hashlib
import os
import re
import typing
import unicodedata


def mkdir_p(path: str) -> None:
    """
    Create a directory and its parent directories if they do not exist.
    Args:
        path (str): The path of the directory to be created.
    Raises:
        OSError: If an error occurs while creating the directory.
    """

    try:
        os.makedirs(path)
    except OSError as exc:  # Python >2.5
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else:
            raise


def slugify(value: str, lower: bool = True) -> str:
    """
    Convert a string into a slug by removing special characters and replacing spaces with hyphens.

    Args:
        value (str): The string to be slugified.
        lower (bool, optional): Whether to convert the slug to lowercase. Defaults to True.

    Returns:
        str: The slugified string.
    """

    value_bytes: bytes = unicodedata.normalize("NFKD", value).encode("utf-8", "ignore")
    value = re.sub(r"[^\w\s-]", "", value_bytes.decode("utf-8")).strip()
    if lower:
        value = value.lower()
    value = str(re.sub(r"[-\s]+", "-", value))
    return value


def hasher(word: typing.Hashable) -> str:
    """
    Hashes a given word and returns the hashed value.

    Parameters:
    - word (typing.Hashable): The word to be hashed.

    Returns:
    - str: The hashed value of the word.
    """

    slug_word = slugify(str(word))
    hash_object = hashlib.sha512(slug_word.encode())
    slug_word = hash_object.hexdigest()
    return slug_word
