import openai
from config import OPENAI_API_KEY
from typing import List, Dict
from utils.logging import get_logger
import asyncio

logger = get_logger(__name__)

# Initialize OpenAI client
client = openai.AsyncClient(api_key=OPENAI_API_KEY)

async def generate_response(user_query: str, context_chunks: List[Dict], out_of_context_message: str = "I cannot answer that question based on the available content.") -> str:
    """
    Generate a response using OpenAI's GPT model with the provided context
    """
    # Construct the context from relevant chunks
    context_text = ""
    sources = []

    for chunk in context_chunks:
        context_text += f"Source: {chunk.get('source_url', 'Unknown')}\n"
        context_text += f"Content: {chunk.get('content', '')}\n\n"
        if chunk.get('source_url') not in sources:
            sources.append(chunk.get('source_url'))

    # If no context chunks were found, return out-of-context message
    if not context_chunks or not context_text.strip():
        return out_of_context_message

    # Create the prompt for the AI model
    prompt = f"""
    You are a helpful assistant that answers questions based on the provided context.
    Only use the information from the context provided below to answer the user's question.
    If the question cannot be answered based on the provided context, respond with: "{out_of_context_message}"

    Context:
    {context_text}

    User question: {user_query}

    Answer:
    """

    try:
        # Generate response using OpenAI
        response = await client.chat.completions.create(
            model="gpt-3.5-turbo",  # You might want to use gpt-4 for better results if available
            messages=[
                {"role": "system", "content": "You are a helpful assistant that answers questions based only on the provided context. If the question cannot be answered with the provided context, say that you don't know based on the available information. When providing information from the context, mention the source URL if relevant."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=500,  # Adjust as needed
            temperature=0.7  # Adjust creativity of responses
        )

        # Extract the generated text
        generated_text = response.choices[0].message.content.strip()

        logger.info(f"Generated response for query: {user_query[:50]}...")
        return generated_text

    except openai.AuthenticationError:
        logger.error("OpenAI API authentication failed")
        return "Sorry, there was an issue with the AI service. Please check the API key configuration."

    except openai.RateLimitError:
        logger.error("OpenAI API rate limit exceeded")
        return "Sorry, the AI service is currently at capacity. Please try again later."

    except openai.APIConnectionError:
        logger.error("Failed to connect to OpenAI API")
        return "Sorry, there was a connection issue with the AI service. Please try again later."

    except openai.APITimeoutError:
        logger.error("OpenAI API request timed out")
        return "Sorry, the AI service is taking too long to respond. Please try again later."

    except Exception as e:
        logger.error(f"Error generating response: {str(e)}")
        # Return a fallback response if OpenAI fails
        fallback_response = (
            f"An error occurred while processing your request. The query was: '{user_query}'. "
            f"We're unable to generate a response at this time. Please try again later."
        )
        return fallback_response