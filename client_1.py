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
testing_button_topic = "Add/Your/Topic"
previous_light_topic = "Add/Your/Topic"
light_topic = "Add/Your/Topic"

# Global communication. Nothing to do.
previous_light_status = "OFF"
testing_button = "OFF"


async def listen():
    global previous_light_status
    global testing_button

    async with aiomqtt.Client(
            hostname=os.getenv("MQTT_BROKER_HOST"),
            username=os.getenv("MQTT_BROKER_USERNAME"),
            password=os.getenv("MQTT_BROKER_PASSWORT"),
    ) as client:
        await client.subscribe(previous_light_topic)
        await client.subscribe(testing_button_topic)

        async for message in client.messages:

            if message.topic.matches(testing_button_topic):
                testing_button = message.payload.decode("UTF-8")
                print(f"[{testing_button_topic}] {testing_button}")

            if message.topic.matches(previous_light_topic):
                previous_light_status = message.payload.decode("UTF-8")
                print(f"[{previous_light_topic}] {previous_light_status}")


async def lighting_show():
    # Playground
    global previous_light_status
    global testing_button

    async with aiomqtt.Client(
            hostname=os.getenv("MQTT_BROKER_HOST"),
            username=os.getenv("MQTT_BROKER_USERNAME"),
            password=os.getenv("MQTT_BROKER_PASSWORT"),
    ) as client:
        while True:
            # Program your own Lightshow
            pass

            # await asyncio.sleep(0.5)


async def main():
    if check_config() is False:
        raise KeyError("Not all config parameters are set")

    async with asyncio.TaskGroup() as tg:
        tg.create_task(listen())
        tg.create_task(lighting_show())


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
