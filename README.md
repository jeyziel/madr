## Iniciando o Projeto

Para iniciar o projeto utilize o pyenv para setar a versão do python para a 3.13.0.
```shell
pyenv local 3.13.0
```

Após isso, instale as dependências do projeto utilizando o poetry:

```shell
poetry install
```

Depois, verifique se os testes unitários estão todos passando:

1º - Entre no poetry shell
```shell
poetry shell
```


2º - Execute os testes
```shell
task test
```

3º - Por fim, rode o projeto:

```shell
task run
```


## Documentação da api

- http://localhost:8000/docs

## Dependências do Projeto:
 - pyenv
 - poetry