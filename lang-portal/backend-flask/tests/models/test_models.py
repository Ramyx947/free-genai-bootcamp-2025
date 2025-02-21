import pytest
from datetime import datetime
from app.models import Word, Group, WordGroup

def test_word_from_db_row():
    row = (
        1,
        "măr",
        "apple",
        "mur",
        "noun",
        '["fruit"]',
        "2024-03-20T10:00:00",
        "2024-03-20T10:00:00"
    )
    
    word = Word.from_db_row(row)
    
    assert word.id == 1
    assert word.romanian == "măr"
    assert word.english == "apple"
    assert word.pronunciation == "mur"
    assert word.part_of_speech == "noun"
    assert word.parts == ["fruit"]
    assert isinstance(word.created_at, datetime)
    assert isinstance(word.updated_at, datetime)

def test_group_from_db_row():
    row = (
        1,
        "Fruits",
        "Romanian fruit vocabulary",
        10,
        "2024-03-20T10:00:00",
        "2024-03-20T10:00:00"
    )
    
    group = Group.from_db_row(row)
    
    assert group.id == 1
    assert group.name == "Fruits"
    assert group.description == "Romanian fruit vocabulary"
    assert group.word_count == 10
    assert isinstance(group.created_at, datetime)
    assert isinstance(group.updated_at, datetime) 