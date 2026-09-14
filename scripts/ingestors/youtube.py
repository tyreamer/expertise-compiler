"""Optional adapter boundary; subtitle fetching is deliberately not implemented yet.

TODO: implement collect with optional yt-dlp subtitle-only downloads into a temporary
folder, explicit language/manual-vs-automatic selection, bounded playlist expansion,
and clear unavailable-caption errors. Return TranscriptInput records with original
caption bytes, creator/title/URL/type metadata. Never alter the IR contract or fetch
video/audio as a hidden fallback. No dependency or network access is needed today.
"""
from urllib.parse import parse_qs, urlparse


class YouTubeIngestor:
    def __init__(self, location):
        self.location = str(location)

    @staticmethod
    def accepts(location):
        value = str(location)
        url = urlparse(value if '://' in value else 'https://' + value)
        if url.scheme not in {'http', 'https'}: return False
        if url.hostname in {'youtu.be', 'www.youtu.be'}: return bool(url.path.strip('/'))
        if url.hostname not in {'youtube.com', 'www.youtube.com', 'm.youtube.com'}: return False
        query = parse_qs(url.query)
        return (url.path == '/watch' and bool(query.get('v'))) or (url.path == '/playlist' and bool(query.get('list')))

    def collect(self, metadata=None):
        from ec import Invalid
        raise Invalid('YouTube transcript fetching is not available yet. Provide exported transcript files or a transcript folder; original YouTube URLs can be retained with them.')
