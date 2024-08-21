# StashConnect

StashConnect is an easy-to-use API wrapper for [stashcat](https://stashcat.com/) and [schul.cloud](https://schul.cloud).

![PyPI - Downloads](https://img.shields.io/pypi/dm/stashconnect?labelColor=345165&color=4793c9)
![PyPI - Version](https://img.shields.io/pypi/v/stashconnect?label=version&labelColor=345165&color=4793c9)
![PyPI - Status](https://img.shields.io/pypi/status/stashconnect?labelColor=345165&color=44af68)

## Installation

To install StashConnect, use pip in your shell:

```bash
pip install -U stashconnect
```

## Example Usage

```python
import stashconnect

client = stashconnect.Client(
    email="your email", password="your password",
    encryption_password="encryption password",
)

# change account settings
client.account.change_status("new status")
client.account.change_password("new", "old")

# upload or download files
client.files.upload("conversation_id", "hello.png")
client.files.download("file_id")

client.messages.send("conversation_id", "hello")

# get the last 30 messages of a chat
last_messages = client.messages.get_messages("channel_id/conversation_id")
for message in last_messages:
    print(message.content)
```

## Features to be added

- [x] docstrings
- [ ] account functions
- [ ] documentation
- [ ] bot class

## Contributors

- All code currently written by [BuStudios](https://github.com/bustudios)
- Create a pull request to contribute code yourself

## Disclaimer

StashConnect is not affiliated with Stashcat GmbH or any of its affiliates.

<img src="https://raw.githubusercontent.com/BuStudios/StashConnect/main/assets/icon-full.png">
