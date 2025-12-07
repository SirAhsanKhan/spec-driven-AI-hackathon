import asyncio
import requests
import time
from config import get_content_url
from utils.logging import get_logger

logger = get_logger(__name__)

def test_complete_workflow():
    """
    Test the complete RAG chatbot workflow:
    1. Check system status
    2. Initialize content from URL
    3. Query the system after initialization
    4. Verify response and citations
    """
    base_url = "http://localhost:8000"
    content_url = get_content_url()
    
    if not content_url:
        logger.error("No CONTENT_URL configured in environment")
        return False
    
    logger.info("Starting end-to-end test of RAG Chatbot workflow")
    
    # Test 1: Check system status
    logger.info("Test 1: Checking system status")
    try:
        response = requests.get(f"{base_url}/api/status")
        if response.status_code == 200:
            status_data = response.json()
            logger.info(f"System status: {status_data['status']}")
        else:
            logger.error(f"Failed to get status: {response.status_code}")
            return False
    except Exception as e:
        logger.error(f"Error checking system status: {e}")
        return False
    
    # Test 2: Initialize content (this might take some time)
    logger.info("Test 2: Initializing content from URL")
    try:
        response = requests.post(f"{base_url}/api/initialize")
        if response.status_code == 200:
            init_data = response.json()
            job_id = init_data.get("job_id")
            logger.info(f"Initialization started with job ID: {job_id}")
        else:
            logger.error(f"Failed to start initialization: {response.status_code}, {response.text}")
            return False
    except Exception as e:
        logger.error(f"Error starting initialization: {e}")
        return False
    
    # Wait for initialization to complete
    logger.info("Waiting for initialization to complete...")
    max_wait_time = 120  # 2 minutes max wait
    wait_interval = 5  # 5 seconds between checks
    elapsed_time = 0
    
    while elapsed_time < max_wait_time:
        try:
            response = requests.get(f"{base_url}/api/initialize/{job_id}")
            if response.status_code == 200:
                job_status = response.json()
                logger.info(f"Initialization progress: {job_status.get('progress', 0)}%")
                
                if job_status.get("status") == "completed":
                    logger.info("Content initialization completed successfully")
                    break
                elif job_status.get("status") == "failed":
                    logger.error(f"Content initialization failed: {job_status.get('error')}")
                    return False
            else:
                logger.error(f"Failed to check job status: {response.status_code}")
                return False
        except Exception as e:
            logger.error(f"Error checking job status: {e}")
            return False
        
        time.sleep(wait_interval)
        elapsed_time += wait_interval
    
    if elapsed_time >= max_wait_time:
        logger.error("Initialization timed out")
        return False
    
    # Test 3: Query the system
    logger.info("Test 3: Querying the system")
    try:
        query_data = {"query": "What is this content about?"}
        response = requests.post(f"{base_url}/api/query", json=query_data)
        
        if response.status_code == 200:
            query_result = response.json()
            logger.info(f"Query response received: {query_result['response'][:100]}...")
            
            if "sources" in query_result and len(query_result["sources"]) > 0:
                logger.info(f"Sources cited: {query_result['sources']}")
            else:
                logger.warning("No sources cited in response")
                
            return True
        else:
            logger.error(f"Query failed: {response.status_code}, {response.text}")
            return False
    except Exception as e:
        logger.error(f"Error querying the system: {e}")
        return False

if __name__ == "__main__":
    logger.info("Running end-to-end test...")
    success = test_complete_workflow()
    if success:
        logger.info("End-to-end test completed successfully!")
    else:
        logger.error("End-to-end test failed!")