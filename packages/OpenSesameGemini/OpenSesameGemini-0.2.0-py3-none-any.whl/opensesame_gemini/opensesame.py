import google.generativeai as genai
import requests
import json
from typing import Dict, Any

class OpenSesame:
    def __init__(self, config: Dict[str, Any]):
        self._config = config
        genai.configure(api_key=config['api_key'])
        print("OpenSesame constructor called")

    def GenerativeModel(self, model_name: str):
        return self.GenerativeModelImpl(f"models/{model_name}", self._config)

    class GenerativeModelImpl(genai.GenerativeModel):
        def __init__(self, model_name: str, config: Dict[str, Any]):
            super().__init__(model_name)
            self._model_name = model_name
            self._config = config

        def generate_content(self, prompt: str, **kwargs):
            print("generate_content called")
            self._log_generation_query(prompt, **kwargs)

            result = super().generate_content(prompt, **kwargs)
            
            if result.text:
                self._log_generation_answer(result)
                answer = result.text

                print('Prompt:', prompt)
                print('Answer:', answer)

                try:
                    print('Sending request to:', 'https://app.opensesame.dev/api/newEvaluate')
                    request_body = {
                        'openSesameKey': self._config['open_sesame_key'],
                        'prompt': prompt,
                        'answer': answer,
                        'projectName': self._config['project_name'],
                        'groundTruth': self._config.get('ground_truth', ''),
                        'context': self._config.get('context', '')
                    }
                    print('Request body:', json.dumps(request_body))

                    response = requests.post(
                        'https://app.opensesame.dev/api/newEvaluate',
                        headers={
                            'Content-Type': 'application/json',
                            'Authorization': self._config['open_sesame_key']
                        },
                        json=request_body
                    )

                    response.raise_for_status()
                    data = response.json()
                    print('Evaluation:', data)
                except requests.RequestException as error:
                    print('Error in API call:', error)
                    if error.response:
                        print('Error response:', error.response.text)

            return result

        def _log_generation_query(self, prompt: str, **kwargs):
            print('Gemini Query:')
            print('Model:', self._model_name)
            print('Prompt:', prompt)

            if 'temperature' in kwargs:
                print('Temperature:', kwargs['temperature'])
            if 'max_output_tokens' in kwargs:
                print('Max Output Tokens:', kwargs['max_output_tokens'])
            print('---')

        def _log_generation_answer(self, result):
            print('Gemini Answer:')
            print(f"Content: {result.text}")
            print('---')