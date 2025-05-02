from chromadb import Client, Settings
from chromadb.utils import embedding_functions
import json
from pathlib import Path
from typing import List, Dict

class TranscriptEmbedder:
    def __init__(self, collection_name: str = "romanian_transcripts"):
        # Initialize with minimal settings
        self.client = Client(Settings(
            anonymized_telemetry=False,  # Disable telemetry
            allow_reset=True,            # Allow resetting the database
            is_persistent=False          # Use in-memory storage for now
        ))
        
        # Use a lightweight embedding model
        self.embedding_fn = embedding_functions.SentenceTransformerEmbeddingFunction(
            model_name="all-MiniLM-L6-v2"  # Smaller, faster model
        )
        
        # Create or get collection
        self.collection = self.client.get_or_create_collection(
            name=collection_name,
            embedding_function=self.embedding_fn
        )
    
    def embed_transcript(self, transcript_file: Path) -> None:
        """Embed transcript segments into vector store"""
        # Load transcript data
        with open(transcript_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Prepare documents for embedding
        ids = []
        documents = []
        metadatas = []
        
        for idx, segment in enumerate(data['segments']):
            segment_id = f"{data['metadata']['video_id']}_{idx}"
            ids.append(segment_id)
            documents.append(segment['text'])
            metadatas.append({
                "video_id": data['metadata']['video_id'],
                "start_time": segment['start_time'],
                "end_time": segment['end_time'],
                "duration": segment['duration'],
                "title": data['metadata']['title']
            })
        
        # Add to collection
        self.collection.add(
            ids=ids,
            documents=documents,
            metadatas=metadatas
        ) 