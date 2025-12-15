import asyncio
import sys
import os

# Add the backend directory to the path so we can import modules
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from services.vector_service import clear_collection, init_qdrant_collection
from config import validate_config

async def main():
    print("Validating configuration...")
    try:
        validate_config()
        print("Configuration is valid.")
    except ValueError as e:
        print(f"Configuration error: {e}")
        return

    print("Initializing Qdrant collection...")
    init_result = init_qdrant_collection()
    if not init_result:
        print("Failed to initialize Qdrant collection.")
        return
    
    print("Clearing Qdrant collection...")
    clear_result = await clear_collection()
    if not clear_result:
        print("Failed to clear Qdrant collection.")
        return

    print("Qdrant collection cleared successfully.")
    print("Now you should re-initialize the content via the API:")
    print("curl -X POST \"http://localhost:8000/api/initialize\" -H \"accept: application/json\" -H \"Content-Type: application/json\"")

if __name__ == "__main__":
    asyncio.run(main())