from anthropic import AsyncAnthropic

class SentenceGenerator:
    """
    A class that generates unique, AI-powered sentences using Claude 3 Sonnet.
    
    This class handles the interaction with Anthropic's API to generate dark, humorous,
    and thought-provoking sentences while ensuring uniqueness through database validation.
    """

    def __init__(self, api_key: str, database):
        """
        Initialize the sentence generator with API credentials and database connection.

        Args:
            api_key (str): Anthropic API key for authentication
            database: Database instance for checking sentence uniqueness
        """
        self.client = AsyncAnthropic(api_key=api_key)
        self.database = database

    async def generate_random_sentence(self):
        """
        Generate a random sentence using Claude AI about a randomly selected topic.
        
        The topic selection is deterministic based on the hash of existing sentences,
        ensuring varied content distribution across different themes.

        Returns:
            str: A generated sentence under 280 characters

        Note:
            The prompt is designed to generate dark, humorous content while
            avoiding similarity with the 5 most recent sentences.
        """
        topics = ["technology", "society", "nature", "human behavior", "modern life", 
                 "relationships", "work", "future", "past", "philosophy", "science"]
        
        prompt = f"""Generate a single random sentence about {topics[hash(str(self.database.get_all_sentences())) % len(topics)]}. 
        Make it dark, funny, and unexpected. Keep it under 240 characters. 
        Make it different from these existing sentences: {self.database.get_all_sentences()[-5:]}
        Return only the sentence, nothing else."""

        response = await self.client.messages.create(
            model="claude-3-sonnet-20240229",
            max_tokens=1000,
            temperature=0.9,  # Higher temperature for more creative outputs
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        
        return response.content[0].text

    async def generate_unique_sentence(self, max_attempts: int = 5):
        """
        Generate a sentence that doesn't exist in the database.

        Args:
            max_attempts (int): Maximum number of generation attempts before raising an error

        Returns:
            str: A unique generated sentence

        Raises:
            Exception: If unable to generate a unique sentence within max_attempts
        """
        for _ in range(max_attempts):
            sentence = await self.generate_random_sentence()
            if not self.database.sentence_exists(sentence):
                return sentence
        
        raise Exception("Could not generate a unique sentence after multiple attempts")
