from typing import Annotated, Any, Generic, TypeVar, Union

from pydantic import BaseModel, BeforeValidator, TypeAdapter, model_validator

__all__ = ("R", "Route", "Routed", "Router")

RoutePart = Union[int, str]
rp_ta = TypeAdapter(RoutePart)


def split_route(route: str) -> list[RoutePart]:
    """Split a `.`-separated string/integer subpath up into a list."""
    match route:
        case str():
            return list(map(rp_ta.validate_strings, route.split(".")))
        case list():
            return route
        case _:
            raise ValueError(f"Invalid route: {route}")


Route = Annotated[list[RoutePart], BeforeValidator(split_route)]
"""The `.`-separated string keys and integers that specify a JSON-like subpath."""


class Router(BaseModel, validate_default=True):
    """A model which should be subclassed to specify `Route` type fields).

    For example:

    ```py
    from fieldrouter import Router, Route

    class Where(Router):
        value_1: Route = "example.subpath.0"
    ```
    """


R = TypeVar("R", bound=Router)


def extract_subpath(path: Route, data: dict) -> Any:
    """Extract a subpath or else an error reporter fallback indicating where it failed."""
    for part_idx, part in enumerate(path):
        reporter = ValueError(f"Missing {part=} on {path}")
        match part:
            case str() as key:
                data = data.get(key, reporter)
            case int() as idx:
                data = (
                    data[idx]
                    if isinstance(data, list) and -len(data) <= idx < len(data)
                    else reporter
                )
        if data is reporter:
            break
    return data


class Routed(BaseModel, Generic[R]):
    """A model which should be subclassed to specify fields at the associated routes.

    When using, the router subclass (with the same field names as this model) should be
    passed as its generic type argument.

    ```py
    from fieldrouter import R, Route, Routed, Router


    class Where(Router):
        some_value: Route = "example.subpath.0"


    class What(Routed[R]):
        some_value: int


    data = {"example": {"subpath": [100]}}
    result = What[Where].model_validate(data).some_value  # 100
    ```
    """

    @model_validator(mode="before")
    def supply_routes(cls, data: dict):
        values = dict(data)  # Make a copy
        route_model = cls.__pydantic_generic_metadata__["args"][0]
        router = route_model()
        for field, route in router.model_dump().items():
            if is_identity_route := route == ["", ""]:  # noqa:F841
                values.update({field: data})
                continue
            elif has_referent_root := route[0] == "":  # noqa:F841
                # This could fail if the referent doesn't exist or the route's malformed
                referent = route[1]
                path = route[2:]
                source = values[referent]
            else:
                path = route
                source = data
            values.update({field: extract_subpath(path=path, data=source)})
        for unrouted_field in set(cls.model_fields) - set(router.model_fields):
            reporter = ValueError(f"No route for {unrouted_field}")
            values.update({unrouted_field: reporter})
        return values
