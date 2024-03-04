from pydantic import BaseModel, Field
from typing import Optional, List


class ConversationRequest(BaseModel):
    requestType: str = Field(
        ...,
        description="query",
    )
    persona: str = Field(
        ...,
        description="Specifies the persona or character assumed by the AI during the conversation.",
    )
    userId: str = Field(
        ...,
        alias="uid",
        description="A unique identifier assigned to each user interacting with the system.",
    )
    message: str = Field(
        ...,
        description="Contains the text input from the user that needs to be processed or analyzed by the LLM.",
    )
    document: str = Field(
        None,
        description="Intended for future functionality, links the interaction to a specific document or content source.",
    )
    context: Optional[str] = Field(
        None,
        description="Provides additional background or situational information to the LLM, limited to 100 words.",
    )
    maxTokens: Optional[int] = Field(
        None,
        description="Specifies the maximum length of the generated response in terms of tokens.",
    )
    temperature: Optional[float] = Field(
        None,
        description="Adjusts the creativity and variability of the LLM's responses.",
    )
    sessionId: str = Field(
        ..., description="Acts as a unique identifier for each conversation thread."
    )
    language: str = Field(
        ..., description="Indicates the language in which the interaction is conducted."
    )


class ErrorResponse(BaseModel):
    code: str = Field(
        ..., description="A unique identifier for the type of error that occurred."
    )
    message: str = Field(
        ..., description="A detailed message explaining what went wrong."
    )

    def pretty_print(self):
        print(f"Error Code: {self.code}\nError Message: {self.message}")


class ConversationResponse(BaseModel):
    requestType: str = Field(..., description="The type of request, such as 'query'.")
    content: str = Field(
        ..., description="The content generated in response to the request."
    )
    citations: List[str] = Field(
        default=[], description="A list of citations in a structured string format."
    )
    inputTokenCount: int = Field(
        ..., description="The number of tokens in the input query."
    )
    outputTokenCount: int = Field(
        ..., description="The number of tokens in the generated response."
    )
    error: Optional[ErrorResponse] = Field(
        None, description="Details about any error that occurred during processing."
    )


class FileOperationReq(BaseModel):
    requestType: str = Field(..., description="The type of file operation request.")
    dataOperands: str = Field(..., description="Operational data for the file request.")
    fileNames: Optional[List[str]] = Field(
        None, description="A list of file names involved in the operation, optional."
    )

    def pretty_print(self):
        print(f"Request Type: {self.requestType}\nData Operands: {self.dataOperands}")
        if self.fileNames:
            print(f"File Names: {', '.join(self.fileNames)}")
        else:
            print("File Names: None")


class FileOperationResp(BaseModel):
    responseType: str
    responseMsg: str
    error: Optional[ErrorResponse] = Field(
        None, description="Details about any error that occurred during processing."
    )

    def pretty_print(self):
        print(
            f"Response Type: {self.responseType}\nResponse Message: {self.responseMsg}"
        )
        if self.error:
            print("Error:")
            self.error.pretty_print()


class REQLocalWebFile(BaseModel):
    request: str
    filedrawer: str
    filename: str

    def pretty_print(self):
        print(
            f"Request: {self.request}\nFile Drawer: {self.filedrawer}\nFilename: {self.filename}"
        )


class RESPLocalWebFile(BaseModel):
    request: str
    status: str
    error: Optional[ErrorResponse] = (
        None  # Use Optional for compatibility with Python versions < 3.10
    )

    def pretty_print(self):
        print(f"Request: {self.request}\nStatus: {self.status}")
        if self.error:
            print("Error:")
            self.error.pretty_print()

class ErrorResponse(BaseModel):
    code: str = Field(
        ..., description="A unique identifier for the type of error that occurred."
    )
    message: str = Field(
        ..., description="A detailed message explaining what went wrong."
    )


class ResponseFileUpload(BaseModel):
    message: str
    error: ErrorResponse | None = None
    listfiles: List[str] = Field(
        default_factory=list, description="A list of filenames that were processed."
    )

