import os
from typing import Optional, Type, Any
from pydantic.v1 import BaseModel, Field
from crewai_tools import BaseTool

class FixedFileWriteToolSchema(BaseModel):
    # Empty parent schema, potentially for future extensions or common fields.
    pass

class FileWriteToolSchema(FixedFileWriteToolSchema):
    file_path: str = Field(..., description="""The complete path from the project root to the file where data 
                                                    will be stored. This should include the file name and extension.""")
    content: str = Field(..., description="The content to be written to the specified file.")

class FileWriteTool(BaseTool):
    name: str = "Content File Writer tool"
    description: str = "A tool that writes specified content to a file located at a given path."
    args_schema: Type[BaseModel] = FileWriteToolSchema
    file_path: Optional[str] = None
    content: Optional[str] = None

    def __init__(self, file_path: Optional[str] = None, content: Optional[str] = None, **kwargs):
        super().__init__(**kwargs)
        self.file_path = file_path
        self.content = content
        if file_path is not None:
            self.file_path = file_path

    def _run(self, **kwargs: Any) -> Any:
        # Retrieve file path and content from kwargs or use instance attributes if not provided in kwargs.
        file_path = kwargs.get('file_path', self.file_path)
        content = kwargs.get('content', self.content)

        if os.path.exists(file_path):
            os.remove(file_path)

        # Write the content to the specified file path.
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(content)
        return f"Content successfully written to {file_path}"

