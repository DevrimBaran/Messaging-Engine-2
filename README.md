# Messaging Engine 2

A complete rewrite of
the [PIME (Python IoT Messaging Engine) Proof-of-Concept implementation](https://gitlab-as.informatik.uni-stuttgart.de/hirmerpl/MA_Del_Gaudio)
.

## Build & Run

This project uses Python's `venv` feature and Python 3.8+. Read more about it
[here](https://packaging.python.org/en/latest/guides/installing-using-pip-and-virtual-environments/)
or [here](https://docs.python.org/3/library/venv.html).

The following commands will set up a local Python development environment for this project:

For Raspberry Pi:
```console
make setup-venv-raspi
make setup
```

For other devices:
```console
make setup-venv
make setup
```

## Continuous Integration (CI)

This project uses a custom image to run the CI jobs in. The [Dockerfile](Dockerfile_build) can be found here.

## Guidelines

### Development guidelines

- Use standard-libraries whenever possible
- Use `asyncio` for I/O operations and task/coroutine management
- Use `make` as build tool
- Development should work across different OS
- Use code linting (`make lint`)

### Git guidelines

- **Branch name**: Use `feature/ME2-[Issue number] [optional: very short description]` for features
  and `fix/ME2-[Issue number]` for bugfixes

  ```
  git checkout -b feature/ME2-23 database
  
  git checkout -b fix/ME2-25
  ```

- **Commit message**: Use `ME2-[Issue number] [your message]`. <br>
  Message length should be up to 50 characters. <br>
  Each commit must belong to an issue number. If there is none, create a new issue!

  ```
  git commit -m "ME2-23 add new database"
  
  git commit -m "ME2-25 fix wrong button color"
  ```

### GitLab guidelines

- **Issues**: Each issue should include an understandable `description` and, if possible, the `acceptance criterias`

## Documentation

The documentation is written using Markdown format for texts and PlantUML for diagrams.
It's located in [docs](docs) directory.

## Development Tools

### CoAp-Client

Execute in venv:

```
aiocoap-client coap://localhost/health
```

### Docker-Compose

There is an example scenario running three instances of ME2 in a docker-compose setup for easy testing.
You can use `ip`, `ping` and `aiocoap-client` command inside the container.

#### Usage

```bash
# Build Image
docker-compose build
docker-compose up

# Get a bash shell in a specific container
docker exec -ti me2_[first|second|third] bash
```

## Libraries

- [aiocoap](https://github.com/chrysn/aiocoap)
- [pyzmq](https://github.com/zeromq/pyzmq)

## Testing

TBD. There is an [example unit test](test/simple_test.py).
