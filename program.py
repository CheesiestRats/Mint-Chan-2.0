import os
import time
import asyncio
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

import discord
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

intents = discord.Intents.all()
client = discord.Client(intents=intents)

# Using Chrome to access the web
driver = webdriver.Chrome()
driver.get('http://127.0.0.1:7862')

wait = WebDriverWait(driver, 20)  # Increase the timeout to 20 seconds

# Find the textarea element
textbox = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'textarea[data-testid="textbox"]')))

@client.event
async def on_ready():
    print(f'Successfully logged in as {client.user.name}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('!generate'):
        prompt = message.content[10:]

        async with message.channel.typing():
            result = await asyncio.get_event_loop().run_in_executor(None, run, prompt)

        if result:
            await message.channel.send(result)
        else:
            await message.channel.send("I'm sorry, I couldn't generate a response for that prompt.")

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