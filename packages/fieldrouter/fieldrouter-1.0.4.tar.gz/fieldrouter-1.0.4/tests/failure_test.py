from fieldrouter import Routing, RoutingModel


def test_bad_route():
    # Route miss due to incorrect type: leaf is a list not a dict
    class DataRouter(RoutingModel):
        a_value: Routing(int, "path.to.the.value.MISTYPE_MISS")

    data = {"path": {"to": {"the": {"value": [100]}}}}
    result = DataRouter.model_validate(data)


if __name__ == "__main__":
    test_bad_route()
