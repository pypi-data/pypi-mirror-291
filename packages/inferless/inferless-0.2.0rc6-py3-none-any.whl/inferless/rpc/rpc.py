import base64
import json
import os
import inspect
import types
import dill
import requests
import rich
from . import config_yaml
from inferless.auth.token import auth_header
from rich.console import Console
from rich.spinner import Spinner
from rich.live import Live


RUNTIME_BUILD_COMPLETED = "RUNTIME_BUILD_COMPLETED"
RUNTIME_BUILD_STARTED = "RUNTIME_BUILD_STARTED"
INFERENCE_COMPLETED = "INFERENCE_COMPLETED"
INFERENCE_STARTED = "INFERENCE_STARTED"
RUNTIME_CACHE_HIT = "RUNTIME_CACHE_HIT"


def call_rpc(func, config_path, *args, **kwargs):
    console = Console()
    spinner = Spinner("dots", "Processing...")
    live = Live(spinner, refresh_per_second=10, transient=True)
    live.start()
    payload = get_rpc_payload(func, config_path, *args, **kwargs)
    headers = get_rpc_headers()
    url = get_rpc_url()
    with requests.post(url, json=payload, stream=True, headers=headers, timeout=600) as response:
        spinner.text = "Getting Infra ready..."
        live.update(spinner)
        for line in response.iter_lines():
            if line:
                msg_type = line.decode("utf-8").split(":")[0]
                if msg_type == "event":
                    event = line.decode("utf-8")[6:]
                    if event == RUNTIME_BUILD_STARTED:
                        live.stop()
                        console.print("[green]Infra is ready \u2713[/green]")
                        spinner.text = "Building runtime..."
                        live = Live(spinner, refresh_per_second=10, transient=True)
                        live.start()
                    elif event == RUNTIME_BUILD_COMPLETED:
                        live.stop()
                        console.print("[green]Runtime is ready \u2713[/green]")
                        spinner.text = "Waiting for inference to start..."
                        live = Live(spinner, refresh_per_second=10, transient=True)
                        live.start()
                    elif event == RUNTIME_CACHE_HIT:
                        live.stop()
                        console.print("[green]Infra is ready \u2713[/green]")
                        console.print("[green]Runtime is ready \u2713[/green]")
                        spinner.text = "Waiting for inference to start..."
                        live = Live(spinner, refresh_per_second=10, transient=True)
                        live.start()
                    elif event == INFERENCE_STARTED:
                        live.stop()
                        spinner.text = "Execution started..."
                        live = Live(spinner, refresh_per_second=10, transient=True)
                        live.start()
                    elif event == INFERENCE_COMPLETED:
                        live.stop()
                        console.print("[green]Execution \u2713[/green]")
                        spinner.text = "Waiting for result..."
                        live = Live(spinner, refresh_per_second=10, transient=True)
                        live.start()
                elif msg_type == "result":
                    live.stop()
                    result = line.decode("utf-8")[7:]
                    return get_rpc_result(result)


def custom_serializer(func):
    # Extract the code object and the function's global scope
    func_globals = func.__globals__

    # To keep track of modules and attributes that are already serialized
    serialized_objects = {}
    serialized_modules = {}

    def serialize_object(obj, name=None):
        """Helper function to serialize a module, class, or function and its dependencies recursively."""
        if name and name in serialized_objects:
            return  # Already serialized

        if isinstance(obj, types.ModuleType):
            module_path = getattr(obj, '__file__', None)
            if module_path and os.path.isfile(module_path):
                if ('/System/Library/Frameworks/' in module_path or
                        '/Library/Frameworks/' in module_path or
                        '/lib/' in module_path or
                        'site-packages' in module_path or
                        'custom_serializer' in module_path):
                    # serialized_modules[obj.__name__] = obj
                    return

                module_source = inspect.getsource(obj)
                serialized_modules[obj.__name__] = module_source

                # Recursively serialize imports within this module
                for attr_name, attr_val in obj.__dict__.items():
                    if isinstance(attr_val, (types.ModuleType, types.FunctionType, type)):
                        serialize_object(attr_val, attr_name)

        elif isinstance(obj, (types.FunctionType, type)):
            # Handle serialization of functions and classes
            # skip built-in functions and classes
            try:
                if name is None:
                    name = obj.__name__
                # if name in ['custom_serializer', "__builtins__", "__loader__", "__name__", "__package__", "__spec__", "__main__"]:
                #     return
                # get object module's path
                module_path = inspect.getfile(obj)
                if ('/System/Library/Frameworks/' in module_path or
                        '/Library/Frameworks/' in module_path or
                        '/lib/' in module_path or
                        'site-packages' in module_path or
                        'custom_serializer' in module_path):
                    return

                # Serialize function or class
                source = inspect.getsource(obj)
                serialized_objects[name] = source

                # Recursively serialize any objects in the function's global scope
                if hasattr(obj, '__globals__'):
                    for glob_name, glob_val in obj.__globals__.items():
                        if isinstance(glob_val, (types.ModuleType, types.FunctionType, type)):
                            serialize_object(glob_val, glob_name)
            except Exception as e:
                return

    for name, val in func_globals.items():
        if isinstance(val, (types.ModuleType, types.FunctionType, type)):
            serialize_object(val, name)

    return func, serialized_objects, serialized_modules


def get_rpc_payload(func, config_path, *args, **kwargs):
    rpc_payload = {
        "func": func,
        "args": args,
        "kwargs": kwargs
    }
    serialized_rpc_payload = base64.b64encode(dill.dumps(rpc_payload, recurse=True)).decode("utf-8")
    configuration_yaml = config_yaml.get_config_yaml(config_path)
    payload = {
        "rpc_payload": serialized_rpc_payload,
        "configuration_yaml": configuration_yaml
    }
    return payload


def get_rpc_headers():
    token_header = auth_header()
    headers = token_header.update(
        {
            "Content-Type": "application/json",
            "Accept": "text/event-stream",
            "Transfer-Encoding": "chunked",
            "Connection": "keep-alive"
        }
    )
    return headers


def get_rpc_result(result):
    data = json.loads(result)
    request_id = data.get("request_id")
    result = data.get("result")
    try:
        output = json.loads(result)
        if output.get("error"):
            rich.print(f"\n[red]{output['error_msg']}[/red]\n")
            rich.print(f"{output['error']}")
            rich.print("\n[white].............................[/white]")
            raise SystemExit
        if output.get("logs"):
            rich.print(f"[blue]Standard Output[/blue]\n")
            rich.print(f"{output['logs']}")
            rich.print("\n[white].............................[/white]")
        if output.get("result"):
            return output.get("result")
        else:
            rich.print(f"[yellow]No result returned[/yellow]")
            return None
    except SystemExit:
        raise SystemExit
    except Exception as e:
        raise Exception(f"Internal error occurred. Request ID for reference: {request_id}, error: {e}")


def get_rpc_url():
    if os.getenv("INFERLESS_ENV") == "DEV":
        return "http://aab1b24401e6d40ee819a4a85da88501-394555867.us-east-1.elb.amazonaws.com/api/v1/rpc/start"

    return "https://serverless-region-v1.inferless.com/api/v1/rpc/start"
