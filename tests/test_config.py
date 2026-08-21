from movie_to_bear.core.config import settings

def test_tmdb_api_token_is_loaded() -> None:
    assert settings.tmdb_api_token == "test-token"