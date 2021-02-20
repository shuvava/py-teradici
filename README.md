# Teradici Technical Assessment

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

### Docker

to run app in docker
1. create docker image using [publish command](#Publishing) 
1. run bash script `./scripts/run.sh`

## Publishing

run bash script `./scripts/publish.sh`

## Links 

* [Technical Assessment](./docs/FullStackDeveloperTakehomeAssessment.pdf)
