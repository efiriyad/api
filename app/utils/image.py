from io import BytesIO
from typing import BinaryIO

from PIL import Image


def resize_image(image: BinaryIO, size: tuple, ext: str = "PNG") -> bytes:
    """Resize image to given size without changing the aspect ratio."""
    image = Image.open(image)
    image.thumbnail(size, Image.ANTIALIAS)

    byte_arr = BytesIO()
    image.save(byte_arr, format=ext)

    return byte_arr.getvalue()
