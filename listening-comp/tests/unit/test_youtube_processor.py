import pytest
from transcript_service.youtube_processor import YouTubeProcessor
from transcript_service.models import TranscriptSegment

@pytest.fixture
def sample_transcript():
    return [
        {'text': 'Bună ziua', 'start': 0.0, 'duration': 2.0},
        {'text': 'cum ești?', 'start': 2.0, 'duration': 1.5}
    ]

def test_segment_transcript(youtube_processor, sample_transcript):
    segments = youtube_processor.segment_transcript(sample_transcript)
    assert len(segments) == 1
    assert isinstance(segments[0], TranscriptSegment)
    assert segments[0].text == "Bună ziua cum ești?"
    assert segments[0].duration == 3.5

def test_get_video_metadata(youtube_processor):
    metadata = youtube_processor.get_video_metadata("test_video_id")
    assert metadata.video_id == "test_video_id" 