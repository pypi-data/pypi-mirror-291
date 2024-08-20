"""
Enum helper base.
"""

import typing as t
import warnings
from pathlib import Path

import typing_extensions as te

from composio.constants import LOCAL_CACHE_DIRECTORY
from composio.exceptions import ComposioSDKError
from composio.storage.base import LocalStorage
from composio.utils.logging import get_logger


_model_cache: t.Dict[str, LocalStorage] = {}
_runtime_actions: t.Dict[str, "ActionData"] = {}

EntityType = t.TypeVar("EntityType", bound=LocalStorage)
ClassType = t.TypeVar("ClassType", bound=t.Type["_AnnotatedEnum"])

TAGS_CACHE = LOCAL_CACHE_DIRECTORY / "tags"
APPS_CACHE = LOCAL_CACHE_DIRECTORY / "apps"
ACTIONS_CACHE = LOCAL_CACHE_DIRECTORY / "actions"
TRIGGERS_CACHE = LOCAL_CACHE_DIRECTORY / "triggers"


class MetadataFileNotFound(ComposioSDKError):
    """Raise when matadata file is missing."""


class SentinalObject:
    """Sentinal object."""

    sentinal = None


class TagData(LocalStorage):
    """Local storage for `Tag` object."""

    app: str
    "App name for this tag."

    value: str
    "Tag string."


class AppData(LocalStorage):
    """Local storage for `App` object."""

    name: str
    "Name of the app."

    is_local: bool = False
    "The tool is local if set to `True`"


class ActionData(LocalStorage):
    """Local storage for `Action` object."""

    name: str
    "Action name."

    app: str
    "App name where the actions belongs to."

    tags: t.List[str]
    "Tag string for the action."

    no_auth: bool = False
    "If set `True` the action does not require authentication."

    is_local: bool = False
    "If set `True` the `app` is a local app."

    is_runtime: bool = False
    "Set `True` for actions registered at runtime."

    shell: bool = False
    "If set `True` the action will be executed using a shell."


class TriggerData(LocalStorage):
    """Local storage for `Trigger` object."""

    name: str
    "Name of the trigger."

    app: str
    "Name of the app where this trigger belongs to."
    _cache: Path = TRIGGERS_CACHE


class _AnnotatedEnum(t.Generic[EntityType]):
    """Enum class that uses class annotations as values."""

    _slug: str
    _path: Path
    _model: t.Type[EntityType]
    _deprecated: t.Dict = {}

    def __new__(cls, value: t.Any, warn: bool = True):
        (base,) = t.cast(t.Tuple[t.Any], getattr(cls, "__orig_bases__"))
        (model,) = t.get_args(base)
        instance = super().__new__(cls)
        instance._model = model
        return instance

    def __init_subclass__(cls, path: Path) -> None:
        cls._path = path
        return super().__init_subclass__()

    def __init__(
        self,
        value: t.Union[str, te.Self, t.Type[SentinalObject]],
        warn: bool = True,
    ) -> None:
        """Create an Enum"""
        if hasattr(value, "sentinal"):
            value = value().get_tool_merged_action_name()  # type: ignore

        if isinstance(value, _AnnotatedEnum):
            value = value._slug

        self._slug = t.cast(str, value).upper()
        if self._slug in self._deprecated and warn:
            warnings.warn(
                f"`{self._slug}` is deprecated and will be removed. "
                f"Use `{self._deprecated[self._slug]}` instead.",
                UserWarning,
            )
            self._slug = self._deprecated[self._slug]
            return

        if (
            self._slug not in self.__annotations__
            and self._slug not in _runtime_actions
        ):
            raise ValueError(f"Invalid value `{value}` for `{self.__class__.__name__}`")

    @property
    def slug(self) -> str:
        """Enum slug value."""
        return self._slug

    def load(self) -> EntityType:
        """Load action data."""
        if self._slug is None:
            raise ValueError(
                "Cannot load `AppData` object without initializing object."
            )
        if self._slug in _runtime_actions:
            return _runtime_actions[self._slug]  # type: ignore
        if not (self._path / self._slug).exists():
            from composio.cli.apps import (  # pylint: disable=import-outside-toplevel
                update,
            )
            from composio.cli.context import (  # pylint: disable=import-outside-toplevel
                get_context,
            )

            logger = get_logger()
            logger.debug(
                f"Metadata file for `{self._slug}` not found, updating metadata"
            )
            update(context=get_context())
        if self._slug not in _model_cache:
            _model_cache[self._slug] = self._model.load(self._path / self._slug)
        return t.cast(EntityType, _model_cache[self._slug])

    @classmethod
    def all(cls) -> t.Iterator[te.Self]:
        """Iterate over available object."""
        for name in cls.__annotations__:
            if name == "_deprecated":
                continue
            yield cls._create(name=name)

    @classmethod
    def _create(cls, name: str) -> te.Self:
        """Create a `_AnnotatedEnum` class."""
        return cls(name)

    def __str__(self) -> str:
        """String representation."""
        return t.cast(str, self._slug)

    def __eq__(self, other: object) -> bool:
        """Check equivilance of two objects."""
        if not isinstance(other, (str, _AnnotatedEnum)):
            return NotImplemented
        return str(self) == str(other)

    def __hash__(self) -> int:
        return hash(self._slug)


def enum(cls: ClassType) -> ClassType:
    """Decorate class."""
    for attr in cls.__annotations__:
        if attr == "_deprecated":
            continue
        setattr(cls, attr, cls(attr, warn=False))
    return cls


def add_runtime_action(name: str, data: ActionData) -> None:
    """Add action at runtime."""
    _runtime_actions[name] = data


def get_runtime_actions() -> t.List:
    """Add action at runtime."""
    return list(_runtime_actions)
