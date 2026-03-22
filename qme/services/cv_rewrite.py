"""CV rewriting toward a job description — pluggable LLM; demo mode without keys."""

from dataclasses import dataclass

from qme.settings import settings


@dataclass
class RewriteResult:
    tailored_cv: str
    notes: str
    demo: bool


def rewrite_cv_for_job(*, cv_text: str, job_description: str) -> RewriteResult:
    """
    Tailor CV narrative to a job description.
    Without a configured provider, returns a structured placeholder so the UI flows.
    """
    if settings.llm_provider:
        # Future: call OpenAI / other provider using env API keys.
        return RewriteResult(
            tailored_cv=cv_text,
            notes="LLM provider is set but not wired in this scaffold — implement in cv_rewrite.",
            demo=False,
        )

    preview = cv_text.strip()[:400] + ("…" if len(cv_text.strip()) > 400 else "")
    return RewriteResult(
        tailored_cv=(
            f"[Demo output]\n\nAligned highlights for the role:\n"
            f"- Echo keywords from the job description in your experience bullets.\n"
            f"- Lead with outcomes that match: {job_description.strip()[:120]}…\n\n"
            f"Your CV excerpt:\n{preview or '(empty)'}"
        ),
        notes="Demo mode: set QME_LLM_PROVIDER and wire an API client for real rewrites.",
        demo=True,
    )
