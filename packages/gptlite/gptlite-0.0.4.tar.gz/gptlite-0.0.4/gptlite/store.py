import os
from typing import Any, Literal, Optional
from uuid import uuid4

from dotenv import load_dotenv
from pydantic import BaseModel

load_dotenv()


class FileInfo(BaseModel):
    id: str
    size: int
    filename: str
    purpose: str
    created_at: float


class Files:
    _STORE_PATH: Any = os.environ.get("GPTLITE_FILE_STORE_PATH", None)

    @staticmethod
    def set(key: Literal["store_path"], value: str):
        if key == "store_path":
            Files._STORE_PATH = value
            if not os.path.exists(Files._STORE_PATH):
                os.makedirs(Files._STORE_PATH)
        else:
            raise ValueError(f"Invalid gptlite Files key: {key}")

    @staticmethod
    def list():
        Files._assert_env()

        files = []
        for file in os.listdir(Files._STORE_PATH):
            id = file.split("_")[0]
            purpose = file.split("_")[1]
            filename = "_".join(file.split("_")[2:])
            path = os.path.join(Files._STORE_PATH, file)
            size = os.path.getsize(path)
            created_at = os.path.getctime(path)
            file = FileInfo(
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
        Files._assert_env()

        id = "file-" + str(uuid4()).replace("-", "")
        purpose = purpose.replace("_", "-")
        path = os.path.join(Files._STORE_PATH, f"{id}_{purpose}_{filename}")
        with open(path, "wb") as f:
            f.write(content)
        size = os.path.getsize(path)
        created_at = os.path.getctime(path)
        return FileInfo(
            id=id,
            size=size,
            filename=filename,
            purpose=purpose,
            created_at=created_at,
        )

    @staticmethod
    def read(id: str) -> Optional[bytes]:
        Files._assert_env()

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
        Files._assert_env()

        deleted = False
        filename = Files._find_file(id)
        path = os.path.join(Files._STORE_PATH, filename)
        if path:
            os.remove(path)
            deleted = True

        return {"id": id, "deleted": deleted}

    @staticmethod
    def info(id: str):
        Files._assert_env()

        file = Files._find_file(id)
        if file:
            id = file.split("_")[0]
            purpose = file.split("_")[1]
            filename = "_".join(file.split("_")[2:])
            path = os.path.join(Files._STORE_PATH, file)
            size = os.path.getsize(path)
            created_at = os.path.getctime(path)
            return FileInfo(
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
        Files._assert_env()

        files = os.listdir(Files._STORE_PATH)
        for file in files:
            if file.startswith(id):
                return file
        return None

    @staticmethod
    def _assert_env():
        assert (
            Files._STORE_PATH
        ), "Please set `store_path` by `GPTLITE_FILE_STORE_PATH` in .env"
