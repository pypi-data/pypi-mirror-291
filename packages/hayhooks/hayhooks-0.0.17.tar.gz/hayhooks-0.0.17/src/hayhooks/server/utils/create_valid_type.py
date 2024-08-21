from inspect import isclass
from types import GenericAlias
from typing import Dict, Optional, Union, get_args, get_origin, get_type_hints


def handle_unsupported_types(type_: type, types_mapping: Dict[type, type]) -> Union[GenericAlias, type]:
    """
    Recursively handle types that are not supported by Pydantic by replacing them with the given types mapping.

    :param type_: Type to replace if not supported
    :param types_mapping: Mapping of types to replace
    """

    def _handle_generics(t_) -> GenericAlias:
        """
        Handle generics recursively
        """
        child_typing = []
        for t in get_args(t_):
            if t in types_mapping:
                result = types_mapping[t]
            elif isclass(t):
                result = handle_unsupported_types(t, types_mapping)
            else:
                result = t
            child_typing.append(result)

        if len(child_typing) == 2 and child_typing[1] is type(None):
            # because TypedDict can't handle union types with None
            # rewrite them as Optional[type]
            return Optional[child_typing[0]]
        else:
            return GenericAlias(get_origin(t_), tuple(child_typing))

    if isclass(type_):
        new_type = {}
        for arg_name, arg_type in get_type_hints(type_).items():
            if get_args(arg_type):
                new_type[arg_name] = _handle_generics(arg_type)
            else:
                new_type[arg_name] = arg_type

        return type_

    return _handle_generics(type_)
