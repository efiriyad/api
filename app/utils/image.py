from io import BytesIO
from typing import BinaryIO

from PIL import Image


def resize_image(image: BinaryIO, size: tuple, format: str = "PNG") -> bytes:
    """Resize image to given size without changing the aspect ratio."""
    image = Image.open(image)
    image.thumbnail(size, Image.ANTIALIAS)

    byte_arr = BytesIO()
    image.save(byte_arr, format=format)

    return byte_arr.getvalue()
