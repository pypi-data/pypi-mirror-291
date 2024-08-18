import hashlib
from pathlib import Path


def mkdir_full(path):
    Path(path).mkdir(parents=True, exist_ok=True)


def file_get_length(file_path, chunk_size=5):
    chunk_size = chunk_size * 1024 * 1024
    total_length = 0
    with open(file_path, 'rb') as file:
        while chunk := file.read(chunk_size):
            total_length += len(chunk)

    return total_length


def file_get_sha256(file_path, chunk_size=5):
    chunk_size = chunk_size * 1024 * 1024
    sha256 = hashlib.sha256()

    with open(file_path, 'rb') as file:
        while chunk := file.read(chunk_size):
            sha256.update(chunk)

    return sha256.hexdigest()
