from typing import Dict, List, Optional
from youtube_transcript_api import YouTubeTranscriptApi
from pytube import YouTube
from app.core.config import Config
from app.models.schemas import TranscriptData, TranscriptMetadata, TranscriptSegment
import logging
import json
from pathlib import Path

logger = logging.getLogger(__name__)

class TranscriptProcessor:
    def __init__(self):
        self.transcripts_dir = Config.TRANSCRIPT_DIR
        self.target_segment_duration = 30.0
        
    def process_video(self, video_url: str) -> TranscriptData:
        try:
            video_id = video_url.split("v=")[-1]
            
            # Get transcript
            transcript_list = YouTubeTranscriptApi.get_transcript(
                video_id,
                languages=['ro']
            )
            
            # Get metadata
            metadata = self._get_video_metadata(video_id)
            
            # Create segments
            segments = self._segment_transcript(transcript_list)
            
            # Create transcript data
            transcript_data = TranscriptData(
                metadata=metadata,
                segments=segments,
                raw_transcript=' '.join(seg.text for seg in segments)
            )
            
            # Save transcript
            self._save_transcript(transcript_data)
            
            return transcript_data
            
        except Exception as e:
            logger.error(f"Error processing video: {str(e)}")
            raise

    def _get_video_metadata(self, video_id: str) -> TranscriptMetadata:
        try:
            yt = YouTube(f"https://www.youtube.com/watch?v={video_id}")
            return TranscriptMetadata(
                video_id=video_id,
                title=yt.title,
                channel_id=yt.channel_id,
                channel_name=yt.author,
                upload_date=str(yt.publish_date),
                duration=yt.length
            )
        except Exception as e:
            logger.error(f"Error getting metadata: {str(e)}")
            raise

    def _segment_transcript(self, transcript_entries: List[Dict]) -> List[TranscriptSegment]:
        segments = []
        current_segment = []
        current_duration = 0
        
        for entry in transcript_entries:
            if current_duration + entry['duration'] > self.target_segment_duration and current_segment:
                text = ' '.join(e['text'] for e in current_segment)
                start_time = current_segment[0]['start']
                end_time = current_segment[-1]['start'] + current_segment[-1]['duration']
                
                segments.append(TranscriptSegment(
                    text=text,
                    start_time=start_time,
                    end_time=end_time,
                    duration=end_time - start_time
                ))
                
                current_segment = []
                current_duration = 0
            
            current_segment.append(entry)
            current_duration += entry['duration']
        
        # Handle remaining entries
        if current_segment:
            text = ' '.join(e['text'] for e in current_segment)
            start_time = current_segment[0]['start']
            end_time = current_segment[-1]['start'] + current_segment[-1]['duration']
            
            segments.append(TranscriptSegment(
                text=text,
                start_time=start_time,
                end_time=end_time,
                duration=end_time - start_time
            ))
        
        return segments

    def _save_transcript(self, transcript_data: TranscriptData) -> None:
        output_file = self.transcripts_dir / f"{transcript_data.metadata.video_id}.json"
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(transcript_data.dict(), f, ensure_ascii=False, indent=2) 