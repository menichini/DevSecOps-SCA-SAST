# DevSecOps-SCA-SAST

Projeto com o objetivo de estruturar pipeline com a integração das práticas DevSecOps. 

## Sobre

Esse projeto pega os dados de uma planilha do google spreadsheets e carrega os dados para um banco de dados Postgres. As credenciais aqui colocadas foram descaracterizadas para poder simular um ambiente caótico com relação a segurança, além de implementar segurança com uma aplicação que possa vir a ser melhorada e utilizada futuramente com base em um contexto de negócio.

## Build

Em virtude desse projeto ser feito com Python, considere instalar, em sua máquina através de uma das formas especificadas [aqui](https://python.org.br/). Para o gerenciamento das dependências, considere os passos abaixos.

```sh
# Dependências para o pyenv
sudo apt-get install build-essential zlib1g-dev libffi-dev libssl-dev libbz2-dev libreadline-dev libsqlite3-dev liblzma-dev tk-dev
# Instalação do pyenv para gerenciar versões do python
curl https://pyenv.run | bash
# Configuração de ambiente do pyenv (fazer o export e eval sempre que inicializar o terminal)
export PYENV_ROOT="$HOME/.pyenv"
[[ -d $PYENV_ROOT/bin ]] && export PATH="$PYENV_ROOT/bin:$PATH"
eval "$(pyenv init -)"
# Instalar a mesma versão do python utilizada pela equipe
pyenv install 3.12.4
# Selecionar a versão do python pro repositório
pyenv local 3.12.4
# Instalação e configuração do poetry
pip install poetry
poetry env use 3.12.4
poetry install --no-root
```

Utilizamos [pré-commit](https://pre-commit.com/) para inspeção antes do código chegar ao repositório remoto.
```sh
poetry run pre-commit install
```
