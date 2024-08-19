import random
from nio import (
    AsyncClient,
    MatrixRoom,
    RoomMessageText,
    RoomMessageMedia,
    LoginResponse,
    RoomGetStateEventResponse,
    InviteMemberEvent,
    JoinedMembersResponse,
    RoomPutStateResponse,
)

import logging


class SupportBot:
    def __init__(self, config):
        self.client = AsyncClient(config["homeserver"], config["username"])
        self.username = config["username"]
        self.password = config["password"]
        self.operator_room_id = config["operator_room_id"]

    async def login(self):
        response = await self.client.login(self.password)
        if isinstance(response, LoginResponse):
            logging.info("Logged in successfully")
        else:
            logging.fatal("Failed to log in")

    async def is_operator(self, user_id):
        logging.info(f"Checking if {user_id} is an operator")

        response = await self.client.joined_members(self.operator_room_id)

        if not isinstance(response, JoinedMembersResponse):
            logging.error(f"Failed to get members in operator room: {response}")
            return False

        for member in response.members:
            if member.user_id == user_id:
                return True

        return False

    async def start(self):
        await self.client.sync(timeout=30000)
        self.client.add_event_callback(self.message_callback, RoomMessageText)
        self.client.add_event_callback(self.message_callback, RoomMessageMedia)
        self.client.add_event_callback(self.invite_callback, InviteMemberEvent)
        await self.client.sync_forever(timeout=30000)

    async def message_callback(self, room: MatrixRoom, event):
        sender = event.sender
        body = event.body if hasattr(event, "body") else None

        if body and body.startswith("!supportbot"):
            await self.handle_command(room, sender, body)
        else:
            await self.relay_message(room, sender, event)

    async def invite_callback(self, room: MatrixRoom, event: InviteMemberEvent):
        logging.info(f"Received invite event: {event}")

        if event.membership == "invite" and event.state_key == self.client.user_id:
            await self.client.join(room.room_id)
            await self.client.room_send(
                room.room_id,
                "m.room.message",
                {
                    "msgtype": "m.text",
                    "body": "Hello! To open a support ticket, please type `!supportbot openticket`.",
                },
            )

    async def handle_command(self, room, sender, command):
        if command == "!supportbot openticket":
            await self.open_ticket(room, sender)
            return
        elif await self.is_operator(sender):
            if command.startswith("!supportbot invite"):
                await self.invite_operator(room, sender, command)
            elif command.startswith("!supportbot close"):
                await self.close_ticket(room, sender, command)
            elif command == "!supportbot list":
                await self.list_tickets(room)
            return

        await self.client.room_send(
            room.room_id,
            "m.room.message",
            {
                "msgtype": "m.text",
                "body": "Sorry, I do not know this command, or you are not authorized to use it.",
            },
        )

    def generate_ticket_id(self):
        return str(random.randint(10000000, 99999999))

    async def open_ticket(self, room, sender):
        ticket_id = self.generate_ticket_id()
        customer_room_alias = f"Ticket-{ticket_id}"
        operator_room_alias = f"Operator-Ticket-{ticket_id}"

        # Create customer-facing room
        customer_room = await self.client.room_create(
            name=customer_room_alias, invite=[sender]
        )
        customer_room_id = customer_room.room_id

        # Create operator-facing room
        operator_room = await self.client.room_create(name=operator_room_alias)
        operator_room_id = operator_room.room_id

        # Update the state in the operator room
        state_event_key = f"ticket_{ticket_id}"
        state_event_content = {
            "ticket_id": ticket_id,
            "customer_room": customer_room_id,
            "operator_room": operator_room_id,
            "status": "open",
        }

        state_event_response = await self.client.room_put_state(
            room_id=self.operator_room_id,
            event_type="m.room.custom.ticket",
            state_key=state_event_key,
            content=state_event_content,
        )

        if not isinstance(state_event_response, RoomPutStateResponse):
            logging.error(
                f"Failed to update state in operator room: {state_event_response}"
            )
            return

        # Inform the operator room
        await self.client.room_send(
            self.operator_room_id,
            "m.room.message",
            {
                "msgtype": "m.text",
                "body": f"New ticket #{ticket_id} created by {sender}",
            },
        )

        # Inform customer
        await self.client.room_send(
            customer_room_id,
            "m.room.message",
            {
                "msgtype": "m.text",
                "body": f"Your ticket #{ticket_id} has been created. Please wait for an operator.",
            },
        )

        await self.client.room_send(
            room.room_id,
            "m.room.message",
            {
                "msgtype": "m.text",
                "body": f"Ticket #{ticket_id} has been created. Please check your DMs.",
            },
        )

    async def invite_operator(self, room, sender, command):
        ticket_id = command.split()[2]
        state_event_key = f"ticket_{ticket_id}"
        response = await self.client.room_get_state_event(
            self.operator_room_id, "m.room.custom.ticket", state_event_key
        )

        if isinstance(response, RoomGetStateEventResponse):
            operator_room_id = response.content["operator_room"]
            await self.client.room_invite(operator_room_id, sender)
        else:
            await self.client.room_send(
                room.room_id,
                "m.room.message",
                {"msgtype": "m.text", "body": f"Ticket #{ticket_id} does not exist."},
            )

    async def close_ticket(self, room, sender, command):
        parts = command.split()
        if len(parts) == 3:
            ticket_id = parts[2]
        else:
            ticket_id = await self.get_ticket_id_from_room(room.room_id)

        state_event_key = f"ticket_{ticket_id}"
        response = await self.client.room_get_state_event(
            self.operator_room_id, "m.room.custom.ticket", state_event_key
        )

        if isinstance(response, RoomGetStateEventResponse):
            ticket_info = response.content
            customer_room_id = ticket_info["customer_room"]
            operator_room_id = ticket_info["operator_room"]

            # Update ticket status
            ticket_info["status"] = "closed"
            await self.client.room_put_state(
                room_id=self.operator_room_id,
                event_type="m.room.custom.ticket",
                state_key=state_event_key,
                content=ticket_info,
            )

            await self.client.room_send(
                customer_room_id,
                "m.room.message",
                {
                    "msgtype": "m.text",
                    "body": f"Ticket #{ticket_id} has been closed. If you need further assistance, please open a new ticket.",
                },
            )
            await self.client.room_send(
                operator_room_id,
                "m.room.message",
                {"msgtype": "m.text", "body": f"Ticket #{ticket_id} has been closed."},
            )
        else:
            await self.client.room_send(
                room.room_id,
                "m.room.message",
                {"msgtype": "m.text", "body": f"Ticket #{ticket_id} does not exist."},
            )

    async def list_tickets(self, room):
        response = await self.client.room_get_state(self.operator_room_id)
        open_tickets = []

        for event in response.events:
            if event["type"] == "m.room.custom.ticket":
                ticket_info = event["content"]
                if ticket_info["status"] == "open":
                    open_tickets.append(ticket_info["ticket_id"])

        await self.client.room_send(
            room.room_id,
            "m.room.message",
            {
                "msgtype": "m.text",
                "body": f"Open tickets: {', '.join(map(str, open_tickets))}",
            },
        )

    async def get_ticket_id_from_room(self, room_id):
        # This method will be used to find the ticket ID based on the room ID
        # It will iterate over the state events in the operator room to find the matching ticket
        response = await self.client.room_get_state(self.operator_room_id)
        for event in response.events:
            if event["type"] == "m.room.custom.ticket":
                ticket_info = event["content"]
                if (
                    ticket_info["customer_room"] == room_id
                    or ticket_info["operator_room"] == room_id
                ):
                    return ticket_info["ticket_id"]
        return None

    async def relay_message(self, room, sender, event):
        # Ignore any messages from the bot itself
        if sender == self.client.user_id:
            return

        ticket_id = await self.get_ticket_id_from_room(room.room_id)
        if ticket_id:
            state_event_key = f"ticket_{ticket_id}"
            response = await self.client.room_get_state_event(
                self.operator_room_id, "m.room.custom.ticket", state_event_key
            )

            if isinstance(response, RoomGetStateEventResponse):
                ticket_info = response.content
                target_room_id = (
                    ticket_info["operator_room"]
                    if room.room_id == ticket_info["customer_room"]
                    else ticket_info["customer_room"]
                )

                # Relay the entire event content to the target room
                await self.client.room_send(
                    target_room_id, "m.room.message", event.source["content"]
                )
