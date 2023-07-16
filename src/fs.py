from contextlib import contextmanager
import os, shutil
import tarfile


@contextmanager
def ArchiveDir(archive_name: str, path: str = ".audascii_files"):
    if os.path.exists(path):
        shutil.rmtree(path)
    os.mkdir(path)
    yield path
    with tarfile.open(f"{archive_name}.audascii", "w:gz") as f:
        for file in os.listdir(path):
            if not file.startswith("."):
                f.add(f"{path}/{file}", file)
    shutil.rmtree(path)
    size = os.path.getsize(f"{archive_name}.audascii")
    print(f"Archive size: {size / 2 ** 20:.3f}MB")
