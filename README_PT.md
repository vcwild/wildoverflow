# wildOverflow Bot

O wildOverflow é um chatbot da Twitch construído sob o framework [TwitchIO](twitchio.readthedocs.io/).
O bot procura interagir com usuários novos no chat e fornecer comandos básicos de interação.

## Índice

- [Features](#features)
- [Como usar](#como-usar)
- [Para implementar](#próximos-passos)
- [Integrações](#integrações)
- [Sugestões e Bugs](#sugestões-e-bugs)
- [Sobre](#sobre)

## Features

Recursos existentes no bot:

- Comandos parametrizados de acordo com o nome do canal que o bot está
- Saudação quando uma nova pessoa se junta ao chat
- Mandar um sh quando encontrar um streamer que se juntou ao chat
- Sistema de cache com Redis
- Lembrar dos usuários que já interagiu

## Como usar

### Pré-requisitos

Serão necessários os seguintes pré-requisitos

- [Poetry](https://python-poetry.org/)
- Python >= 3.6
- [Docker-compose](https://docs.docker.com/compose/)
- Requisição de um [Twitch OAuth Token](https://twitchapps.com/tmi/)

### Setup

- Subir o cache do bot em um container docker

```sh
docker-compose up -d
```

- Instalar as dependências do bot

```sh
poetry install
```

- Renomear o arquivo `.env_mock` para `.env` e configurar o bot com suas credenciais

- Iniciar o bot

```sh
poetry run bot.py
```

### Como usar o bot

Basta interagir com o bot no chat utilizando:

`@wildOverflow [comando]` ou `![comando]`

## Integrações

- Hub API (em desenvolvimento)

## Sugestões e bugs

Encontrou algum bug ou gostaria de sugerir um recurso para colocar no bot?
Fique à vontade para abrir uma issue.

## Sobre

O projeto está sob a licença *Gnu General Public License 3.0*.
