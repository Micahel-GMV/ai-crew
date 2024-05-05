import requests
import json
from bs4 import BeautifulSoup
from typing import Optional, Type, Any
from pydantic.v1 import BaseModel, Field
from crewai_tools import BaseTool

class FixedApiRequestToolSchema(BaseModel):
    pass

class ApiRequestToolSchema(FixedApiRequestToolSchema):
    endpoint_url: str = Field(..., description="Mandatory endpoint url to make API calls")
    http_verb: str = Field(..., description="Mandatory http verb to make API call.")
    data: Optional[dict] = Field(None, description="Data to be sent in POST/PUT requests.")

class ApiRequestTool(BaseTool):
    name: str = "Make API calls"
    description: str = "A tool that can be used to make API calls."
    args_schema: Type[BaseModel] = ApiRequestToolSchema
    endpoint_url: Optional[str] = None
    http_verb: Optional[str] = None

    def __init__(self, endpoint_url: Optional[str] = None, http_verb: Optional[str] = None, **kwargs):
        super().__init__(**kwargs)
        if endpoint_url is not None:
            self.endpoint_url = endpoint_url
        self.http_verb = http_verb if http_verb is not None else "GET"

    def _run(self, **kwargs: Any) -> Any:
        endpoint_url = kwargs.get('endpoint_url', self.endpoint_url)
        http_verb = kwargs.get('http_verb', self.http_verb)
        data = kwargs.get('data', {})

        # Choose the right requests function based on the http_verb
        method = getattr(requests, http_verb.lower(), requests.get)
        response = method(
            endpoint_url,
            timeout=15,
            data=json.dumps(data) if data else None
        )

        # Check if the content is HTML and parse it
        if 'html' in response.headers.get('Content-Type', ''):
            parsed = BeautifulSoup(response.content, "html.parser")
            body = parsed.get_text()
        else:
            body = response.text  # Use raw text if not HTML

        response_data = {
            "code": response.status_code,
            "body": body
        }

        return json.dumps(response_data, ensure_ascii=False)
