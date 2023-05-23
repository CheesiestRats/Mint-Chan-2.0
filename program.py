import os
import time

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

import re

import asyncio
import discord
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

intents = discord.Intents.all()
client = discord.Client(intents=intents)

data_directory = os.path.join(os.getcwd(), 'chrome-data')  # Set the custom data directory location

chrome_options = Options()
chrome_options.add_argument(f"--user-data-dir={data_directory}")  # Specify the custom data directory

# Using Chrome to access the web
driver = webdriver.Chrome(options=chrome_options)
driver.get('http://127.0.0.1:7862')

wait = WebDriverWait(driver, 20)  # Increase the timeout to 20 seconds

# Find the textarea element
textbox = WebDriverWait(driver, 10).until(
    EC.visibility_of_element_located((By.CSS_SELECTOR, 'textarea[data-testid="textbox"]'))
)

@client.event
async def on_ready():
    print(f'Successfully logged in as {client.user.name}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    content = message.content.lower()

    # Define the regex pattern to match the desired words.
    pattern = r'\bmint-chan|minty|she|her\b'

    # Check if the message contains any matches
    if re.search(pattern, content):
        # Process the message and generate a response.
        prompt = message.content

        async with message.channel.typing():
            result = await asyncio.get_event_loop().run_in_executor(None, run, prompt)

        if result:
            await message.reply(result)
        else:
            await message.reply("Oopsie Woopsie, Blinky's computer had a little fucky wucky UwU")

def run(prompt):
    textbox.clear()  # Clear any existing text
    textbox.send_keys(prompt)
    textbox.send_keys(Keys.RETURN)  # Simulate pressing the Enter key to submit the text.

    time.sleep(1)  # Wait for 1 second.

    try:
        # Wait until div.prose.svelte-1ybaih5.min is no longer visible
        message_body_locator = (By.CSS_SELECTOR, 'div.prose.svelte-1ybaih5.min')
        wait.until_not(EC.visibility_of_element_located(message_body_locator))

        # Retrieve the generated text from the first message-body div
        message_body_element = driver.find_element(By.CSS_SELECTOR,
                                                   'div.prose.svelte-1ybaih5 div.chat div.message div.text div.message-body p')
        generated_text = message_body_element.text
        return generated_text

    except Exception as e:
        error_message = "An error occurred: " + str(e)
        return error_message

client.run(TOKEN)