import tiktoken
from typing import List

# Initialize the tokenizer for OpenAI's text-embedding-3-small model
# Using cl100k_base which is used by text-embedding-3-small
tokenizer = tiktoken.get_encoding("cl100k_base")

def count_tokens(text: str) -> int:
    """
    Count the number of tokens in a given text
    """
    return len(tokenizer.encode(text))

def chunk_text(text: str, max_tokens: int = 1024, min_tokens: int = 512) -> List[str]:
    """
    Split text into chunks based on token count with overlap to maintain context
    """
    # First, split text into sentences or paragraphs as potential chunk boundaries
    sentences = text.split('\n\n')  # Split by paragraphs first
    
    chunks = []
    current_chunk = ""
    
    for sentence in sentences:
        # Check if adding this sentence would exceed the max token limit
        test_chunk = current_chunk + " " + sentence if current_chunk else sentence
        token_count = count_tokens(test_chunk)
        
        if token_count <= max_tokens:
            # Add to current chunk if it doesn't exceed the limit
            current_chunk = test_chunk
        else:
            # If current chunk is substantial (more than min_tokens), save it
            if count_tokens(current_chunk) >= min_tokens:
                chunks.append(current_chunk.strip())
                current_chunk = sentence  # Start new chunk with this sentence
            else:
                # If current chunk is too small, try splitting the current sentence
                if count_tokens(sentence) > max_tokens:
                    # Split the long sentence into smaller parts
                    sub_chunks = chunk_long_text(sentence, max_tokens, min_tokens)
                    if chunks and sub_chunks:
                        # Add the first sub-chunk to current chunk if it's not too big
                        first_sub = sub_chunks.pop(0)
                        combined = current_chunk + " " + first_sub if current_chunk else first_sub
                        if count_tokens(combined) <= max_tokens:
                            current_chunk = combined
                        else:
                            chunks.append(current_chunk.strip())
                            current_chunk = first_sub
                    chunks.extend(sub_chunks)
                else:
                    # Start a new chunk with this sentence
                    chunks.append(current_chunk.strip())
                    current_chunk = sentence
    
    # Add the last chunk if it has content
    if current_chunk.strip():
        chunks.append(current_chunk.strip())
    
    return chunks

def chunk_long_text(text: str, max_tokens: int = 1024, min_tokens: int = 512) -> List[str]:
    """
    Helper function to chunk text that is longer than max_tokens
    """
    words = text.split()
    chunks = []
    current_chunk = []
    
    for word in words:
        current_chunk.append(word)
        chunk_text = " ".join(current_chunk)
        if count_tokens(chunk_text) > max_tokens:
            # Remove the last word that caused overflow
            current_chunk.pop()
            if current_chunk:  # If there are words to save
                chunks.append(" ".join(current_chunk))
                # Start new chunk with the word that caused overflow
                current_chunk = [word]
    
    # Add any remaining words as a final chunk
    if current_chunk:
        chunks.append(" ".join(current_chunk))
    
    return chunks