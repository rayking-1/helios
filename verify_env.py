import os
from dotenv import load_dotenv, find_dotenv
import sys

print("--- Running .env Verification Script ---")

# Find and load the .env file from the project root
# This approach is more robust as it will search upward from the current directory
dotenv_path = find_dotenv()
if not dotenv_path:
    print("❌ FAILURE: .env file not found anywhere in the project directory tree.")
    sys.exit(1)

try:
    # Attempt to load the .env file
    loaded = load_dotenv(dotenv_path=dotenv_path, verbose=True)
    if not loaded:
         print(f"❌ FAILURE: .env file was found but could not be loaded. Check file permissions.")
         sys.exit(1)

    print(f"\n✅ SUCCESS: .env file loaded successfully from: {dotenv_path}")
except Exception as e:
    print(f"❌ CRITICAL FAILURE: Error parsing .env file: {e}")
    print("   This often indicates an ENCODING ISSUE (e.g., saved with BOM).")
    print("   Please ensure the file is saved as 'UTF-8 without BOM'.")
    sys.exit(1)


# Verify that all required keys are present in the environment
required_keys = ['DASHSCOPE_API_KEY', 'DEEPSEEK_API_KEY']
missing_keys = [key for key in required_keys if not os.getenv(key)]

if not missing_keys:
    print("✅ SUCCESS: All required environment variables are loaded correctly.")
    print("\n--- Verification Complete: You can now safely start the main application. ---")
else:
    print(f"\n❌ FAILURE: The following required keys are missing: {', '.join(missing_keys)}")
    print("   Please check your .env file content for typos or missing lines.")
    sys.exit(1) 