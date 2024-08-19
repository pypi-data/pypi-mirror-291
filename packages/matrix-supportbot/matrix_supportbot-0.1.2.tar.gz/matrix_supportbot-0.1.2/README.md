# Matrix Support Bot

[![Support Private.coffee!](https://shields.private.coffee/badge/private.coffee-support%20us!-pink?logo=coffeescript)](https://private.coffee)

Matrix Support Bot is a support ticket bot for the Matrix protocol built using the `matrix-nio` library. The bot allows users to open support tickets and communicate with support operators in a structured manner. Operators can manage tickets and relay messages between customer-facing and operator-facing rooms.

## Features

- The bot's state is stored in a Matrix room, so no external database is required.
- Users can invite the bot to a direct message (DM) and receive instructions on how to open a support ticket.
- Users can open support tickets using the `!supportbot openticket` command.
- The bot creates a new customer-facing room for each ticket and invites the user to it.
- Operators are notified of new tickets in a shared operator room.
- Operators can join operator-facing rooms for each ticket and communicate with customers.
- Messages between customer-facing and operator-facing rooms are relayed by the bot.
- Operators can close tickets and list open tickets using bot commands.
- Supports relaying of different message types, including text and media.

## Commands

### User Commands

- `!supportbot openticket` - Opens a new support ticket and creates a customer-facing room.

### Operator Commands

- `!supportbot invite <ticket_id>` - Invites an operator to the operator-facing room for the specified ticket.
- `!supportbot close <ticket_id>` - Closes the specified ticket.
- `!supportbot list` - Lists all open tickets.

## Installation

1. Install from PyPI:

   ```bash
   pip install matrix-supportbot
   ```

2. Create a `config.yaml` file with your Matrix credentials and operator room ID:

   ```yaml
   homeserver: "https://homeserver.example"
   username: "your_username"
   password: "your_password"
   operator_room_id: "!your_operator_room_id:homeserver.example"
   ```

## Usage

Run the bot with the following command:

```bash
supportbot
```

The bot will log in to your Matrix server, join the operator room, and start listening for commands and invites.

## Contributing

Contributions are welcome! Please fork the repository and create a pull request with your changes.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
