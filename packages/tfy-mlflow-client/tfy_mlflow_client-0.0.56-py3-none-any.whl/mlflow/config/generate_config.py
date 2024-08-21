# SERVICEFOUNDRY_SERVER_URL='' SVC_FOUNDRY_SERVICE_API_KEY='' AUTH_SERVER_URL='https://example.com' python mlflow/config/generate_config.py
import inspect
import os
import textwrap


def generate_config(api_route):
    class_name = "".join(word.capitalize() for word in api_route.name.split("_"))
    response_dto = {api_route.__dict__.get("response_model")}
    if response_dto:
        response_dto = response_dto.pop()
        if response_dto:
            response_dto = response_dto.__name__
    else:
        response_dto = {}

    request_dto_typedef = ""
    request_func_annotation = inspect.getfullargspec(api_route.endpoint).annotations
    if "request_dto" in request_func_annotation:
        request_dto = request_func_annotation["request_dto"].__name__
    else:
        fields = {}
        if isinstance(request_func_annotation, dict):
            for key, value in request_func_annotation.items():
                if inspect.isclass(value):
                    fields[key] = value.__name__
                else:
                    fields[key] = value
        if fields:
            fields = "\n".join(f"{key}: {value}" for key, value in fields.items())
        else:
            fields = "pass"

        request_dto = "RequestDtoType"
        request_dto_typedef = f"""\
class {request_dto}(typing.TypedDict):
{textwrap.indent(fields, "    ")}
"""

    class_definition = f"""\
class {class_name}:
{textwrap.indent(request_dto_typedef, "    ")}
    path = '{api_route.path}'
    method = '{api_route.methods.pop()}'
    response_dto = {response_dto}
    request_dto = {request_dto}
    """
    return class_definition


def main():
    this_dir = os.path.dirname(os.path.abspath(__file__))
    config_path = os.path.join(this_dir, "config.py")

    with open(config_path, "w") as f:
        f.write("")

    from mlflow.server import app

    total_write = [
        """\
import typing

import mlflow
from mlflow.dto.artifacts_dto import *
from mlflow.dto.auth_dto import *
from mlflow.dto.common_dto import *
from mlflow.dto.experiments_dto import *
from mlflow.dto.mlfoundry_artifacts_dto import *
from mlflow.dto.metrics_dto import *
from mlflow.dto.python_deployment_config_dto import *
from mlflow.dto.runs_dto import *

NoneType = typing.Type[None]
    """
    ]
    for route in app.routes:
        if any(part in route.path for part in ("/preview/", "/2.0mlflow/")):
            continue
        if route.path.startswith("/api/"):
            print("Mapping route: ", route.path)
            total_write.append(generate_config(route))

    with open(config_path, "w") as f:
        f.write("\n\n".join(total_write))


if __name__ == "__main__":
    main()
