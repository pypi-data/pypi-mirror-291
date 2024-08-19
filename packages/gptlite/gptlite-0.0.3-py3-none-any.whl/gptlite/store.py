import os
from uuid import uuid4

from pydantic import BaseModel


class _FILE_INFO(BaseModel):
    id: str
    size: int
    filename: str
    purpose: str
    created_at: float


class Files:
    _STORE_PATH = None

    @staticmethod
    def set_store_path(path: str):
        Files._STORE_PATH = path
        if not os.path.exists(Files._STORE_PATH):
            os.makedirs(Files._STORE_PATH)

    @staticmethod
    def list():
        files = []
        for file in os.listdir(Files._STORE_PATH):
            id = file.split("_")[0]
            purpose = file.split("_")[1]
            filename = "_".join(file.split("_")[2:])
            path = os.path.join(Files._STORE_PATH, file)
            size = os.path.getsize(path)
            created_at = os.path.getctime(path)
            file = _FILE_INFO(
                id=id,
                size=size,
                filename=filename,
                purpose=purpose,
                created_at=created_at,
            )
            files.append(file)
        return files

    @staticmethod
    def create(filename, content: bytes, purpose: str):
        assert Files._STORE_PATH

        id = "file-" + str(uuid4()).replace("-", "")
        purpose = purpose.replace("_", "-")
        path = os.path.join(Files._STORE_PATH, f"{id}_{purpose}_{filename}")
        with open(path, "wb") as f:
            f.write(content)
        size = os.path.getsize(path)
        created_at = os.path.getctime(path)
        return _FILE_INFO(
            id=id,
            size=size,
            filename=filename,
            purpose=purpose,
            created_at=created_at,
        )

    @staticmethod
    def read(id: str) -> bytes | None:
        assert Files._STORE_PATH

        file = Files._find_file(id)
        if file:
            path = os.path.join(Files._STORE_PATH, file)
            with open(path, "rb") as f:
                content = f.read()
                return content
        else:
            return None

    @staticmethod
    def delete(id: str):
        assert Files._STORE_PATH

        deleted = False
        filename = Files._find_file(id)
        path = os.path.join(Files._STORE_PATH, filename)
        if path:
            os.remove(path)
            deleted = True

        return {"id": id, "deleted": deleted}

    @staticmethod
    def info(id: str):
        assert Files._STORE_PATH

        file = Files._find_file(id)
        if file:
            id = file.split("_")[0]
            purpose = file.split("_")[1]
            filename = "_".join(file.split("_")[2:])
            path = os.path.join(Files._STORE_PATH, file)
            size = os.path.getsize(path)
            created_at = os.path.getctime(path)
            return _FILE_INFO(
                id=id,
                size=size,
                filename=filename,
                purpose=purpose,
                created_at=created_at,
            )
        else:
            return None

    @staticmethod
    def _find_file(id: str):
        assert Files._STORE_PATH

        files = os.listdir(Files._STORE_PATH)
        for file in files:
            if file.startswith(id):
                return file
        return None
