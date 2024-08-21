import pickle
from typing import Any

from langgraph.checkpoint.serde.base import SerializerProtocol


class JarvisCheckpointSerializer(SerializerProtocol):
    def dumps(self, obj: Any) -> bytes:
        return pickle.dumps(obj=obj)

    def dumps_typed(self, obj: Any) -> tuple[str, bytes]:
        return "bytes", pickle.dumps(obj=obj)

    def loads(self, data: bytes) -> Any:
        return pickle.loads(data)

    def loads_typed(self, data: tuple[str, bytes]) -> Any:
        type_, data_ = data
        return pickle.loads(data_)
