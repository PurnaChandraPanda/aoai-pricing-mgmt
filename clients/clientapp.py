from azure.identity import DefaultAzureCredential, get_bearer_token_provider
from openai import AzureOpenAI
import os, time
from datetime import datetime, timezone
from _logger import CSVLogger
from dotenv import load_dotenv
load_dotenv()

# Initialize the csv logger
_logger = CSVLogger()

## RBAC: Add current user with role: Cognitive Services OpenAI User
token_provider = get_bearer_token_provider(
    DefaultAzureCredential(), "https://cognitiveservices.azure.com/.default"
)

## Initialize the Azure OpenAI client
client = AzureOpenAI(
    api_version=os.getenv("AZURE_OPENAI_API_VERSION"),
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
    azure_ad_token_provider=token_provider
)

def _single_completion(model_deployment): 
    ## Create a completion for a single chat message
    response = client.chat.completions.create(
        model=model_deployment, 
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "Does Azure OpenAI support customer managed keys?"},
            {"role": "assistant", "content": "Yes, customer managed keys are supported by Azure OpenAI."},
            {"role": "user", "content": "Do other Azure AI services support this too?"}
        ],
        temperature = 0.7,
        top_p = 0.95,
        max_completion_tokens = 500
    )

    # Log the response
    _logger.log(
        datetime.fromtimestamp(response.created, tz=timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ'),
        model_deployment,
        response.model,
        response.object,
        response.usage.prompt_tokens,
        response.usage.completion_tokens,
        response.usage.total_tokens
    )

    print(response.choices[0].message.content)

def loop_completion():
    _model_deployment = os.getenv("AZURE_OPENAI_MODEL")
    if _model_deployment is not None:
        _single_completion(model_deployment=_model_deployment)
    else:
        ## Run a loop for multiple model deployments
        for i in range(0, 50):
            ## Expect AZURE_OPENAI_MODELS env var is set instead with list of deployments
            _model_deployments = os.getenv("AZURE_OPENAI_MODELS").split(',')
            for model in _model_deployments:
                _model_deployment = model
                # print(_model_deployment)
                _single_completion(model_deployment=_model_deployment)

            ## Sleep for 10 seconds
            time.sleep(10)

def embedding_operation():
    embedding_model = "text-embedding-ada-002"

    for i in range(0, 100):
        response = client.embeddings.create(
            model=embedding_model,
            input=["Azure OpenAI is a powerful tool for developers."]
        )
        # print(datetime.now().strftime('%Y-%m-%dT%H:%M:%SZ'), response.model, response.usage.prompt_tokens, response.usage.total_tokens)
        print(response.model, response.usage.total_tokens)

        # Log the response
        _logger.log(
            datetime.now().strftime('%Y-%m-%dT%H:%M:%SZ'),
            embedding_model,
            response.model,
            response.object,
            response.usage.prompt_tokens,
            None,
            response.usage.total_tokens
        )

if __name__ == '__main__':
    loop_completion()
    embedding_operation()
