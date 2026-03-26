"""Parse and normalize resume text into editable core sections."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class ResumeSections:
    profile: str = ""
    strengths: str = ""
    education: str = ""
    job_experience: str = ""
    other: str = ""


def _section_from_heading(line: str) -> str | None:
    text = line.strip().lower().rstrip(":")
    if text in {"profile", "summary", "professional summary", "about"}:
        return "profile"
    if text in {"strengths", "skills", "core strengths", "core competencies", "competencies"}:
        return "strengths"
    if text in {"education", "academic background", "academics"}:
        return "education"
    if text in {"experience", "work experience", "professional experience", "employment history"}:
        return "job_experience"
    return None


def parse_resume_sections(text: str) -> ResumeSections:
    sections = ResumeSections()
    current = "profile"
    buckets: dict[str, list[str]] = {
        "profile": [],
        "strengths": [],
        "education": [],
        "job_experience": [],
        "other": [],
    }
    for raw in text.splitlines():
        line = raw.strip()
        if not line:
            continue
        heading = _section_from_heading(line)
        if heading:
            current = heading
            continue
        buckets[current if current in buckets else "other"].append(line)

    sections.profile = "\n".join(buckets["profile"]).strip()
    sections.strengths = "\n".join(buckets["strengths"]).strip()
    sections.education = "\n".join(buckets["education"]).strip()
    sections.job_experience = "\n".join(buckets["job_experience"]).strip()
    sections.other = "\n".join(buckets["other"]).strip()
    return sections


def compose_resume_text(sections: ResumeSections) -> str:
    chunks: list[str] = []
    mapping = [
        ("Profile", sections.profile),
        ("Strengths", sections.strengths),
        ("Education", sections.education),
        ("Job Experience", sections.job_experience),
    ]
    for title, body in mapping:
        body = (body or "").strip()
        if body:
            chunks.append(f"{title}\n{body}")
    if sections.other.strip():
        chunks.append(f"Other\n{sections.other.strip()}")
    return "\n\n".join(chunks).strip()
