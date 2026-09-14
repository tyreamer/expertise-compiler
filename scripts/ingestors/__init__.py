"""Adapters produce original transcript bytes plus metadata; the IR is adapter-neutral."""
from dataclasses import dataclass
from typing import Protocol


@dataclass(frozen=True)
class TranscriptInput:
    filename: str
    raw: bytes
    metadata: dict


class Ingestor(Protocol):
    def collect(self, metadata=None) -> list[TranscriptInput]: ...


def adapter_for(location):
    from .youtube import YouTubeIngestor
    from .transcript_files import TranscriptFiles
    return YouTubeIngestor(location) if YouTubeIngestor.accepts(location) else TranscriptFiles(location)
