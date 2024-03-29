# wildOverflow Bot

wildOverflow is a Twitch chatbot built with the [TwitchIO](twitchio.readthedocs.io/) framework.
The bot greets joining chatters and has basic command interactions. If a joining chatter is a streamer, the bot will send a shoutout to that person's channel.

## Table of Contents

- [Features](#features)
- [Usage](#usage)
- [Integrations](#integrations)
- [Contribute](#contribute)
- [Bugs & suggestions](#bugs-and-suggestions)
- [About](#about)

## Features

Existing resources:

- Parameterized commands according to the context of the channel the bot is on
- Greeting message when a new person joins the chat
- Send a sh when a streamer has joined the chat
- User caching
- Reminds its recent interactions

## Usage

### Requirements

The following prerequisites will be needed

- [Poetry](https://python-poetry.org/)
- Python >= 3.6
- [Docker-compose](https://docs.docker.com/compose/)
- [Twitch OAuth Token](https://twitchapps.com/tmi/)

### Setup

There are 2 ways you can configure wildOverflow to work

#### 1. Simple use

- Clone the repository
- Rename `.env.example` to `.env` and configure the bot credentials
- Mount the bot cache in a docker container

```sh
docker-compose up -d
```

#### 2. Setup via development environment

- Mount the bot cache in a docker container

```sh
docker-compose up -d
```

- Install bot dependencies

```sh
poetry install
```

- Rename `.env.example` to `.env` and configure the bot credentials

- Run the bot

```sh
poetry run bot.py
```

### How to use

Main commands are [listed here](https://vcwild.github.io/wildoverflow)

## Integrations

- Hub API (in development)

## Contribute

If you want to contribute to the project, please read before our [CONTRIBUTING](./CONTRIBUTING.md) policy.

## Bugs and suggestions

Did you find a bug or you would like to suggest a feature to put in the bot?
Please feel free to reach out and open an issue.

## About

The project is under the *Gnu General Public License 3.0*.
