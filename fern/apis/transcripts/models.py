from enum import Enum
from typing import Dict, List, Optional, Union, Annotated

from pydantic import BaseModel, ConfigDict, Field, model_validator, Discriminator, Tag


class TranscriptStatus(str, Enum):
    """The status of your transcript. Possible values are queued, processing, completed, or error."""

    queued = "queued"
    processing = "processing"
    completed = "completed"
    error = "error"


class AudioIntelligenceModelStatus(str, Enum):
    """Either success, or unavailable in the rare case that the model failed."""

    success = "success"
    unavailable = "unavailable"


class Sentiment(str, Enum):
    """Sentiment classification."""

    POSITIVE = "POSITIVE"
    NEUTRAL = "NEUTRAL"
    NEGATIVE = "NEGATIVE"


class EntityType(str, Enum):
    """The type of entity for the detected entity."""

    account_number = "account_number"
    banking_information = "banking_information"
    blood_type = "blood_type"
    credit_card_cvv = "credit_card_cvv"
    credit_card_expiration = "credit_card_expiration"
    credit_card_number = "credit_card_number"
    date = "date"
    date_interval = "date_interval"
    date_of_birth = "date_of_birth"
    drivers_license = "drivers_license"
    drug = "drug"
    duration = "duration"
    email_address = "email_address"
    event = "event"
    filename = "filename"
    gender_sexuality = "gender_sexuality"
    healthcare_number = "healthcare_number"
    injury = "injury"
    ip_address = "ip_address"
    language = "language"
    location = "location"
    marital_status = "marital_status"
    medical_condition = "medical_condition"
    medical_process = "medical_process"
    money_amount = "money_amount"
    nationality = "nationality"
    number_sequence = "number_sequence"
    occupation = "occupation"
    organization = "organization"
    passport_number = "passport_number"
    password = "password"
    person_age = "person_age"
    person_name = "person_name"
    phone_number = "phone_number"
    physical_attribute = "physical_attribute"
    political_affiliation = "political_affiliation"
    religion = "religion"
    statistics = "statistics"
    time = "time"
    url = "url"
    us_social_security_number = "us_social_security_number"
    username = "username"
    vehicle_id = "vehicle_id"
    zodiac_sign = "zodiac_sign"


class RedactPiiAudioQuality(str, Enum):
    """Controls the filetype of the audio created by redact_pii_audio."""

    mp3 = "mp3"
    wav = "wav"


class SubstitutionPolicy(str, Enum):
    """The replacement logic for detected PII."""

    entity_name = "entity_name"
    hash = "hash"


class SpeechModel(str, Enum):
    """The speech model to use for the transcription."""

    best = "best"
    slam_1 = "slam-1"
    universal = "universal"


class SubtitleFormat(str, Enum):
    """Format of the subtitles."""

    srt = "srt"
    vtt = "vtt"


class SummaryModel(str, Enum):
    """The model to summarize the transcript."""

    informative = "informative"
    conversational = "conversational"
    catchy = "catchy"


class SummaryType(str, Enum):
    """The type of summary."""

    bullets = "bullets"
    bullets_verbose = "bullets_verbose"
    gist = "gist"
    headline = "headline"
    paragraph = "paragraph"


class ErrorResponse(BaseModel):
    """Standard error response."""

    model_config = ConfigDict(extra="forbid")

    error: str = Field(..., description="Error message describing what went wrong")


class UploadedFile(BaseModel):
    """Response for uploaded file."""

    model_config = ConfigDict(extra="forbid")

    upload_url: str = Field(
        ..., 
        description="A URL that points to your audio file, accessible only by AssemblyAI's servers",
        format="url"
    )




class TranscriptLanguageCode(str, Enum):
    """The language of your audio file. Possible values are found in [Supported Languages](https://www.assemblyai.com/docs/concepts/supported-languages). The default value is 'en_us'."""

    en = "en"
    en_au = "en_au"
    en_uk = "en_uk"
    en_us = "en_us"
    es = "es"
    fr = "fr"
    de = "de"
    it = "it"
    pt = "pt"
    nl = "nl"
    af = "af"
    sq = "sq"
    am = "am"
    ar = "ar"
    hy = "hy"
    as_ = "as"
    az = "az"
    ba = "ba"
    eu = "eu"
    be = "be"
    bn = "bn"
    bs = "bs"
    br = "br"
    bg = "bg"
    my = "my"
    ca = "ca"
    zh = "zh"
    hr = "hr"
    cs = "cs"
    da = "da"
    et = "et"
    fo = "fo"
    fi = "fi"
    gl = "gl"
    ka = "ka"
    el = "el"
    gu = "gu"
    ht = "ht"
    ha = "ha"
    haw = "haw"
    he = "he"
    hi = "hi"
    hu = "hu"
    is_ = "is"
    id_ = "id"
    ja = "ja"
    jw = "jw"
    kn = "kn"
    kk = "kk"
    km = "km"
    ko = "ko"
    lo = "lo"
    la = "la"
    lv = "lv"
    ln = "ln"
    lt = "lt"
    lb = "lb"
    mk = "mk"
    mg = "mg"
    ms = "ms"
    ml = "ml"
    mt = "mt"
    mi = "mi"
    mr = "mr"
    mn = "mn"
    ne = "ne"
    no = "no"
    nn = "nn"
    oc = "oc"
    pa = "pa"
    ps = "ps"
    fa = "fa"
    pl = "pl"
    ro = "ro"
    ru = "ru"
    sa = "sa"
    sr = "sr"
    sn = "sn"
    sd = "sd"
    si = "si"
    sk = "sk"
    sl = "sl"
    so = "so"
    su = "su"
    sw = "sw"
    sv = "sv"
    tl = "tl"
    tg = "tg"
    ta = "ta"
    tt = "tt"
    te = "te"
    th = "th"
    bo = "bo"
    tr = "tr"
    tk = "tk"
    uk = "uk"
    ur = "ur"
    uz = "uz"
    vi = "vi"
    cy = "cy"
    yi = "yi"
    yo = "yo"


class Timestamp(BaseModel):
    """Timestamp containing a start and end property in milliseconds."""

    model_config = ConfigDict(extra="forbid")

    start: int = Field(..., description="The start time in milliseconds")
    end: int = Field(..., description="The end time in milliseconds")


class TranscriptWord(BaseModel):
    """A word in the transcript with timing and confidence information."""

    model_config = ConfigDict(extra="forbid")

    confidence: float = Field(
        ...,
        description="The confidence score for the transcript of this word",
        ge=0,
        le=1,
    )
    start: int = Field(
        ..., description="The starting time, in milliseconds, for the word"
    )
    end: int = Field(..., description="The ending time, in milliseconds, for the word")
    text: str = Field(..., description="The text of the word")
    channel: Optional[str] = Field(
        None,
        description="The channel of the word. The left and right channels are channels 1 and 2",
    )
    speaker: Optional[str] = Field(
        None,
        description="The speaker of the word if Speaker Diarization is enabled, else null",
    )


class TranscriptUtterance(BaseModel):
    """An utterance in the transcript."""

    model_config = ConfigDict(extra="forbid")

    confidence: float = Field(
        ...,
        description="The confidence score for the transcript of this utterance",
        ge=0,
        le=1,
    )
    start: int = Field(
        ...,
        description="The starting time, in milliseconds, of the utterance in the audio file",
    )
    end: int = Field(
        ...,
        description="The ending time, in milliseconds, of the utterance in the audio file",
    )
    text: str = Field(..., description="The text for this utterance")
    words: List[TranscriptWord] = Field(..., description="The words in the utterance")
    channel: Optional[str] = Field(None, description="The channel of this utterance")
    speaker: str = Field(..., description="The speaker of this utterance")
    translated_texts: Optional[Dict[str, str]] = Field(None, description="Translated text keyed by language code")


class ContentSafetyLabel(BaseModel):
    """Content Moderation label."""

    label: str = Field(..., description="The label of the sensitive topic")
    confidence: float = Field(
        ...,
        description="The confidence score for the topic being discussed, from 0 to 1",
        ge=0,
        le=1,
    )
    severity: float = Field(
        ...,
        description="How severely the topic is discussed in the section, from 0 to 1",
        ge=0,
        le=1,
    )


class ContentSafetyLabelResult(BaseModel):
    """Content Moderation label result."""

    text: str = Field(
        ...,
        description="The transcript of the section flagged by the Content Moderation model",
    )
    labels: List[ContentSafetyLabel] = Field(
        ..., description="An array of safety labels"
    )
    sentences_idx_start: int = Field(
        ..., description="The sentence index at which the section begins"
    )
    sentences_idx_end: int = Field(
        ..., description="The sentence index at which the section ends"
    )
    timestamp: Timestamp = Field(
        ..., description="Timestamp information for the section"
    )


class SeverityScoreSummary(BaseModel):
    """Severity score summary."""

    low: float = Field(..., description="Low severity score", ge=0, le=1)
    medium: float = Field(..., description="Medium severity score", ge=0, le=1)
    high: float = Field(..., description="High severity score", ge=0, le=1)


class ContentSafetyLabelsResult(BaseModel):
    """Content Moderation labels result."""

    status: Optional[AudioIntelligenceModelStatus] = Field(
        None, description="The status of the Content Moderation model"
    )
    results: Optional[List[ContentSafetyLabelResult]] = Field(
        None, description="An array of results for the Content Moderation model"
    )
    summary: Optional[dict] = Field(
        None, description="A summary of the Content Moderation confidence results"
    )
    severity_score_summary: Optional[dict] = Field(
        None, description="A summary of the Content Moderation severity results"
    )


class TopicDetectionLabel(BaseModel):
    """Topic detection label."""

    relevance: float = Field(
        ..., description="How relevant the detected topic is", ge=0, le=1
    )
    label: str = Field(
        ..., description="The IAB taxonomical label for the detected topic"
    )


class TopicDetectionResult(BaseModel):
    """Topic detection result."""

    text: str = Field(
        ..., description="The text in the transcript in which a detected topic occurs"
    )
    labels: Optional[List[TopicDetectionLabel]] = Field(
        None, description="An array of detected topics in the text"
    )
    timestamp: Optional[Timestamp] = Field(None, description="Timestamp information")


class TopicDetectionModelResult(BaseModel):
    """The result of the Topic Detection model."""

    status: Optional[AudioIntelligenceModelStatus] = Field(
        None, description="The status of the Topic Detection model"
    )
    results: Optional[List[TopicDetectionResult]] = Field(
        None, description="An array of results for the Topic Detection model"
    )
    summary: Optional[dict] = Field(
        None, description="The overall relevance of topic to the entire audio file"
    )


class AutoHighlightResult(BaseModel):
    """Auto highlight result."""

    count: int = Field(
        ...,
        description="The total number of times the key phrase appears in the audio file",
    )
    rank: float = Field(
        ...,
        description="The total relevancy to the overall audio file of this key phrase",
        ge=0,
        le=1,
    )
    text: str = Field(..., description="The text itself of the key phrase")
    timestamps: List[Timestamp] = Field(
        ..., description="The timestamp of the key phrase"
    )


class AutoHighlightsResult(BaseModel):
    """Auto highlights result."""

    status: AudioIntelligenceModelStatus = Field(
        ..., description="The status of the Key Phrases model"
    )
    results: List[AutoHighlightResult] = Field(
        ..., description="A temporally-sequential array of Key Phrases"
    )


class Chapter(BaseModel):
    """Chapter of the audio file."""

    gist: str = Field(
        ...,
        description="An ultra-short summary (just a few words) of the content spoken in the chapter",
    )
    headline: str = Field(
        ...,
        description="A single sentence summary of the content spoken during the chapter",
    )
    summary: str = Field(
        ...,
        description="A one paragraph summary of the content spoken during the chapter",
    )
    start: int = Field(
        ..., description="The starting time, in milliseconds, for the chapter"
    )
    end: int = Field(
        ..., description="The starting time, in milliseconds, for the chapter"
    )


class Entity(BaseModel):
    """A detected entity."""

    entity_type: EntityType = Field(
        ..., description="The type of entity for the detected entity"
    )
    text: str = Field(..., description="The text for the detected entity")
    start: int = Field(
        ...,
        description="The starting time, in milliseconds, at which the detected entity appears",
    )
    end: int = Field(
        ..., description="The ending time, in milliseconds, for the detected entity"
    )


class SentimentAnalysisResult(BaseModel):
    """The result of the Sentiment Analysis model."""

    text: str = Field(..., description="The transcript of the sentence")
    start: int = Field(
        ..., description="The starting time, in milliseconds, of the sentence"
    )
    end: int = Field(
        ..., description="The ending time, in milliseconds, of the sentence"
    )
    sentiment: Sentiment = Field(
        ..., description="The detected sentiment for the sentence"
    )
    confidence: float = Field(
        ..., description="The confidence score for the detected sentiment", ge=0, le=1
    )
    channel: Optional[str] = Field(None, description="The channel of this utterance")
    speaker: Optional[str] = Field(
        None,
        description="The speaker of the sentence if Speaker Diarization is enabled",
    )


class TranscriptCustomSpelling(BaseModel):
    """Custom spelling configuration."""

    from_: List[str] = Field(
        ..., alias="from", description="Words or phrases to replace"
    )
    to: str = Field(..., description="Word to replace with")


class LanguageDetectionOptions(BaseModel):
    """Options for Automatic Language Detection."""

    expected_languages: Optional[List[TranscriptLanguageCode]] = Field(
        None, description="List of languages expected in the audio file"
    )
    fallback_language: str = Field(
        "auto",
        description="Fallback language if detected language is not in expected languages",
    )
    code_switching: bool = Field(
        False, description="Whether code switching should be detected"
    )
    code_switching_confidence_threshold: float = Field(
        0.3, description="Confidence threshold for code switching detection", ge=0, le=1
    )


class SpeakerOptions(BaseModel):
    """Options for speaker diarization."""

    min_speakers_expected: int = Field(
        1, description="The minimum number of speakers expected"
    )
    max_speakers_expected: int = Field(
        10, description="The maximum number of speakers expected"
    )


class RedactPiiAudioOptions(BaseModel):
    """Options for PII redacted audio files."""

    return_redacted_no_speech_audio: bool = Field(
        False, description="Return redacted audio URLs even for silent audio files"
    )


class SpeakerType(str, Enum):
    """The type of speaker identification."""
    
    name = "name"
    role = "role"


class SpeakerIdentificationRequest(BaseModel):
    """Speaker identification request configuration."""
    
    model_config = ConfigDict(extra="forbid")
    
    speaker_type: SpeakerType = Field(..., description="The type of speaker identification")
    known_values: Optional[List[str]] = Field(None, description="Known values for speakers (required when speaker_type is 'role')")


class SpeakerIdentificationResponse(BaseModel):
    """Speaker identification response."""
    
    model_config = ConfigDict(extra="forbid")
    mapping: Dict[str, str] = Field(..., description="Mapping of original text to speaker identification")
    status: str = Field(..., description="The status of speaker identification")


class TranslationRequest(BaseModel):
    """Translation request configuration."""
    
    model_config = ConfigDict(extra="forbid")
    
    target_languages: List[str] = Field(..., description="List of target language codes")
    formal: bool = Field(True, description="Whether to use formal language")
    match_original_utterance: bool = Field(False, description="Whether to match original utterance structure")


class TranslationResponse(BaseModel):
    """Translation response."""
    
    model_config = ConfigDict(extra="forbid")
    
    status: str = Field(..., description="The status of translation")


class CustomFormattingRequest(BaseModel):
    """Custom formatting request configuration."""
    
    model_config = ConfigDict(extra="forbid")
    
    date: Optional[str] = Field(None, description="Date format pattern (e.g., 'mm/dd/yyyy')")
    phone_number: Optional[str] = Field(None, description="Phone number format pattern (e.g., '(xxx)xxx-xxxx')")
    email: Optional[str] = Field(None, description="Email format pattern (e.g., 'username@domain.com')")
    formatted_utterances: bool = Field(True, description="Whether to format utterances")


class CustomFormattingResponse(BaseModel):
    """Custom formatting response."""
    
    model_config = ConfigDict(extra="forbid")
    
    mapping: Dict[str, str] = Field(..., description="Mapping of original text to formatted text")
    formatted_text: Optional[str] = Field(None, description="The formatted text")
    formatted_utterances: Optional[List[TranscriptUtterance]] = Field(None, description="Formatted utterances")
    status: str = Field(..., description="The status of custom formatting")


class SpeechUnderstandingRequest(BaseModel):
    """Speech understanding request configuration."""
    
    model_config = ConfigDict(extra="forbid")
    
    speaker_identification: Optional[SpeakerIdentificationRequest] = Field(None, description="Speaker identification request")
    translation: Optional[TranslationRequest] = Field(None, description="Translation request")
    custom_formatting: Optional[CustomFormattingRequest] = Field(None, description="Custom formatting request")


class SpeechUnderstandingResponse(BaseModel):
    """Speech understanding response configuration."""
    
    model_config = ConfigDict(extra="forbid")
    
    speaker_identification: Optional[SpeakerIdentificationResponse] = Field(None, description="Speaker identification response")
    translation: Optional[TranslationResponse] = Field(None, description="Translation response")
    custom_formatting: Optional[CustomFormattingResponse] = Field(None, description="Custom formatting response")


class SpeechUnderstandingInput(BaseModel):
    """Speech Understanding input configuration for transcript creation."""

    model_config = ConfigDict(extra="forbid")

    request: SpeechUnderstandingRequest = Field(..., description="The speech understanding request configuration")


# For transcript responses - contains both request and response data
class SpeechUnderstanding(BaseModel):
    """Speech Understanding configuration with results."""

    model_config = ConfigDict(extra="forbid")

    request: SpeechUnderstandingRequest = Field(
        ..., description="The speech understanding request configuration"
    )
    response: Optional[SpeechUnderstandingResponse] = Field(
        None, description="The speech understanding response"
    )


class TranscriptSentence(BaseModel):
    """A sentence in the transcript with timing and word-level information."""

    model_config = ConfigDict(extra="forbid")

    text: str = Field(..., description="The text of the sentence")
    start: int = Field(
        ..., description="The starting time, in milliseconds, of the sentence"
    )
    end: int = Field(
        ..., description="The ending time, in milliseconds, of the sentence"
    )
    confidence: float = Field(
        ..., description="The confidence score for the sentence", ge=0, le=1
    )
    words: List[TranscriptWord] = Field(
        ..., description="An array of word objects that make up the sentence"
    )
    speaker: Optional[str] = Field(
        None,
        description="The speaker of the sentence if Speaker Diarization is enabled",
    )


class TranscriptSentencesResponse(BaseModel):
    """Response model for the sentences endpoint."""

    model_config = ConfigDict(extra="forbid")

    id: str = Field(..., description="The unique identifier of the transcript")
    sentences: List[TranscriptSentence] = Field(
        ..., description="An array of sentence objects"
    )
    confidence: Optional[float] = Field(
        None, description="Overall confidence score for the transcript", ge=0, le=1
    )
    audio_duration: Optional[float] = Field(
        None, description="The duration of the audio file, in seconds"
    )


class TranscriptParagraph(BaseModel):
    """A paragraph in the transcript with timing and word-level information."""

    model_config = ConfigDict(extra="forbid")

    text: str = Field(..., description="The text of the paragraph")
    start: int = Field(
        ..., description="The starting time, in milliseconds, of the paragraph"
    )
    end: int = Field(
        ..., description="The ending time, in milliseconds, of the paragraph"
    )
    confidence: float = Field(
        ..., description="The confidence score for the paragraph", ge=0, le=1
    )
    words: List[TranscriptWord] = Field(
        ..., description="An array of word objects that make up the paragraph"
    )


class TranscriptParagraphsResponse(BaseModel):
    """Response model for the paragraphs endpoint."""

    model_config = ConfigDict(extra="forbid")

    id: str = Field(..., description="The unique identifier of the transcript")
    paragraphs: List[TranscriptParagraph] = Field(
        ..., description="An array of paragraph objects"
    )
    confidence: Optional[float] = Field(
        None, description="Overall confidence score for the transcript", ge=0, le=1
    )
    audio_duration: Optional[float] = Field(
        None, description="The duration of the audio file, in seconds"
    )


class WordSearchMatch(BaseModel):
    """A word search match result."""

    model_config = ConfigDict(extra="forbid")

    text: str = Field(..., description="The matched word or phrase")
    count: int = Field(..., description="The number of times this word/phrase appears")
    timestamps: List[List[int]] = Field(
        ..., description="Array of `[start, end]` timestamp pairs in milliseconds"
    )
    indexes: List[int] = Field(
        ..., description="Array of word indexes where the match occurs"
    )


class WordSearchResponse(BaseModel):
    """Response model for word search endpoint."""

    model_config = ConfigDict(extra="forbid")

    id: str = Field(..., description="The unique identifier of the transcript")
    matches: List[WordSearchMatch] = Field(
        ..., description="An array of word search matches"
    )
    total_count: int = Field(
        ..., description="Total count of all matches across all words/phrases"
    )


class RedactedAudioResponse(BaseModel):
    """Response model for redacted audio endpoint."""

    model_config = ConfigDict(extra="forbid")

    redacted_audio_url: str = Field(
        ..., description="The URL of the redacted audio file",
    )
    status: str = Field(..., description="The status of the redacted audio file")


class TranscriptListItem(BaseModel):
    """A transcript item in the list response."""

    model_config = ConfigDict(extra="forbid")

    id: str = Field(..., description="The unique identifier of the transcript")
    status: TranscriptStatus = Field(..., description="The status of the transcript")
    audio_url: str = Field(..., description="The URL of the media that was transcribed")
    created: Optional[str] = Field(None, description="The creation timestamp")
    completed: Optional[str] = Field(None, description="The completion timestamp")
    language_code: Optional[str] = Field(
        None, description="The language of the audio file"
    )
    audio_duration: Optional[int] = Field(
        None, description="The duration of the media file, in seconds"
    )
    error: Optional[str] = Field(
        None, description="Error message if the transcript failed"
    )
    resource_url: str = Field(..., description="The URL to retrieve the transcript")
    region: Optional[str] = Field(
        None, description="The region where the transcript was processed"
    )


class PageDetails(BaseModel):
    """Pagination details for list responses."""

    model_config = ConfigDict(extra="forbid")

    limit: int = Field(..., description="The maximum number of transcripts returned")
    result_count: int = Field(
        ..., description="The actual number of transcripts returned"
    )
    current_url: str = Field(..., description="The URL of the current page")
    prev_url: Optional[str] = Field(None, description="The URL of the previous page")
    next_url: Optional[str] = Field(None, description="The URL of the next page")


class TranscriptListResponse(BaseModel):
    """Response model for transcript list endpoint."""

    model_config = ConfigDict(extra="forbid")

    page_details: PageDetails = Field(..., description="Pagination information")
    transcripts: List[TranscriptListItem] = Field(
        ..., description="An array of transcript objects"
    )


class TranscriptResponse(BaseModel):
    """A transcript object."""

    model_config = ConfigDict(extra="forbid")

    id: str = Field(..., description="The unique identifier of your transcript")
    audio_url: str = Field(..., description="The URL of the media that was transcribed")
    status: TranscriptStatus = Field(..., description="The status of your transcript")
    language_code: Optional[TranscriptLanguageCode] = Field(
        None, description="The language of your audio file"
    )
    language_codes: Optional[List[TranscriptLanguageCode]] = Field(
        None,
        description="The language codes of your audio file. Used for Code switching",
    )
    language_detection: Optional[bool] = Field(
        None, description="Whether Automatic language detection is enabled"
    )
    language_detection_options: Optional[LanguageDetectionOptions] = Field(
        None, description="Options for Automatic Language Detection"
    )
    language_confidence_threshold: Optional[float] = Field(
        None,
        description="The confidence threshold for the automatically detected language",
        ge=0,
        le=1,
    )
    language_confidence: Optional[float] = Field(
        None, description="The confidence score for the detected language", ge=0, le=1
    )
    speech_model: Optional[SpeechModel] = Field(
        None, description="The speech model used for the transcription", deprecated=True
    )
    speech_models: Optional[List[SpeechModel]] = Field(
        None, description="List multiple speech models in priority order"
    )
    speech_model_used: Optional[str] = Field(
        None,
        description="The speech model that was actually used for the transcription",
    )
    language_model: str = Field(
        ...,
        description="The language model that was used for the transcript",
        deprecated=True,
    )
    acoustic_model: str = Field(
        ...,
        description="The acoustic model that was used for the transcript",
        deprecated=True,
    )
    text: Optional[str] = Field(
        None, description="The textual transcript of your media file"
    )
    words: Optional[List[TranscriptWord]] = Field(
        None, description="An array of temporally-sequential word objects"
    )
    utterances: Optional[List[TranscriptUtterance]] = Field(
        None,
        description="When multichannel or speaker_labels is enabled, a list of turn-by-turn utterance objects",
    )
    confidence: Optional[float] = Field(
        None, description="The confidence score for the transcript", ge=0, le=1
    )
    audio_duration: Optional[int] = Field(
        None,
        description="The duration of this transcript object's media file, in seconds",
    )
    audio_channels: Optional[int] = Field(
        None, description="The number of audio channels in the audio file"
    )
    punctuate: Optional[bool] = Field(
        None, description="Whether Automatic Punctuation is enabled"
    )
    format_text: Optional[bool] = Field(
        None, description="Whether Text Formatting is enabled"
    )
    disfluencies: Optional[bool] = Field(
        None, description="Transcribe Filler Words, like 'umm'"
    )
    multichannel: Optional[bool] = Field(
        None, description="Whether Multichannel transcription was enabled"
    )
    dual_channel: Optional[bool] = Field(
        None,
        description="Whether Dual channel transcription was enabled",
        deprecated=True,
    )
    audio_start_from: Optional[int] = Field(
        None,
        description="The point in time, in milliseconds, in the file at which the transcription was started",
    )
    audio_end_at: Optional[int] = Field(
        None,
        description="The point in time, in milliseconds, in the file at which the transcription was terminated",
    )
    filter_profanity: Optional[bool] = Field(
        None, description="Whether Profanity Filtering is enabled"
    )
    redact_pii: bool = Field(..., description="Whether PII Redaction is enabled")
    redact_pii_audio: Optional[bool] = Field(
        None, description="Whether a redacted version of the audio file was generated"
    )
    redact_pii_audio_quality: Optional[RedactPiiAudioQuality] = Field(
        None, description="The audio quality of the PII-redacted audio file"
    )
    redact_pii_policies: Optional[List[EntityType]] = Field(
        None, description="The list of PII Redaction policies that were enabled"
    )
    redact_pii_sub: Optional[SubstitutionPolicy] = Field(
        None, description="The replacement logic for detected PII"
    )
    redact_pii_audio_options: Optional[RedactPiiAudioOptions] = Field(
        None, description="Options for PII redacted audio files"
    )
    speaker_labels: Optional[bool] = Field(
        None, description="Whether Speaker diarization is enabled"
    )
    speakers_expected: Optional[int] = Field(
        None,
        description="Tell the speaker label model how many speakers it should attempt to identify",
    )
    speaker_options: Optional[SpeakerOptions] = Field(
        None, description="Options for speaker diarization"
    )
    auto_highlights: bool = Field(..., description="Whether Key Phrases is enabled")
    auto_highlights_result: Optional[AutoHighlightsResult] = Field(
        None, description="An array of results for the Key Phrases model"
    )
    content_safety: Optional[bool] = Field(
        None, description="Whether Content Moderation is enabled"
    )
    content_safety_labels: Optional[ContentSafetyLabelsResult] = Field(
        None, description="An array of results for the Content Moderation model"
    )
    iab_categories: Optional[bool] = Field(
        None, description="Whether Topic Detection is enabled"
    )
    iab_categories_result: Optional[TopicDetectionModelResult] = Field(
        None, description="The result of the Topic Detection model"
    )
    sentiment_analysis: Optional[bool] = Field(
        None, description="Whether Sentiment Analysis is enabled"
    )
    sentiment_analysis_results: Optional[List[SentimentAnalysisResult]] = Field(
        None, description="An array of results for the Sentiment Analysis model"
    )
    entity_detection: Optional[bool] = Field(
        None, description="Whether Entity Detection is enabled"
    )
    entities: Optional[List[Entity]] = Field(
        None, description="An array of results for the Entity Detection model"
    )
    auto_chapters: Optional[bool] = Field(
        None, description="Whether Auto Chapters is enabled"
    )
    chapters: Optional[List[Chapter]] = Field(
        None,
        description="An array of temporally sequential chapters for the audio file",
    )
    summarization: bool = Field(..., description="Whether Summarization is enabled")
    summary_type: Optional[str] = Field(
        None, description="The type of summary generated"
    )
    summary_model: Optional[str] = Field(
        None, description="The Summarization model used to generate the summary"
    )
    summary: Optional[str] = Field(
        None, description="The generated summary of the media file"
    )
    custom_spelling: Optional[List[TranscriptCustomSpelling]] = Field(
        None, description="Customize how words are spelled and formatted"
    )
    keyterms_prompt: Optional[List[str]] = Field(
        None,
        description="Improve accuracy with domain-specific words or phrases",
    )
    prompt: Optional[str] = Field(
        None,
        description="This parameter does not currently have any functionality",
        deprecated=True,
    )
    custom_topics: Optional[bool] = Field(
        None, description="Whether custom topics is enabled", deprecated=True
    )
    topics: List[str] = Field(
        default_factory=list,
        description="The list of custom topics provided",
        deprecated=True,
    )
    speech_threshold: Optional[float] = Field(
        None,
        description="Reject audio files that contain less than this fraction of speech",
        ge=0,
        le=1,
    )
    speech_understanding: Optional[SpeechUnderstanding] = Field(
        None,
        description="Speech understanding tasks like translation, speaker identification, and custom formatting",
    )
    translated_texts: Optional[dict] = Field(
        None, description="Translated text keyed by language code"
    )
    speed_boost: bool = Field(
        False, description="Whether speed boost is enabled", deprecated=True
    )
    throttled: Optional[bool] = Field(
        None, description="True while a request is throttled"
    )
    error: Optional[str] = Field(
        None, description="Error message of why the transcript failed"
    )
    webhook_url: Optional[str] = Field(
        None, description="The URL to which we send webhook requests"
    )
    webhook_status_code: Optional[int] = Field(
        None, description="The status code we received from your server"
    )
    webhook_auth: bool = Field(
        ..., description="Whether webhook authentication details were provided"
    )
    webhook_auth_header_name: Optional[str] = Field(
        None, description="The header name to be sent with webhook requests"
    )
    word_boost: List[str] = Field(
        default_factory=list, description="Words to boost in recognition"
    )
    boost_param: Optional[str] = Field(
        None, description="How much to boost specified words"
    )
    language_detection_results: Optional[dict] = Field(
        None, description="Results of language detection analysis"
    )
    project_id: Optional[int] = Field(None, description="The project ID")
    token_id: Optional[int] = Field(None, description="The token ID")
    is_deleted: Optional[bool] = Field(
        None, description="Whether the transcript has been deleted"
    )
    custom_topics_results: Optional[dict] = Field(
        None, description="Results for custom topics", deprecated=True
    )


class TranscriptParams(BaseModel):
    """Parameters for creating a transcript."""

    model_config = ConfigDict(extra="forbid", json_schema_extra={"examples": [{"audio_url": "https://assembly.ai/wildfires.mp3"}]})

    audio_url: str = Field(..., description="The URL of the audio or video file to transcribe", format="url")

    # Language settings
    language_code: Optional[TranscriptLanguageCode] = Field(
        "en_us", description="The language of your audio file. Defaults to 'en_us'."
    )
    language_codes: Optional[List[TranscriptLanguageCode]] = Field(
        None, description="The language codes of your audio file. Used for Code switching. One of the values specified must be 'en'."
    )
    language_detection: bool = Field(
        False, description="Enable Automatic language detection, either true or false."
    )
    language_detection_options: Optional[LanguageDetectionOptions] = Field(
        None, description="Specify options for Automatic Language Detection."
    )
    language_confidence_threshold: float = Field(
        0.0, description="The confidence threshold for the automatically detected language.", ge=0, le=1
    )

    # Speech model settings
    speech_model: Optional[SpeechModel] = Field(
        "universal", description="The speech model to use for the transcription.", deprecated=True
    )
    speech_models: Optional[List[SpeechModel]] = Field(
        None, description="List multiple speech models in priority order."
    )

    # Text processing settings
    punctuate: bool = Field(True, description="Enable Automatic Punctuation, can be true or false")
    format_text: bool = Field(True, description="Enable Text Formatting, can be true or false")
    disfluencies: bool = Field(False, description="Transcribe Filler Words, like 'umm', in your media file")

    # Audio channel settings
    multichannel: bool = Field(False, description="Enable Multichannel transcription, can be true or false.")
    dual_channel: bool = Field(False, description="Enable Dual Channel transcription, can be true or false.", deprecated=True)

    # Webhook settings
    webhook_url: Optional[str] = Field(None, description="The URL to which we send webhook requests.", format="url")
    webhook_auth_header_name: Optional[str] = Field(None, description="The header name to be sent with webhook requests")
    webhook_auth_header_value: Optional[str] = Field(None, description="The header value to send back with webhook requests")

    # Audio processing settings
    auto_highlights: bool = Field(False, description="Enable Key Phrases, either true or false")
    audio_start_from: Optional[int] = Field(None, description="The point in time, in milliseconds, to begin transcribing")
    audio_end_at: Optional[int] = Field(None, description="The point in time, in milliseconds, to stop transcribing")

    # Content filtering
    filter_profanity: bool = Field(False, description="Filter profanity from the transcribed text")

    # PII settings
    redact_pii: bool = Field(False, description="Redact PII from the transcribed text using the Redact PII model")
    redact_pii_audio: bool = Field(False, description="Generate a copy of the original media file with spoken PII 'beeped' out")
    redact_pii_audio_quality: RedactPiiAudioQuality = Field("mp3", description="Controls the filetype of the audio created by redact_pii_audio")
    redact_pii_policies: Optional[List[EntityType]] = Field(None, description="The list of PII Redaction policies to enable")
    redact_pii_sub: Optional[SubstitutionPolicy] = Field("hash", description="The replacement logic for detected PII")
    redact_pii_audio_options: Optional[RedactPiiAudioOptions] = Field(None, description="Specify options for PII redacted audio files")

    # Speaker settings
    speaker_labels: bool = Field(False, description="Enable Speaker diarization, can be true or false")
    speakers_expected: Optional[int] = Field(None, description="Tells the speaker label model how many speakers it should attempt to identify")
    speaker_options: Optional[SpeakerOptions] = Field(None, description="Specify options for speaker diarization")

    # AI features
    content_safety: bool = Field(False, description="Enable Content Moderation, can be true or false")
    content_safety_confidence: int = Field(50, description="The confidence threshold for the Content Moderation model", ge=25, le=100)
    iab_categories: bool = Field(False, description="Enable Topic Detection, can be true or false")
    sentiment_analysis: bool = Field(False, description="Enable Sentiment Analysis, can be true or false")
    auto_chapters: bool = Field(False, description="Enable Auto Chapters, can be true or false")
    entity_detection: bool = Field(False, description="Enable Entity Detection, can be true or false")

    # Summarization
    summarization: bool = Field(False, description="Enable Summarization, can be true or false")
    summary_model: SummaryModel = Field("informative", description="The model to summarize the transcript")
    summary_type: SummaryType = Field("bullets", description="The type of summary")

    # Customization
    custom_spelling: Optional[List[TranscriptCustomSpelling]] = Field(None, description="Customize how words are spelled and formatted")
    keyterms_prompt: List[str] = Field(default_factory=list, description="Improve accuracy with domain-specific words or phrases")
    
    # Quality settings
    speech_threshold: Optional[float] = Field(0.0, description="Reject audio files that contain less than this fraction of speech", ge=0, le=1)

    # Deprecated fields
    prompt: Optional[str] = Field(None, description="This parameter does not currently have any functionality", deprecated=True)
    custom_topics: bool = Field(False, description="Enable custom topics, either true or false", deprecated=True)
    topics: List[str] = Field(default_factory=list, description="The list of custom topics", deprecated=True)

    # Advanced features
    speech_understanding: Optional[SpeechUnderstandingInput] = Field(None, description="Enable speech understanding tasks like translation, speaker identification, and custom formatting")
