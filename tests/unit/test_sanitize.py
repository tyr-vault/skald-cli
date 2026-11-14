from skald.utils.sanitize import is_sensitive_path


def test_sensitive_env_paths() -> None:
    assert is_sensitive_path(".env")
    assert is_sensitive_path("config/.env.production")
    assert not is_sensitive_path("src/main.py")
