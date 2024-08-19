from inspect import signature
from typing import Any, Callable, get_type_hints


class InterfaceError(Exception):
    pass


def implements(*interfaces):
    def decorator(cls):
        checked_interfaces = set()
        missing_methods = set()

        def check_interface(interface):
            if interface in checked_interfaces:
                return
            checked_interfaces.add(interface)

            interface_attrs = {attr[0]: attr[1] for attr in interface.__dict__.items() if not attr[0].startswith("__")}
            for attr_name, attr_value in interface_attrs.items():
                if attr_name.startswith("__"):
                    continue

                if callable(attr_value) and not attr_name.startswith("__"):
                    if not hasattr(cls, attr_name):
                        if "optional" in attr_name:
                            continue

                        if "default" in attr_name and f"{attr_name}" in interface_attrs.keys():
                            setattr(cls, attr_name, getattr(interface, f"{attr_name}"))
                        else:
                            missing_methods.add(f"{interface.__name__}.{attr_name}")
                    elif not callable(getattr(cls, attr_name)):
                        raise InterfaceError(f"{attr_name} in {cls.__name__} must be callable")
                    else:
                        check_method_signature(cls, interface, attr_name)

            for parent in interface.__bases__:
                if issubclass(parent, Interface):
                    check_interface(parent)

        for interface in interfaces:
            check_interface(interface)

        if missing_methods:
            raise InterfaceError(f"{cls.__name__} does not implement {', '.join(missing_methods)}")

        return cls

    return decorator


def check_method_signature(cls, interface, method_name):
    cls_method = getattr(cls, method_name)
    interface_method = getattr(interface, method_name)

    cls_sig = signature(cls_method)
    interface_sig = signature(interface_method)

    if cls_sig.parameters != interface_sig.parameters:
        raise InterfaceError(f"Method {method_name} in {cls.__name__} has incorrect signature")

    cls_return = get_type_hints(cls_method).get("return")
    interface_return = get_type_hints(interface_method).get("return")

    if cls_return != interface_return:
        raise InterfaceError(f"Method {method_name} in {cls.__name__} has incorrect return type")


class Interface:
    @classmethod
    def check_implements(cls, obj: Any) -> bool:
        return all(
            hasattr(obj, attr) and callable(getattr(obj, attr))
            for attr, value in cls.__dict__.items()
            if callable(value) and not attr.startswith("__")
        )


def method(func: Callable) -> Callable:
    return func


def default_method(func: Callable) -> Callable:
    return func


def optional_method(func: Callable) -> Callable:
    return func
