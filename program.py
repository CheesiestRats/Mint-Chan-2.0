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

# Set the user ID of the specific user who can clear history
OWNER_ID = os.getenv('OWNER_ID')

intents = discord.Intents.all()
client = discord.Client(intents=intents)

data_directory = os.path.join(os.getcwd(), 'chrome-data')  # Set the custom data directory location

chrome_options = Options()
chrome_options.add_argument(f"--user-data-dir={data_directory}")  # Specify the custom data directory

# Some Chrome Options
#chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

# Using Chrome to access the web
driver = webdriver.Chrome(options=chrome_options)
driver.get('http://127.0.0.1:7862')

wait = WebDriverWait(driver, 20)  # Increase the timeout to 20 seconds

# Find the textarea element
textbox = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'textarea[data-testid="textbox"]')))

@client.event
async def on_ready():
    print(f'Successfully logged in as {client.user.name}')

@client.event
async def on_message(message):
    try:
        if message.author == client.user:
            # Process the bot's own messages
            # (e.g., handle replies to its messages)
            if message.reference:
                # Check if the message is a reply to the bot's message
                replied_message = await message.channel.fetch_message(message.reference.message_id)
                if replied_message.author == client.user:
                    # This is a reply to the bot's message
                    # Implement your logic here
                    # You can access the replied message content using replied_message.content

                    # Example: Echo the replied message back
                    await message.channel.send(replied_message.content)

            return

        # Check if the message is in DM
        if isinstance(message.channel, discord.DMChannel):
            # Process messages in DM
            # Call the run function to generate a response
            prompt = message.content

            async with message.channel.typing():
                result = await asyncio.get_event_loop().run_in_executor(None, run, prompt)

            if result:
                await message.channel.send(result)
            else:
                await message.channel.send("Oopsie Woopsie, Blinky's computer had a little fucky wucky UwU")

            return

        content = message.content.lower()

        # Define the regex pattern to match the desired words.
        pattern = r'\bmint-chan|minty|she|her\b'

        # Check if the message is from the specific user who can clear history
        if str(message.author.id) == OWNER_ID and content == "clear history":
            await clear_history()

        # Check if the message contains any matches
        elif re.search(pattern, content):
            # Process the message and generate a response.
            prompt = message.content

            # Filter out non-BMP characters from the prompt
            prompt = remove_non_bmp_characters(prompt)

            async with message.channel.typing():
                result = await asyncio.get_event_loop().run_in_executor(None, run, prompt)

            if result:
                await message.reply(result)
            else:
                await message.reply("Oopsie Woopsie, Blinky's computer had a little fucky wucky UwU")

    except Exception as e:
        print(f"An error occurred: {str(e)}")

# Function to remove non-BMP characters from text
def remove_non_bmp_characters(text):
    non_bmp_pattern = re.compile('[^\u0000-\uFFFF]')
    return non_bmp_pattern.sub('', text)

async def clear_history():
    try:
        clear_button_locator = (By.XPATH, '//button[contains(text(), "Clear history")]')
        clear_button = wait.until(EC.element_to_be_clickable(clear_button_locator))
        clear_button.click()

        confirm_button_locator = (By.CSS_SELECTOR, 'button.lg.stop.svelte-1ipelgc')
        confirm_button = wait.until(EC.element_to_be_clickable(confirm_button_locator))
        confirm_button.click()

    except Exception as e:
        print(f"An error occurred while clearing history: {str(e)}")

def run(prompt):
    textbox.clear() # Clear any existing text
    textbox.send_keys(prompt)
    textbox.send_keys(Keys.RETURN) # Simulate pressing the Enter key to submit the text.

    time.sleep(1) # Wait for 1 second.

    try:
        # Wait until div.prose.svelte-1ybaih5.min is no longer visible
        message_body_locator = (By.CSS_SELECTOR, 'div.prose.svelte-1ybaih5.min')
        wait.until_not(EC.visibility_of_element_located(message_body_locator))
        
        # Retrieve the generated text from the first message-body div
        message_body_element = driver.find_element(By.CSS_SELECTOR, 'div.prose.svelte-1ybaih5 div.chat div.message div.text div.message-body p')
        generated_text = message_body_element.text
        return generated_text
    
    except Exception as e:
        error_message = "An error occurred: " + str(e)
        return error_message

client.run(TOKEN)