from __future__ import annotations

import asyncio.subprocess as asyncio_subprocess
import os
import subprocess
from contextlib import AbstractContextManager, asynccontextmanager, contextmanager
from os import PathLike
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import TYPE_CHECKING, AsyncGenerator, Generator, Union
from uuid import uuid4

from kubernetes.client import ApiClient
from kubernetes.config import new_client_from_config
from yellowbox.service import YellowService

if TYPE_CHECKING:
    try:
        from pytest import TempPathFactory
    except ImportError:
        pass

from yellowbox_kind.namespaces import NamespaceManager

DEFAULT_KIND_PATH = "kind"


class KindClusterService(YellowService):
    def __init__(
        self,
        config_path: PathLike[str] | str | TemporaryDirectory | TempPathFactory,
        *,
        cluster_name: str | None = None,
        kind_path: str | None = None,
    ):
        self.kind_path = kind_path or DEFAULT_KIND_PATH

        if isinstance(config_path, TemporaryDirectory):
            config_path = config_path.name
        elif hasattr(config_path, "mktemp"):  # this is a pytest TempPathFactory
            config_path = config_path.mktemp("yellowbox-kind")

        self.base_config_path = config_path

        self.config_path: Union[Path, None] = None  # this will be none until the service is started
        self.cluster_name = cluster_name

        self._client: Union[ApiClient, None] = None  # this is an internal k8s client, used for various operations
        self._namespace_manager: Union[NamespaceManager, None] = None

    def is_alive(self) -> bool:
        return self.cluster_name is not None

    def _infer_cluster_config(self) -> None:
        if not self.cluster_name:
            existing_clusters = frozenset(
                subprocess.check_output([self.kind_path, "get", "clusters"], text=True).strip().splitlines()
            )
            # note that if there are no existing clusters, we will return a list with only one item: the response
            # from the command this means that an auto-generated cluster name will never be exactly equal to the
            # empty reponse, which I can live with
            while True:
                self.cluster_name = "yellowbox-" + uuid4().hex[:8]
                if self.cluster_name not in existing_clusters:
                    break

        if os.path.exists(self.base_config_path):
            if not os.path.isdir(self.base_config_path):
                raise ValueError(
                    f"File {self.base_config_path} already exists, specify "
                    "a directory to create an anonymous kubeconfig file"
                )
            base_config_path = Path(self.base_config_path)
            if (
                self.cluster_name
                and not (cand_path := (base_config_path / ("kubeconfig-" + self.cluster_name + ".yaml"))).exists()
            ):
                self.config_path = cand_path
                return
            # generate a unique filename in the directory
            while True:
                self.config_path = base_config_path / ("kubeconfig-" + uuid4().hex[:8] + ".yaml")
                if not self.config_path.exists():
                    return
        self.config_path = Path(self.base_config_path)

    @contextmanager
    def kube_client(self) -> Generator[ApiClient, None, None]:
        # currently, this provides the internal k8s client, but it could be changed to provide client especially
        #  configured for the user
        yield self._get_client()

    @classmethod
    @contextmanager
    def run(cls, *args, **kwargs) -> Generator[KindClusterService, None, None]:
        inst = cls(*args, **kwargs)
        inst.start()
        with inst:
            yield inst

    @classmethod
    @asynccontextmanager
    async def arun(cls, *args, **kwargs) -> AsyncGenerator[KindClusterService, None]:
        inst = cls(*args, **kwargs)
        await inst.astart()
        try:
            yield inst
        finally:
            await inst.astop()

    def start(self) -> KindClusterService:
        self._infer_cluster_config()
        assert self.config_path is not None
        assert self.cluster_name is not None

        subprocess.check_call(
            [self.kind_path, "create", "cluster", "--name", self.cluster_name, "--kubeconfig", self.config_path]
        )

        return self

    async def astart(self):
        self._infer_cluster_config()  # note that this operation included a syncronous subprocess call,
        # but it's short enough and likely to not be noticable
        assert self.config_path is not None
        assert self.cluster_name is not None

        proc = await asyncio_subprocess.create_subprocess_exec(
            self.kind_path, "create", "cluster", "--name", self.cluster_name, "--kubeconfig", self.config_path
        )
        await proc.wait()

        return self

    def _cleanup(self):
        if self._namespace_manager is not None:
            if self._namespace_manager.created_namespaces:
                # this should only be possible through some improper use of the service,
                # since the namespace manager is private, and only exposes the context manager
                # methods
                raise RuntimeError(
                    "There are still temporary namespaces created by the service, to explicitly create "
                    "a namespace that outlives the cluster, use the kubernetes client directly"
                )
            self._namespace_manager.delete_all_created()
        if self._client is not None:
            self._client.close()

    def stop(self):
        self._cleanup()
        if self.cluster_name:
            subprocess.check_call([self.kind_path, "delete", "cluster", "--name", self.cluster_name])
        self.cluster_name = None

    async def astop(self):
        self._cleanup()
        if self.cluster_name:
            proc = await asyncio_subprocess.create_subprocess_exec(
                self.kind_path, "delete", "cluster", "--name", self.cluster_name
            )
            await proc.wait()
        self.cluster_name = None

    def _get_client(self) -> ApiClient:
        if self.config_path is None:
            raise ValueError("The cluster has not been started yet.")
        if self._client is None:
            self._client = new_client_from_config(config_file=str(self.config_path))
        return self._client

    def _get_namespace_manager(self) -> NamespaceManager:
        if self._namespace_manager is None:
            self._namespace_manager = NamespaceManager(self._get_client())
        return self._namespace_manager

    def namespace(self, name: str, *, exists_ok: bool = False) -> AbstractContextManager[str]:
        return self._get_namespace_manager().namespace(name, exists_ok=exists_ok)

    def anonymous_namespace(self) -> AbstractContextManager[str]:
        return self._get_namespace_manager().anonymous_namespace()
