# Messaging Engine 2

A complete rewrite of
the [PIME (Python IoT Messaging Engine) Proof-of-Concept implementation](https://gitlab-as.informatik.uni-stuttgart.de/hirmerpl/MA_Del_Gaudio)
.

## Build & Run

This project uses Python's `venv` feature and Python 3.8+. Read more about it
[here](https://packaging.python.org/en/latest/guides/installing-using-pip-and-virtual-environments/)
or [here](https://docs.python.org/3/library/venv.html).

The following commands will set up a local Python development environment for this project:

```console
make setup-venv
make setup
```

## Continuous Integration (CI)

This project uses a custom image to run the CI jobs in. The [Dockerfile](Dockerfile_build) can be found here.

## Development guidelines

- Use standard-libraries whenever possible
- Use `asyncio` for I/O operations and task/coroutine management
- Use `make` as build tool
- Development should work across different OS
- Use code linting (`make lint`)

## Documentation

The documentation is written using Markdown format for texts and PlantUML for diagrams.
It's located in [docs](docs) directory.

## Development Tools

### CoAp-Client

Execute in venv:

```
aiocoap-client coap://localhost/health
```

## Libraries

- [aiocoap](https://github.com/chrysn/aiocoap)
- [pyzmq](https://github.com/zeromq/pyzmq)

## Testing

TBD. There is an [example unit test](test/simple_test.py).