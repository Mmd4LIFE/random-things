from anthropic import AsyncAnthropic

class SentenceGenerator:
    def __init__(self, api_key, database):
        self.client = AsyncAnthropic(api_key=api_key)
        self.database = database

    async def generate_random_sentence(self):
        topics = ["technology", "society", "nature", "human behavior", "modern life", 
                 "relationships", "work", "future", "past", "philosophy"]
        
        prompt = f"""Generate a single random sentence about {topics[hash(str(self.database.get_all_sentences())) % len(topics)]}. 
        Make it dark, funny, and unexpected. Keep it under 280 characters. 
        Make it different from these existing sentences: {self.database.get_all_sentences()[-5:]}
        Return only the sentence, nothing else."""

        response = await self.client.messages.create(
            model="claude-3-sonnet-20240229",
            max_tokens=1000,
            temperature=0.9,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        
        return response.content[0].text

    async def generate_unique_sentence(self, max_attempts=5):
        for _ in range(max_attempts):
            sentence = await self.generate_random_sentence()
            if not self.database.sentence_exists(sentence):
                return sentence
        
        raise Exception("Could not generate a unique sentence after multiple attempts")
