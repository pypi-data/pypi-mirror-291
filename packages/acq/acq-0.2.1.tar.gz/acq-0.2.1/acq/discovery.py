import collections
import importlib
import inspect
import types
import typing

MODULE_NAME_SEPARATOR = '.'

T = typing.TypeVar("T", bound=typing.Type[object])


def import_module_safe(module_name: str) -> typing.Optional[types.ModuleType]:
    """ Wrapper for importlib.import_module that ignores ImportError

    """

    try:
        return importlib.import_module(module_name)
    except ImportError:
        return None


def get_module_name(*parts: str) -> str:
    return MODULE_NAME_SEPARATOR.join(parts)


def get_modules(
    *module_names: str,
    package_names: typing.Sequence[str] = [],
) -> typing.List[types.ModuleType]:
    if not package_names:
        return list(filter(None, map(import_module_safe, module_names)))

    if not module_names:
        return get_modules(*package_names)

    all_module_names = []

    for package_name in package_names:
        for module_name in module_names:
            all_module_names.append(get_module_name(package_name, module_name))

    return get_modules(*all_module_names)


def get_module_objects(
    modules: typing.List[types.ModuleType],
    types: typing.Tuple[T],
) -> typing.Mapping[T, typing.Sequence[T]]:
    results = collections.defaultdict(list)

    for module in modules:
        for attribute_name in dir(module):
            for object_type in types:
                module_object = getattr(module, attribute_name)
                is_class = inspect.isclass(module_object)

                if attribute_name == 'FancySubClass':
                    print(
                        module_object,
                        issubclass(module_object, object_type),
                    )

                if module_object is object_type:
                    results[object_type].append(module_object)
                elif is_class and issubclass(module_object, object_type):
                    results[object_type].append(module_object)
                elif isinstance(module_object, object_type):
                    results[object_type].append(module_object)

    return results


@typing.overload
def discover(
    *module_names: str,
    package_names: typing.Sequence[str] = [],
    types: typing.Literal[None] = None,
) -> typing.List[types.ModuleType]:
    """ called with no types provided """


@typing.overload
def discover(
    *module_names: str,
    package_names: typing.Sequence[str] = [],
    types: typing.Tuple[T],
) -> typing.Mapping[T, typing.Sequence[T]]:
    """ called with types provided """


def discover(
    *module_names: str,
    package_names: typing.Sequence[str] = [],
    types: None | typing.Tuple[T] = None,
) -> typing.List[types.ModuleType] | typing.Mapping[T, typing.Sequence[T]]:
    """ Allows discovery of modules, packages, or objects within them """

    modules = get_modules(*module_names, package_names=package_names)

    if types is None:
        return modules

    return get_module_objects(modules, types)
