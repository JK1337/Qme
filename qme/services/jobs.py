"""Mock job listings for dream-job discovery — replace with search API or DB."""

from dataclasses import dataclass


@dataclass(frozen=True)
class Job:
    id: str
    title: str
    company: str
    location: str
    work_type: str  # remote | hybrid | onsite
    employment_type: str
    salary_range: str
    seniority: str
    department: str
    posted_days_ago: int
    skills: list[str]
    snippet: str
    description: str


JOBS: list[Job] = [
    Job("job-ux-1", "Senior Product Designer", "Northline Labs", "Amsterdam, NL", "hybrid", "Full-time", "EUR 74k-95k", "Senior", "Design", 3, ["Figma", "Research", "Design Systems"], "Design systems, research-led iteration, and close collaboration with engineering.", "Own the design system and lead discovery for our B2B analytics product. Run usability tests, ship Figma-to-production handoffs, and partner with PMs on roadmap."),
    Job("job-fe-1", "Frontend Engineer (TypeScript)", "Riverstack", "Remote (EU)", "remote", "Full-time", "EUR 68k-90k", "Mid-Senior", "Engineering", 2, ["React", "TypeScript", "Accessibility"], "React, accessibility, performance — customer-facing dashboards.", "Build accessible, fast UIs in React and TypeScript. Experience with design tokens, testing, and performance profiling. Remote within EU time zones."),
    Job("job-data-1", "Data Analyst - Growth", "Crescent Mobility", "Berlin, DE", "onsite", "Full-time", "EUR 58k-75k", "Mid", "Data", 5, ["SQL", "Python", "Experimentation"], "SQL, experimentation, and storytelling for leadership.", "Own funnel metrics and experiment analysis. Present to leadership weekly and partner with marketing on attribution and lifecycle opportunities."),
    Job("job-pm-1", "Technical Product Manager", "HelioGrid", "London, UK", "hybrid", "Full-time", "GBP 80k-105k", "Senior", "Product", 4, ["APIs", "Roadmapping", "Stakeholder Mgmt"], "API products, developer experience, roadmap with engineering.", "Drive roadmap for the public API platform. Background in software or technical PM role. Comfortable reading OpenAPI specs and prioritizing with engineering squads."),
    Job("job-cs-1", "Customer Success Manager", "Plaincraft", "Remote (UK / IE)", "remote", "Full-time", "GBP 52k-66k + bonus", "Mid", "Customer", 6, ["Onboarding", "Renewals", "CRM"], "Onboarding, renewals, and expansion for SMB SaaS.", "Manage a book of SMB accounts with onboarding, QBRs, and upsell. Experience with SaaS metrics (NRR, churn) and consultative communication."),
    Job("job-devrel-1", "Developer Advocate", "OpenSpan", "Remote", "remote", "Full-time", "USD 95k-125k", "Senior", "Developer Relations", 1, ["Content", "Public Speaking", "Python"], "Content, samples, and community for an open SDK.", "Create tutorials, speak at meetups, and maintain sample apps for our SDK. Strong writing and demos, plus coding in one of Python, Go, or JavaScript."),
    Job("job-be-1", "Backend Engineer (Python)", "Arclane", "Rotterdam, NL", "hybrid", "Full-time", "EUR 72k-96k", "Senior", "Engineering", 7, ["Python", "FastAPI", "PostgreSQL"], "Own service APIs and data workflows for a scaling product.", "Design and operate backend services in Python/FastAPI with PostgreSQL and queues. Strong testing and observability mindset expected."),
    Job("job-ml-1", "ML Engineer - Ranking", "Lumina Search", "Paris, FR", "hybrid", "Full-time", "EUR 85k-112k", "Senior", "AI/ML", 9, ["PyTorch", "Ranking", "MLOps"], "Train and deploy ranking models for marketplace relevance.", "Build offline/online ranking pipelines, run A-B tests, and collaborate with product and data engineering on model serving quality."),
    Job("job-sec-1", "Security Engineer", "VaultBridge", "Remote (EMEA)", "remote", "Full-time", "EUR 88k-118k", "Senior", "Security", 8, ["Threat Modeling", "SIEM", "Cloud Security"], "Embed security in SDLC and lead incident readiness.", "Lead threat modeling, hardening, and incident response exercises. Partner across teams to reduce risk and improve detection/response cycles."),
    Job("job-qa-1", "QA Automation Engineer", "KiteLedger", "Dublin, IE", "hybrid", "Full-time", "EUR 55k-74k", "Mid", "Quality", 10, ["Playwright", "API Testing", "CI/CD"], "Automate web and API regression in a fast release cycle.", "Develop test automation strategy and maintain flaky-test hygiene. Work with engineering to shift quality left and improve release confidence."),
    Job("job-sales-1", "Account Executive (Mid-Market)", "NexaFlow", "Madrid, ES", "onsite", "Full-time", "EUR 50k OTE 100k", "Mid", "Sales", 11, ["Pipeline", "Discovery", "Negotiation"], "Own full-cycle sales from discovery to close.", "Run outbound/inbound opportunities, manage forecasts, and collaborate with CS for handover. B2B SaaS experience preferred."),
    Job("job-hr-1", "People Operations Specialist", "BrightForge", "Remote (EU)", "remote", "Part-time", "EUR 32k-44k", "Mid", "People", 12, ["HRIS", "Onboarding", "Policy"], "Improve employee experience from hiring through growth.", "Own onboarding ops, policy maintenance, and manager enablement programs. Detail-oriented with strong communication and process design skills."),
]


def list_jobs(*, q: str = "", location: str = "", work_type: str = "") -> list[Job]:
    ql = q.strip().lower()
    loc = location.strip().lower()
    wt = work_type.strip().lower()
    out: list[Job] = []
    for j in JOBS:
        hay = " ".join([
            j.title,
            j.company,
            j.snippet,
            j.department,
            j.seniority,
            " ".join(j.skills),
            j.employment_type,
        ]).lower()
        if ql and ql not in hay:
            continue
        if loc and loc not in j.location.lower():
            continue
        if wt and j.work_type != wt:
            continue
        out.append(j)
    return out


def get_job(job_id: str) -> Job | None:
    for j in JOBS:
        if j.id == job_id:
            return j
    return None
