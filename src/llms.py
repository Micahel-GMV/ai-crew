import os
from langchain_openai import ChatOpenAI

OPENAI_API_BASE_LOCAL='http://127.0.0.1:11434/v1'
OPENAI_API_KEY_LOCAL = 'sk-aac078a86af0403b92eae32499f6a6ea'

OPENAI_API_KEY_WEB = "sk-ai-mase-service-account-5538Pa2M143W1WVLtwC0T3BlbkFJFlKxYT9wEUSVGGn7Xizx"
OPENAI_API_BASE_WEB = 'https://api.openai.com/v1'

openai_35_turbo_web = ChatOpenAI(
    model = "gpt-3.5-turbo",
    base_url = OPENAI_API_BASE_WEB,
    openai_api_key = OPENAI_API_KEY_WEB,
    api_key = OPENAI_API_KEY_WEB
)
# for text scraper - can`t recognise the task url, but tries something. Generates Shakespeare-like dialogues

llama3 = ChatOpenAI(
    model = "llama3",
    base_url = OPENAI_API_BASE_LOCAL,
    openai_api_key = OPENAI_API_KEY_LOCAL,
    api_key = OPENAI_API_KEY_LOCAL
)
# for text scraper - can`t recognise the task url, but tries something. Generates Shakespeare-like dialogues

mistral = ChatOpenAI(
    model = "mistral",
    base_url = OPENAI_API_BASE_LOCAL,
    openai_api_key = OPENAI_API_KEY_LOCAL,
    api_key = OPENAI_API_KEY_LOCAL
)
# for text scraper -

mistral_openorca = ChatOpenAI(
    model = "mistral-openorca",
    base_url = OPENAI_API_BASE_LOCAL,
    openai_api_key = OPENAI_API_KEY_LOCAL,
    api_key = OPENAI_API_KEY_LOCAL
)
# for text scraper -

nomic_embed_text = ChatOpenAI(
    model = "nomic-embed-text",
    base_url = OPENAI_API_BASE_LOCAL,
    openai_api_key = OPENAI_API_KEY_LOCAL,
    api_key = OPENAI_API_KEY_LOCAL
)
# for text scraper - doesn`t support chat.

wizardlm2 = ChatOpenAI(
    model = "wizardlm2",
    base_url = OPENAI_API_BASE_LOCAL,
    openai_api_key = OPENAI_API_KEY_LOCAL,
    api_key = OPENAI_API_KEY_LOCAL
)
# for text scraper -

dbrx = ChatOpenAI(
    model = "dbrx",
    base_url = OPENAI_API_BASE_LOCAL,
    openai_api_key = OPENAI_API_KEY_LOCAL,
    api_key = OPENAI_API_KEY_LOCAL
)
# for text scraper -

mixtral = ChatOpenAI(
    model = "mixtral",
    base_url = OPENAI_API_BASE_LOCAL,
    openai_api_key = OPENAI_API_KEY_LOCAL,
    api_key = OPENAI_API_KEY_LOCAL
)
# for text scraper - perfect result. Removes even technical text, formulates everything clearly and exactly

command_r_plus = ChatOpenAI(
    model = "command-r-plus",
    base_url = OPENAI_API_BASE_LOCAL,
    openai_api_key = OPENAI_API_KEY_LOCAL,
    api_key = OPENAI_API_KEY_LOCAL
)

command_r = ChatOpenAI(
    model = "command-r",
    base_url = OPENAI_API_BASE_LOCAL,
    openai_api_key = OPENAI_API_KEY_LOCAL,
    api_key = OPENAI_API_KEY_LOCAL
)
# for text scraper - perfect result. Removes even technical text, formulates everything clearly and exactly

gemma = ChatOpenAI(
    model = "gemma",
    base_url = OPENAI_API_BASE_LOCAL,
    openai_api_key = OPENAI_API_KEY_LOCAL,
    api_key = OPENAI_API_KEY_LOCAL
)
# for t

codegemma = ChatOpenAI(
    model = "codegemma",
    base_url = OPENAI_API_BASE_LOCAL,
    openai_api_key = OPENAI_API_KEY_WEB,
    api_key = OPENAI_API_KEY_LOCAL
)
# for t