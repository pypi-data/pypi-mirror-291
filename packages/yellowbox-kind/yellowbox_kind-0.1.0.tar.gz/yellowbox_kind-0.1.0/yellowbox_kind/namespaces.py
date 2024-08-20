from contextlib import contextmanager
from typing import Generator, MutableSet, Union
from uuid import uuid4

from kubernetes.client import ApiClient, ApiException, CoreV1Api, V1Namespace, V1ObjectMeta


class NamespaceManager:
    def __init__(self, client: Union[ApiClient, CoreV1Api]):
        if isinstance(client, ApiClient):
            self.client = CoreV1Api(client)
        else:
            self.client = client

        self.created_namespaces: MutableSet[str] = set()

    def create_namespace(self, name: str, *, exists_ok: bool = False) -> bool:
        try:
            self.client.create_namespace(V1Namespace(metadata=V1ObjectMeta(name=name)))
        except ApiException as e:
            if e.status == 409:  # noqa: PLR2004
                if exists_ok:
                    return False
                raise ValueError(f"Namespace {name} already exists.") from e
            raise
        self.created_namespaces.add(name)
        return True

    def delete_namespace(self, name: str):
        # note that it may take a while for the namespace to be fully deleted
        # from my experience, it takes about 15 seconds
        if name not in self.created_namespaces:
            raise ValueError(f"Namespace {name} has not been created by this manager.")
        self.client.delete_namespace(name)
        self.created_namespaces.remove(name)

    def create_anonymous_namespace(self):
        # TODO handle collisions
        name = "yellowbox-" + uuid4().hex[:8]
        self.create_namespace(name)
        return name

    def delete_all_created(self):
        for ns in self.created_namespaces:
            self.delete_namespace(ns)
        self.created_namespaces.clear()

    @contextmanager
    def namespace(self, name: str, *, exists_ok: bool = False) -> Generator[str, None, None]:
        created = self.create_namespace(name, exists_ok=exists_ok)
        try:
            yield name
        finally:
            if created:
                self.delete_namespace(name)

    @contextmanager
    def anonymous_namespace(self) -> Generator[str, None, None]:
        name = self.create_anonymous_namespace()
        try:
            yield name
        finally:
            self.delete_namespace(name)
