# """
# Simple session-based file caching system.
# Stores files with original names during browser session only.
# """

# import logging
# import shutil
# import uuid
# from pathlib import Path
# from typing import Any
# from urllib import parse

# logger = logging.getLogger("toolfront")

# DEFAULT_CACHE_DIR = Path("toolfront_cache")

# class SessionCache:
#     """Simple session-based file cache with original file names."""

#     def __init__(self, session_id: str = None):
#         if session_id is None:
#             session_id = uuid.uuid4().hex[:8]

#         # Use platform-specific cache directory
#         cache_root = DEFAULT_CACHE_DIR
#         self.base_dir = cache_root / f"session_{session_id}"
#         self.base_dir.mkdir(parents=True, exist_ok=True)

#         logger.info(f"Created session cache: {self.base_dir}")

#     def _get_file_path(self, base_url: str, file_path: str) -> Path:
#         """Get the cached file path, preserving directory structure."""
#         # Parse base URL to get domain
#         parsed_base = parse.urlparse(base_url)
#         domain = parsed_base.netloc or "localhost"

#         # Clean file path (remove leading slash, handle relative paths)
#         clean_path = file_path.lstrip("/")

#         # Create full path: cache_dir/domain/path/to/file.ext
#         return self.base_dir / domain / clean_path

#     def get(self, base_url: str, file_path: str) -> bytes | None:
#         """Get cached file content."""
#         cache_path = self._get_file_path(base_url, file_path)
#         if cache_path.exists():
#             return cache_path.read_bytes()
#         return None

#     def get_path(self, base_url: str, file_path: str) -> Path | None:
#         """Get the actual disk path of a cached file."""
#         cache_path = self._get_file_path(base_url, file_path)
#         if cache_path.exists():
#             return cache_path
#         return None

#     def set(self, base_url: str, file_path: str, content: bytes) -> None:
#         """Cache file content."""
#         cache_path = self._get_file_path(base_url, file_path)

#         # Create directories
#         cache_path.parent.mkdir(parents=True, exist_ok=True)

#         # Write file content as-is, preserving original name
#         cache_path.write_bytes(content)

#         logger.info(f"Cached file: {file_path} -> {cache_path}")

#     def clear(self) -> None:
#         """Clear all cached files for this session."""
#         if self.base_dir.exists():
#             shutil.rmtree(self.base_dir)
#         logger.info(f"Cleared session cache: {self.base_dir}")

#     def stats(self) -> dict[str, Any]:
#         """Get cache statistics."""
#         if not self.base_dir.exists():
#             return {'size': 0, 'volume': 0, 'directory': str(self.base_dir)}

#         cache_files = [f for f in self.base_dir.glob("**/*") if f.is_file()]
#         total_size = sum(f.stat().st_size for f in cache_files)

#         return {
#             'size': len(cache_files),
#             'volume': total_size,
#             'directory': str(self.base_dir),
#         }

#     def list_cached_files(self, base_url: str = None) -> list[dict[str, Any]]:
#         """List all cached files, optionally filtered by base URL."""
#         cached_files = []

#         if not self.base_dir.exists():
#             return cached_files

#         for cache_file in self.base_dir.glob("**/*"):
#             if cache_file.is_file():
#                 try:
#                     # Extract domain and file path from cache structure
#                     rel_path = cache_file.relative_to(self.base_dir)
#                     parts = rel_path.parts
#                     if len(parts) >= 2:
#                         domain = parts[0]
#                         file_path = str(Path(*parts[1:]))

#                         if base_url is None or parse.urlparse(base_url).netloc == domain:
#                             cached_files.append({
#                                 'file_path': file_path,
#                                 'domain': domain,
#                                 'cache_path': str(cache_file),
#                                 'size': cache_file.stat().st_size,
#                             })
#                 except Exception:
#                     continue

#         return cached_files


# # Global session cache instance
# default_cache = SessionCache()


# # Convenience functions for backward compatibility
# def get_cached_file(base_url: str, file_path: str) -> bytes | None:
#     """Get cached file content."""
#     return default_cache.get(base_url, file_path)


# def get_cached_file_path(base_url: str, file_path: str) -> Path | None:
#     """Get cached file path."""
#     return default_cache.get_path(base_url, file_path)


# def cache_file(base_url: str, file_path: str, content: bytes) -> None:
#     """Cache a file."""
#     default_cache.set(base_url, file_path, content)


# def list_cached_files(base_url: str = None) -> list[dict[str, Any]]:
#     """List all cached files."""
#     return default_cache.list_cached_files(base_url)


# def get_cache_dir() -> Path:
#     """Get the current session cache directory."""
#     return default_cache.base_dir


# def cache_stats() -> dict[str, Any]:
#     """Get cache statistics."""
#     return default_cache.stats()


# def get_cache_path(file_url: str) -> Path:
#     """Get the cache path for a file."""
#     parsed = parse.urlparse(file_url)
#     return DEFAULT_CACHE_DIR / parsed.netloc.rstrip("/") / parsed.path.lstrip("/")


# def load_file_from_cache(file_url: str) -> bytes | None:
#     """Get cached file content."""
#     cache_path = get_cache_path(file_url)
#     if cache_path.exists():
#         return cache_path.read_bytes()
#     return None

# def save_file_to_cache(file_url: str, content: bytes) -> None:
#     """Cache a file."""
#     cache_path = get_cache_path(file_url)

#     cache_path.parent.mkdir(parents=True, exist_ok=True)

#     # Write file content as-is, preserving original name
#     cache_path.write_bytes(content)

#     logger.info(f"Cached file: {file_url} -> {cache_path}")


# def clear_cache() -> None:
#     """Clear all cached files."""
#     if DEFAULT_CACHE_DIR.exists():
#         shutil.rmtree(DEFAULT_CACHE_DIR)

