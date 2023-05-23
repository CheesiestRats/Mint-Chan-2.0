import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

# Using Chrome to access the web
driver = webdriver.Chrome()
driver.get('http://127.0.0.1:7862')

wait = WebDriverWait(driver, 20)  # Increase the timeout to 20 seconds

# Find the textarea element
textbox = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'textarea[data-testid="textbox"]')))

# Enter a loop to keep the script running
while True:
    user_input = input("Enter text (or 'quit' to exit): ")
    
    if user_input.lower() == 'quit':
        break  # Exit the loop and terminate the script
    
    textbox.clear()  # Clear any existing text
    textbox.send_keys(user_input)
    textbox.send_keys(Keys.RETURN)  # Simulate pressing the Enter key to submit the text
    
    time.sleep(2)  # Wait for 2 seconds
    
    try:
        # Wait until div.prose.svelte-1ybaih5.min is no longer visible
        message_body_locator = (By.CSS_SELECTOR, 'div.prose.svelte-1ybaih5.min')
        wait.until_not(EC.visibility_of_element_located(message_body_locator))
        
        # Retrieve the generated text from the first message-body div
        message_body_element = driver.find_element(By.CSS_SELECTOR, 'div.prose.svelte-1ybaih5 div.chat div.message div.text div.message-body p')
        generated_text = message_body_element.text
        print("Generated text:", generated_text)
        
    except Exception as e:
        print("An error occurred:", e)
        continue

# Close the driver
driver.quit()