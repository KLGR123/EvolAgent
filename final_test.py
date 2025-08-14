#!/usr/bin/env python3
import sys
import os
sys.path.insert(0, 'src')

# Import interpreter directly without going through __init__.py  
from utils.interpreter import create_enhanced_config, PythonInterpreter

print('=' * 60)
print('FINAL ENHANCED INTERPRETER TEST')
print('=' * 60)

print('Step 1: Successfully imported enhanced interpreter')

# Test configuration
config = create_enhanced_config()
print('Step 2: Configuration created')

# Test interpreter creation
interpreter = PythonInterpreter(config)
print('Step 3: Interpreter created')

# Test simple execution
print('\nStep 4: Testing simple execution...')
result = interpreter.execute('print("Hello from enhanced interpreter!")')
print('Result:')
print(result)

# Test web browsing environment
print('\nStep 5: Testing web browsing environment setup...')
env_test_code = '''
import os
print("Web browsing environment variables:")
web_vars = ["DISPLAY", "CHROME_BIN", "WDM_LOG_LEVEL", "USER_AGENT"]
for var in web_vars:
    value = os.environ.get(var, "Not set")
    print(f"  {var}: {value}")
'''

result = interpreter.execute(env_test_code)
print('Result:')
print(result)

# Test selenium with enhanced error handling
print('\nStep 6: Testing selenium with enhanced error handling...')
selenium_test_code = '''
try:
    from selenium import webdriver
    from selenium.webdriver.chrome.options import Options
    
    print("Setting up Chrome WebDriver...")
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-dev-shm-usage")
    
    driver = webdriver.Chrome(options=options)
    print("✓ WebDriver created successfully")
    
    # Simple test
    driver.get("data:text/html,<html><body><h1>Test Page</h1></body></html>")
    title = driver.title
    print(f"✓ Page title: {title}")
    
    driver.quit()
    print("✓ Enhanced interpreter selenium test: SUCCESS!")
    
except Exception as e:
    print(f"Selenium test failed: {e}")
    # This should trigger our enhanced error handling
    raise e
'''

result = interpreter.execute(selenium_test_code)
print('Result:')
print(result)

print('\n' + '=' * 60)
print('ENHANCED INTERPRETER TEST COMPLETED')
print('=' * 60)
