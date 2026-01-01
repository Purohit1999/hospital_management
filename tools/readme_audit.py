import os
import re
import time
import json
import subprocess
from pathlib import Path
from urllib.parse import urlparse
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError


ROOT = Path(__file__).resolve().parents[1]
README_PATH = ROOT / "README.md"
REPORT_PATH = ROOT / "README_AUDIT_REPORT.md"
LIVE_SITE = "https://hospital-management-web-4963f51d811d.herokuapp.com"
GITHUB_REPO = "https://github.com/Purohit1999/hospital_management"

SECTION_KEYWORDS = {
    "features": {"features", "app features", "overview"},
    "user_stories": {"user stories"},
    "deployment": {"deployment", "heroku"},
    "payments": {"stripe", "payment"},
    "testing": {"validation", "testing", "lighthouse"},
    "architecture": {"architecture", "design"},
    "data_models": {"data models", "schema", "erd"},
    "ai": {"ai", "rag", "agent"},
    "pdf": {"pdf", "invoice"},
}

SECRET_PATTERNS = [
    re.compile(r"(sk_[A-Za-z0-9_]+)"),
    re.compile(r"(pk_[A-Za-z0-9_]+)"),
    re.compile(r"(api[_-]?key\s*[:=]\s*['\"][^'\"]+['\"])"),
    re.compile(r"(secret|token|password)\s*[:=]\s*['\"][^'\"]+['\"]", re.IGNORECASE),
]

EVIDENCE_FILES = [
    "hospitalmanagement/settings.py",
    "hospitalmanagement/urls.py",
    "hospital/views.py",
    "hospital/models.py",
    "payments/views.py",
    "payments/models.py",
    "ai_hub/views.py",
    "ai_hub/models.py",
]

EVIDENCE_DIRS = [
    "templates",
]


def redact_secrets(line: str) -> str:
    redacted = line
    for pattern in SECRET_PATTERNS:
        redacted = pattern.sub("[REDACTED]", redacted)
    return redacted


def run_git_ls_files() -> set:
    try:
        result = subprocess.run(
            ["git", "ls-files"],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=False,
        )
        if result.returncode != 0:
            return set()
        return set(result.stdout.splitlines())
    except Exception:
        return set()


def parse_readme():
    text = README_PATH.read_text(encoding="utf-8", errors="ignore")
    lines = text.splitlines()
    headings = []
    bullets_by_heading = {}
    current_heading = None
    for line in lines:
        if line.startswith("#"):
            current_heading = line.strip()
            headings.append(current_heading)
            bullets_by_heading.setdefault(current_heading, [])
            continue
        if current_heading and line.strip().startswith(("-", "*")):
            bullets_by_heading[current_heading].append(line.strip())
    images = re.findall(r"!\[[^\]]*\]\(([^)]+)\)", text)
    links = re.findall(r"\[[^\]]+\]\(([^)]+)\)", text)
    return headings, bullets_by_heading, images, links


def section_for_heading(heading: str) -> str:
    h = heading.lower()
    for section, keys in SECTION_KEYWORDS.items():
        if any(k in h for k in keys):
            return section
    return "other"


def extract_claims(bullets_by_heading):
    claims = []
    for heading, bullets in bullets_by_heading.items():
        if not bullets:
            continue
        section = section_for_heading(heading)
        for bullet in bullets:
            claims.append({"section": section, "heading": heading, "claim": bullet})
    return claims


def load_repo_text_files():
    files = []
    for rel in EVIDENCE_FILES:
        path = ROOT / rel
        if path.exists():
            files.append(path)
    for dir_name in EVIDENCE_DIRS:
        base = ROOT / dir_name
        if base.exists():
            for path in base.rglob("*"):
                if path.is_file() and path.suffix in {".html", ".py", ".txt", ".md"}:
                    files.append(path)
    return files


def keywordize(text: str):
    words = re.findall(r"[A-Za-z][A-Za-z0-9_-]+", text)
    return [w.lower() for w in words if len(w) >= 4]


def find_repo_evidence(claims):
    files = load_repo_text_files()
    evidence = []
    for claim in claims:
        keywords = keywordize(claim["claim"])
        keywords = [k for k in keywords if k not in {"with", "this", "that", "have", "from"}]
        matched = []
        for path in files:
            try:
                content = path.read_text(encoding="utf-8", errors="ignore")
            except Exception:
                continue
            for line in content.splitlines():
                line_lower = line.lower()
                if any(k in line_lower for k in keywords[:4]):
                    matched.append(f"{path.relative_to(ROOT)}: {redact_secrets(line.strip())}")
                    if len(matched) >= 3:
                        break
            if len(matched) >= 3:
                break
        evidence.append(matched)
    return evidence


def is_internal_path(link: str) -> bool:
    if link.startswith("#"):
        return False
    parsed = urlparse(link)
    return parsed.scheme == "" and parsed.netloc == ""


def is_live_site_link(link: str) -> bool:
    return link.startswith(LIVE_SITE)


def safe_head(url: str):
    req = Request(url, method="HEAD")
    try:
        with urlopen(req, timeout=10) as resp:
            return resp.status, resp.geturl(), resp.headers.get("Location")
    except HTTPError as exc:
        return exc.code, url, exc.headers.get("Location")
    except URLError:
        return None, url, None


def safe_get(url: str):
    req = Request(url, method="GET")
    try:
        with urlopen(req, timeout=10) as resp:
            return resp.status, resp.geturl(), resp.headers.get("Location")
    except HTTPError as exc:
        return exc.code, url, exc.headers.get("Location")
    except URLError:
        return None, url, None


def live_site_checks(links):
    checked = []
    to_check = [LIVE_SITE + "/"]
    for link in links:
        if is_live_site_link(link):
            to_check.append(link)
    unique = []
    for u in to_check:
        if u not in unique:
            unique.append(u)
    unique = unique[:15]

    for url in unique:
        status, final_url, location = safe_head(url)
        if status is None:
            checked.append((url, "ERROR", "Request failed"))
            time.sleep(1)
            continue
        if status in (301, 302, 303, 307, 308):
            if location and location.startswith("http") and not location.startswith(LIVE_SITE):
                checked.append((url, "EXTERNAL_NOT_TESTED", "Redirects external"))
            elif location and "login" in location.lower():
                checked.append((url, "NEEDS_AUTH", "Redirects to login"))
            else:
                status_get, _, _ = safe_get(url)
                checked.append((url, status_get or status, "GET fallback"))
        else:
            checked.append((url, status, "OK"))
        time.sleep(1)
    return checked


def validate_assets(images, links):
    git_files = run_git_ls_files()
    assets = []
    for img in images:
        if img.startswith("http"):
            assets.append((img, "EXTERNAL", "Skipped"))
            continue
        img_path = (ROOT / img).resolve()
        exists = img_path.exists()
        tracked = str(Path(img).as_posix()) in git_files
        assets.append((img, "OK" if exists else "MISSING", "tracked" if tracked else "untracked"))
    for link in links:
        if not is_internal_path(link):
            continue
        rel = link.lstrip("./")
        path = ROOT / rel
        exists = path.exists()
        tracked = str(Path(rel).as_posix()) in git_files
        assets.append((link, "OK" if exists else "MISSING", "tracked" if tracked else "untracked"))
    return assets


def build_report(claims, evidence, assets, live_checks):
    lines = []
    lines.append("# README Audit Report")
    lines.append("")
    lines.append(f"Repository: {ROOT}")
    lines.append(f"GitHub: {GITHUB_REPO}")
    lines.append(f"Live site: {LIVE_SITE}")
    lines.append("")
    lines.append("## Summary Table")
    lines.append("")
    lines.append("| Claim | Repo Evidence | Live Evidence (public only) | Status | Notes |")
    lines.append("| ----- | ------------- | --------------------------- | ------ | ----- |")
    for claim, ev in zip(claims, evidence):
        repo_evidence = " | ".join(ev) if ev else "No local match found"
        status = "PARTIAL" if ev else "FAIL"
        lines.append(
            f"| {claim['claim']} | {repo_evidence} | - | {status} | {claim['heading']} |"
        )

    lines.append("")
    lines.append("## README Asset Integrity")
    lines.append("")
    lines.append("| Asset | Status | Git |")
    lines.append("| ----- | ------ | --- |")
    for path, status, git_status in assets:
        lines.append(f"| {path} | {status} | {git_status} |")

    lines.append("")
    lines.append("## Live Site Checks (Public Only)")
    lines.append("")
    lines.append("| URL | Result | Notes |")
    lines.append("| --- | ------ | ----- |")
    for url, status, note in live_checks:
        lines.append(f"| {url} | {status} | {note} |")

    lines.append("")
    lines.append("## Gaps & Suggested Fixes")
    lines.append("")
    lines.append("- Review any claims without repo evidence and align README to code.")
    lines.append("- Verify public pages manually if a route requires authentication.")
    lines.append("- Ensure all local assets are tracked in git and referenced with correct paths.")
    return "\n".join(lines) + "\n"


def main():
    headings, bullets_by_heading, images, links = parse_readme()
    claims = extract_claims(bullets_by_heading)
    evidence = find_repo_evidence(claims)
    assets = validate_assets(images, links)
    live_checks = live_site_checks(links)
    report = build_report(claims, evidence, assets, live_checks)
    REPORT_PATH.write_text(report, encoding="utf-8")
    print(str(REPORT_PATH))


if __name__ == "__main__":
    main()
