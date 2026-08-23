"""Read resumes from plain text or PDF files."""

from __future__ import annotations

from pathlib import Path

from pypdf import PdfReader


class ResumeParser:
    SUPPORTED = {".txt", ".md", ".pdf"}

    def parse(self, path: str | Path) -> str:
        resume_path = Path(path)
        if not resume_path.exists():
            raise FileNotFoundError(f"Resume not found: {resume_path}")
        suffix = resume_path.suffix.lower()
        if suffix not in self.SUPPORTED:
            raise ValueError(
                f"Unsupported resume type '{resume_path.suffix}'. Use .txt, .md, or .pdf."
            )
        if suffix == ".pdf":
            return self._parse_pdf(resume_path)
        return resume_path.read_text(encoding="utf-8").strip()

    def _parse_pdf(self, path: Path) -> str:
        reader = PdfReader(str(path))
        pages = [page.extract_text() or "" for page in reader.pages]
        text = "\n".join(page.strip() for page in pages if page.strip()).strip()
        if not text:
            raise ValueError(f"No readable text found in PDF resume: {path}")
        return text
