from typing import Annotated, Any, TypeVar, Union
import json

from pydantic import (
    BaseModel,
    BeforeValidator,
    TypeAdapter,
    model_validator,
    ValidationError,
)

__all__ = ("Route", "Routing", "RoutingModel")

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


class Via:
    routes: Route | list[Route]

    def __init__(self, routes):
        self.routes = routes

    def __repr__(self):
        return f"Via(routes={self.routes})"


T = TypeVar("T")


def Routing(tp: T, via: str | list[str]) -> Annotated[T, Via]:
    match via:
        case list():
            routes = via
        case str():
            routes = [via]
        case _ as t:
            raise TypeError(f"Expected a route string or list of strings, got {t}")
    return Annotated[tp, Via(routes=routes)]


dict_ta = TypeAdapter(dict)
list_ta = TypeAdapter(list)


def throw_helpfully(via: str, report: str, ve: ValidationError):
    input_ = json.loads(ve.json())[0]["input"]
    raise TypeError(f"No {via} {report}: input={input_}") from None


def extract_subpath(path: Route, data: dict) -> Any:
    """Extract a subpath or else an error reporter fallback indicating where it failed."""
    if path == ["", ""]:
        return data
    # Validate to avoid finding a shape mismatch mid-way through the hierarchy
    for part_idx, part in enumerate(path):
        report = f"{part!r} on {path}"
        reporter = KeyError(report)
        match part:
            case str() as key:
                try:
                    dict_ta.validate_python(data)
                except ValidationError as ve:
                    throw_helpfully(via="dict", report=report, ve=ve)
                data = data.get(key, reporter)
            case int() as idx:
                try:
                    list_ta.validate_python(data)
                except ValidationError as ve:
                    throw_helpfully(via="list", report=report, ve=ve)
                data = (
                    data[idx]
                    if isinstance(data, list) and -len(data) <= idx < len(data)
                    else reporter
                )
        if data is reporter:
            break
    return data


class RoutingModel(BaseModel):
    """A model which should be subclassed to specify fields at the associated routes.

    ```py
    from typing import Annotated
    from fieldrouter.v2 import Route, RoutingModel


    class DataRouter(RoutingModel):
        some_value: Annotated[int, Route("example.subpath.0")]


    data = {"example": {"subpath": [100]}}
    result = DataRouter.model_validate(data).some_value  # 100
    ```
    """

    @model_validator(mode="before")
    def supply_routes(cls, data: dict):
        values = dict(data)  # Make a copy to mutate
        for field, route_meta in cls.model_fields.items():
            match route_meta.metadata:
                case [Via()]:
                    route_string = route_meta.metadata[0].routes[0]
                    route = split_route(route_string)
                    # A field reference is when the route begins with a . (e.g. ".foo")
                    # except the identity route (".") which reproduces the entire input
                    if route[0] == "" and route[1:] != [""]:
                        # This could fail if the referent doesn't exist or the route's malformed
                        if (referent := route[1]) not in values:
                            raise NameError(f"No such referent {referent}")
                        path = route[2:]
                        source = values[referent]
                    else:
                        path = route
                        source = data
                    route_data = extract_subpath(path=path, data=source)
                    values[field] = route_data
                case _:
                    pass  # Do not otherwise interfere with the data
        return values
