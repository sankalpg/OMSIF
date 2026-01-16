from enum import Enum
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field

# --- Enums ---
class JobStatus(str, Enum):
    QUEUED = "queued"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"

class AudioFormat(str, Enum):
    MP3 = "mp3"
    WAV = "wav"
    M4A = "m4a"
    AAC = "aac"

# --- Template Models ---
class Template(BaseModel):
    id: str
    name: str
    description: Optional[str] = None
    capabilities: List[str] = []
    input_schema: Optional[Dict[str, Any]] = None

class CapabilitiesResponse(BaseModel):
    version: str = "1.0"
    provider: str
    features: List[str]
    templates: List[Template]

# --- Context Models ---
class PatientContext(BaseModel):
    id: Optional[str] = None
    name: Optional[str] = None
    dob: Optional[str] = None
    gender: Optional[str] = None

class EncounterContext(BaseModel):
    id: Optional[str] = None
    date: Optional[str] = None
    type: Optional[str] = None
    facility: Optional[str] = None

class ProviderContext(BaseModel):
    id: Optional[str] = None
    name: Optional[str] = None

class ContextPayload(BaseModel):
    patient: Optional[PatientContext] = None
    encounter: Optional[EncounterContext] = None
    provider: Optional[ProviderContext] = None

# --- Request Models ---
class AudioConfig(BaseModel):
    format: Optional[AudioFormat] = None
    sample_rate: Optional[int] = None
    channel_count: Optional[int] = None
    language_code: str = "en-US"

class RequestConfig(BaseModel):
    webhook_url: Optional[str] = None
    return_fhir: bool = False
    return_transcription: bool = True

class ScribeRequest(BaseModel):
    template_id: str
    audio_config: Optional[AudioConfig] = None
    context: Optional[ContextPayload] = None
    config: Optional[RequestConfig] = None

# --- Response Models ---
class ScribeOutput(BaseModel):
    transcription: Optional[str] = None
    structured_data: Optional[Dict[str, Any]] = None
    fhir_bundles: Optional[List[Dict[str, Any]]] = None

class JobResult(BaseModel):
    job_id: str
    status: JobStatus
    created_at: str
    completed_at: Optional[str] = None
    output: Optional[ScribeOutput] = None
    error: Optional[str] = None

class AsyncJobAccepted(BaseModel):
    job_id: str
    status: JobStatus
    eta_seconds: Optional[int] = None

class SessionCreated(BaseModel):
    session_id: str

class SessionCommitResponse(BaseModel):
    job_id: str
