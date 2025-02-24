from app.models import Group, Word


def test_word_to_dict():
    """Test Word model to_dict() method matches API specs."""
    word = Word(
        romanian="măr",
        english="apple",
        pronunciation="mur",
        part_of_speech="noun",
        parts=["fruit"],
        learned=False,
    )
    data = word.to_dict()

    # Check all required fields from API specs
    assert data["romanian"] == "măr"
    assert data["english"] == "apple"
    assert data["pronunciation"] == "mur"
    assert data["part_of_speech"] == "noun"
    assert data["parts"] == ["fruit"]
    assert data["learned"] is False
    assert data["createdAt"] is None  # Not set in test
    assert data["updatedAt"] is None  # Not set in test
    assert data["groupIds"] == []  # No groups assigned


def test_group_to_dict():
    group = Group(name="Fruits", description="Romanian fruit vocabulary", word_count=10)
    data = group.to_dict()
    assert data["name"] == "Fruits"
    assert data["description"] == "Romanian fruit vocabulary"
    assert data["wordCount"] == 10
