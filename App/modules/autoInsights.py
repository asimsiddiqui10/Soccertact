import google.generativeai as genai


class AutoInsights:
    def __init__(self):
        self.api_key = "AIzaSyAwPJOkqRhWbGYfpJBvji3_4XMMg9XdVyQ"
        self.model_name = "gemini-1.5-flash"
        self.model = None
        self.configure()

    def configure(self):
        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel(self.model_name)

    def format_prompt(self, prompt):
        """
        Format the prompt for the Generative AI model.

        Args:
            prompt (list): List of dictionaries with 'role' and 'content' keys.

        Returns:
            list: List of dictionaries formatted with 'parts'.
        """
        formatted_prompt = []
        for message in prompt:
            formatted_prompt.append({
                "role": message["role"],
                "parts": [message["content"]]  # Wrap the content in a 'parts' list
            })
        return formatted_prompt

    def generate_content(self, prompt):
        """
        Generate content from the AI model based on the provided prompt.

        Args:
            prompt (list): List of dictionaries with 'role' and 'content' keys.

        Returns:
            str: Generated text response.
        """
        try:
            # Format the prompt for the API
            formatted_prompt = self.format_prompt(prompt)
            response = self.model.generate_content(contents=formatted_prompt)
            return response.text
        except Exception as e:
            return f"An error occurred: {e}"

