import sys
import os

# Add the backend directory to the path so we can import modules
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from qdrant_client import QdrantClient
from config import QDRANT_HOST, QDRANT_API_KEY

print("Qdrant client methods:")
print([method for method in dir(QdrantClient) if not method.startswith('_')])

# Initialize client the same way as in vector_service.py
if QDRANT_HOST.startswith(('http://', 'https://')):
    client = QdrantClient(
        url=QDRANT_HOST,
        api_key=QDRANT_API_KEY,
        prefer_grpc=False
    )
else:
    from config import QDRANT_PORT
    client = QdrantClient(
        host=QDRANT_HOST,
        port=QDRANT_PORT,
        api_key=QDRANT_API_KEY,
    )

print("\nClient instance methods:")
print([method for method in dir(client) if not method.startswith('_') and 'search' in method.lower()])

hasattr_search = hasattr(client, 'search')
print(f"\nHas 'search' attribute: {hasattr_search}")