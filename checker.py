import asyncio
import os
import sys

import aiomqtt
from dotenv import load_dotenv

from solution.load_config import check_config

load_dotenv()

# Change to the "Selector" event loop if platform is Windows
if sys.platform.lower() == "win32" or os.name.lower() == "nt":
    from asyncio import set_event_loop_policy, WindowsSelectorEventLoopPolicy

    set_event_loop_policy(WindowsSelectorEventLoopPolicy())

# Add your topic
test_topic = "test/message"


async def listen():
    async with aiomqtt.Client(
            hostname=os.getenv("MQTT_BROKER_HOST"),
            username=os.getenv("MQTT_BROKER_USERNAME"),
            password=os.getenv("MQTT_BROKER_PASSWORT"),
    ) as client:
        await client.subscribe(test_topic)

        async for message in client.messages:

            if message.topic.matches(test_topic):
                testing_button = message.payload.decode("UTF-8")
                print(f"[{test_topic}] {testing_button}")


async def main():
    if check_config() is False:
        raise KeyError("Not all config parameters are set")

    async with asyncio.TaskGroup() as tg:
        tg.create_task(listen())


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
