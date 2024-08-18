import typing as t
from pydantic import BaseModel, Field, ConfigDict

from ..summarization.bases import SummarizerConfig

from ..rag.bases import RagAgentConfig


class DocumentSourceComponentConfig(BaseModel):
    type: t.Literal["storage", "filesystem", "pycode_filesystem"]
    config: t.Union[str, dict] = Field(default_factory=dict)


class LLMComponentConfig(BaseModel):
    type: str
    config: dict
    model_config = ConfigDict(extra= "allow")


class EncoderComponentConfig(BaseModel):
    type: t.Literal["hugging_face"]
    config: dict = Field(default_factory=dict)


class AnalysisConfig(BaseModel):
    analyzer_type: t.Literal["python"]
    storage: str


class SummarizerComponentConfig(BaseModel):
    
    class SummarizerComponentRefSubconfig(BaseModel):
        llm: str
        model_config = ConfigDict(extra= "allow")

    type: t.Literal["python_code"]
    config: t.Union[SummarizerComponentRefSubconfig, SummarizerConfig]


class StorageComponentConfig(BaseModel):
    data_type: t.Literal["metadata", "vector", "summary", "omni"]
    type: t.Literal["elasticsearch", "pydict"]
    config: dict = Field(default_factory=dict)


class RagAgentComponentConfig(BaseModel):
    type: str
    config: RagAgentConfig
