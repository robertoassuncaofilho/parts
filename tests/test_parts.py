from uuid import UUID
from unittest.mock import patch, MagicMock
from app.api.parts import get_common_words

def test_create_part(client):
    response = client.post(
        "/parts/",
        json={
            "name": "Test Part",
            "sku": "TEST-001",
            "description": "This is a test part",
            "weight_ounces": 10,
            "is_active": True
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Test Part"
    assert data["sku"] == "TEST-001"
    assert UUID(data["id"])

def test_get_part(client):
    # First create a part
    create_response = client.post(
        "/parts/",
        json={
            "name": "Test Part",
            "sku": "TEST-001",
            "description": "This is a test part",
            "weight_ounces": 10,
            "is_active": True
        }
    )
    part_id = create_response.json()["id"]
    
    # Then get it
    response = client.get(f"/parts/{part_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == part_id
    assert data["name"] == "Test Part"

def test_update_part(client):
    # Create a part first
    create_response = client.post(
        "/parts/",
        json={
            "name": "Test Part",
            "sku": "TEST-001",
            "description": "This is a test part",
            "weight_ounces": 10,
            "is_active": True
        }
    )
    part_id = create_response.json()["id"]
    
    # Update it
    response = client.put(
        f"/parts/{part_id}",
        json={
            "name": "Updated Part",
            "weight_ounces": 20
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Updated Part"
    assert data["weight_ounces"] == 20
    assert data["sku"] == "TEST-001"  # Unchanged field

def test_delete_part(client):
    # Create a part
    create_response = client.post(
        "/parts/",
        json={
            "name": "Test Part",
            "sku": "TEST-001",
            "description": "This is a test part",
            "weight_ounces": 10,
            "is_active": True
        }
    )
    part_id = create_response.json()["id"]
    
    # Delete it
    response = client.delete(f"/parts/{part_id}")
    assert response.status_code == 200
    assert response.json()["message"] == "Part deleted successfully"
    
    # Verify it's gone
    get_response = client.get(f"/parts/{part_id}")
    assert get_response.status_code == 404

def test_common_words():
    # Mock data
    mock_words = [
        ("test", 2),
        ("description", 2),
        ("one", 1),
        ("two", 1),
        ("new", 1)
    ]
    
    # Create mock session
    mock_session = MagicMock()
    mock_result = MagicMock()
    mock_result.__iter__.return_value = iter(mock_words)  # Make the result iterable
    mock_session.execute.return_value = mock_result
    
    # Mock Redis
    mock_redis = MagicMock()
    mock_redis.get.return_value = None
    
    # Mock cache
    mock_cache = MagicMock()
    mock_cache.redis = mock_redis
    mock_cache.get.return_value = None
    
    with patch('app.api.parts.get_db', return_value=mock_session), \
         patch('app.api.parts.cache', mock_cache):
        
        # First call - should compute and cache
        result1 = get_common_words(mock_session)
        assert len(result1) == 5  # We should get exactly 5 words
        mock_cache.set.assert_called_once_with(result1)  # Check if set was called with the result
        
        # Second call - should use cache
        mock_cache.get.return_value = result1
        result2 = get_common_words(mock_session)
        assert result2 == result1
        assert mock_cache.get.called
        
        # Simulate cache invalidation
        mock_cache.get.return_value = None
        result3 = get_common_words(mock_session)
        assert result3 != result1  # Should be different due to cache invalidation 