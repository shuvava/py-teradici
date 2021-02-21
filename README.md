# Teradici Technical Assessment

## Usage

1. [build docker file](#Docker Build) 
1. [run docker compose](#Run)
1. open url `http://127.0.0.1:8080/docs#/`

## Development 

### Environment Configuration

1. instal pipenv

    ```sh
    pip install pipenv
    ```

1. instal dependencies

    ```sh
    pipenv install
    ```

1. get environment path

    ```sh
    pipenv --py
    ```
1. if you are using VS Code update launch.json pythonPath variable

```json
{
    "pythonPath": "/home/myuser/.local/share/virtualenvs/projectname/bin/python"
}
```

### pip env usage

* To activate this project's virtualenv, run

    ```sh
    pipenv shell
    ```

* Alternatively, run a command inside the virtualenv with

    ```sh
    pipenv run python main.py
    ```

### Docker Build

1. run bash script `./scripts/build.sh`

### Run

to run app in docker
1. create docker image using [build command](#DockerBuild) 
1. run bash script `./scripts/run.sh`

### Unit Test

#### Run in Docker

to run unit-tests

1. build test container 

```shell
  docker-compose -f docker-compose.test.yml build
```

1. run unit-test

```shell
docker-compose -f docker-compose.test.yml up
```

#### Run in pipenv

1. run `pipenv shell`
1. run `./tests/run.sh`

## Publishing

run bash script `./scripts/publish.sh`

## Links 

* [Technical Assessment](./docs/FullStackDeveloperTakehomeAssessment.pdf)
