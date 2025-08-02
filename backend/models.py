from pydantic import BaseModel, Field
from typing import Annotated, Dict
from datetime import datetime

class MetaData(BaseModel):
    filename: Annotated[str, Field(default=None, title='filename', description="Given filename should be of string format")]
    
    size: Annotated[int, Field(default=0, title='size of the file', description="This contains the size of the file")]
    
    headers: Annotated[Dict[str, str], Field(default_factory=dict, title='Headers of the file', description="This has the headers of the file")]
    
    content_type: Annotated[str, Field(default=None, title="Content type", description="This has the content information about the file")]
    
    upload_time: Annotated[datetime, Field(default_factory= datetime.now, title='Upload time', description="Timestamp when the file was uploaded")]
