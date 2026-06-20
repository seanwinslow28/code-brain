"""Evidence model: real-URL records gathered in Stage 1, consumed by fuse/verify/frame."""

from dataclasses import dataclass, field


@dataclass(frozen=True)
class EvidenceRecord:
    source_type: str   # "reddit" | "x" | "youtube" | "hn" | "sonar" | "web" | ...
    source_name: str   # "r/ProductManagement", "@handle", "G2", publication name
    url: str
    date: str          # ISO "YYYY-MM-DD" or "" if unknown
    quote: str         # verbatim text actually present at url
    engagement: int = 0


def _dedup_key(r: EvidenceRecord) -> tuple[str, str]:
    return (r.url, r.quote.strip().lower()[:200])


@dataclass
class EvidenceBundle:
    records: list[EvidenceRecord] = field(default_factory=list)
    _keys: set = field(default_factory=set)
    urls: set = field(default_factory=set)

    def add(self, record: EvidenceRecord) -> bool:
        key = _dedup_key(record)
        if key in self._keys:
            return False
        self._keys.add(key)
        self.records.append(record)
        self.urls.add(record.url)
        return True

    def has_url(self, url: str) -> bool:
        return url in self.urls
