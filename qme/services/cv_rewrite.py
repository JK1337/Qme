"""CV rewriting toward a job description — uses main CV + life story when available."""

from dataclasses import dataclass

from qme.settings import settings


@dataclass
class RewriteResult:
    tailored_cv: str
    notes: str
    demo: bool


def rewrite_cv_for_job(
    *,
    job_description: str,
    document_cv: str,
    life_story: str = "",
) -> RewriteResult:
    """
    Tailor CV text to a job description.

    ``document_cv`` is the baseline CV for this run (pasted override or account main CV).
    ``life_story`` is woven in as narrative strengths when non-empty (from the account).
    """
    jd = job_description.strip()
    doc = document_cv.strip()
    story = life_story.strip()

    if settings.llm_provider:
        return RewriteResult(
            tailored_cv=doc,
            notes=(
                "LLM provider is set but not wired in this scaffold — pass job description, "
                "document CV, and life story into your model as context."
            ),
            demo=False,
        )

    story_bit = (
        f"\n- Surface life-story strengths: {story[:200]}{'…' if len(story) > 200 else ''}\n"
        if story
        else "\n- Add your life story in Account to strengthen every rewrite.\n"
    )
    preview = doc[:400] + ("…" if len(doc) > 400 else "") if doc else "(no CV text yet)"

    return RewriteResult(
        tailored_cv=(
            f"[Demo output]\n\n"
            f"Qme would align your main CV to this role using your full account context:\n"
            f"- Echo keywords and outcomes from the job description.\n"
            f"- Lead with proof that matches: {jd[:120]}{'…' if len(jd) > 120 else ''}"
            f"{story_bit}\n"
            f"Baseline CV excerpt:\n{preview}"
        ),
        notes=(
            "Demo mode: connect an LLM and send job_description + document_cv + life_story "
            "as system/user messages for production rewrites."
        ),
        demo=True,
    )
