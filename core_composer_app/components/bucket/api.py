"""Bucket api
"""
from core_composer_app.components.bucket.models import Bucket
import random


def get_by_id(bucket_id):
    """Returns a bucket given its id

    Args:
        bucket_id:

    Returns:

    """
    return Bucket.get_by_id(bucket_id)


def upsert(bucket):
    """Saves or Updates a bucket

    Args:
        bucket:

    Returns:

    """
    # get list of colors already present
    existing_colors = Bucket.get_colors()
    # set a color if not set
    if bucket.color is None:
        # get a unique color
        color = _get_random_hex_color()
        while color in existing_colors:
            color = _get_random_hex_color()

        bucket.color = color

    return bucket.save()


def get_all():
    """Returns all buckets

    Returns:

    """
    return Bucket.get_all()


def delete(bucket):
    """Deletes a bucket

    Args:
        bucket:

    Returns:

    """
    bucket.delete()


def _get_random_hex_color():
    """Returns a random hexa color string

    Returns:

    """
    return '#' + ''.join([random.choice('0123456789ABCDEF') for x in range(6)])
