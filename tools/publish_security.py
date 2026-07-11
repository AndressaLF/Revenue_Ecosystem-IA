"""Scan staged and tracked files before pushing to the public GitHub mirror.

Personal identifiers (ClickBank nick, Digistore ID, email, local paths) are
loaded at runtime from `.env` / optional local YAML — never hardcoded here so
this file stays safe to publish on the public mirror.
"""

from __future__ import annotations

import os
import re
import subprocess
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path

# Placeholders and public template tokens — not real credentials.
ALLOWLIST_LITERALS: frozenset[str] = frozenset(
    {
        "SEU_USUARIO",
        "SEU_NICK",
        "SEU_ID",
        "SEU_ID_AQUI",
        "YOUR_NICKNAME",
        "YOUR_AFFILIATE",
        "YOUR_AFFILIATE_ID",
        "YOUR_AFFILIATE_LINK",
        "YOUR_USERNAME",
        "VENDOR",
        "voce",
        "testnick",
        "SEU_USUARIO.github.io",
    }
)

# Affiliate= values that are OK in public docs (placeholders / fixtures).
_AFFILIATE_ALLOWLIST: frozenset[str] = frozenset(
    {
        "seu_nick",
        "your_nickname",
        "your_affiliate",
        "your_affiliate_id",
        "testnick",
        "vendor",
        "voce",
    }
)

# Paths that must never be tracked (also must appear in .gitignore).
FORBIDDEN_TRACKED_PREFIXES: tuple[str, ...] = (
    ".env",
    "secrets/",
    "storage/",
    "modules/digital_affiliate/output/",
    "cursor_avalie_",
    "cursor_",
    ".venv/",
    ".vscode/",
)

FORBIDDEN_TRACKED_EXACT: frozenset[str] = frozenset(
    {
        ".env",
        ".env.local",
        ".env.production",
        ".env.development",
    }
)

SECRET_PATTERNS: tuple[tuple[str, re.Pattern[str], str], ...] = (
    (
        "gemini_key",
        re.compile(r"GEMINI_API_KEY\s*=\s*[^\s#]{12,}", re.I),
        "GEMINI_API_KEY com valor (use .env local)",
    ),
    (
        "openai_sk",
        re.compile(r"sk-proj-[A-Za-z0-9_-]{20,}"),
        "Chave OpenAI (sk-proj-...)",
    ),
    (
        "openrouter_sk",
        re.compile(r"sk-or-v1-[A-Za-z0-9_-]{20,}"),
        "Chave OpenRouter",
    ),
    (
        "groq_gsk",
        re.compile(r"gsk_[A-Za-z0-9_-]{20,}"),
        "Chave Groq",
    ),
    (
        "cerebras_csk",
        re.compile(r"csk-[A-Za-z0-9_-]{20,}"),
        "Chave Cerebras",
    ),
    (
        "clickbank_api",
        re.compile(r"API-[A-Z0-9]{20,}"),
        "Chave API ClickBank",
    ),
    (
        "ds24_api",
        re.compile(r"DIGISTORE24_API_KEY\s*=\s*[^\s#]{12,}", re.I),
        "DIGISTORE24_API_KEY com valor",
    ),
    (
        "reddit_secret",
        re.compile(r"REDDIT_CLIENT_SECRET\s*=\s*[^\s#]{8,}", re.I),
        "REDDIT_CLIENT_SECRET com valor",
    ),
    (
        "medium_token",
        re.compile(r"MEDIUM_INTEGRATION_TOKEN\s*=\s*[^\s#]{8,}", re.I),
        "MEDIUM_INTEGRATION_TOKEN com valor",
    ),
)

# Generic PII / ops patterns — no personal literals (safe for public mirror).
_GENERIC_PII_PATTERNS: tuple[tuple[str, re.Pattern[str], str], ...] = (
    (
        "affiliate_non_placeholder",
        re.compile(r"affiliate=([A-Za-z0-9_]{3,})\b", re.I),
        "Hoplink com nickname real (use SEU_NICK / YOUR_NICKNAME no público)",
    ),
    (
        "windows_user_path",
        re.compile(r"(?:[A-Za-z]:)?[/\\]Users[/\\][^/\\\s\"']+", re.I),
        "Caminho do perfil Windows",
    ),
)


@dataclass(frozen=True)
class SecurityFinding:
    severity: str  # error | warning
    path: str
    line: int | None
    rule_id: str
    message: str

    def format(self) -> str:
        loc = f"{self.path}:{self.line}" if self.line else self.path
        return f"[{self.severity.upper()}] {loc} — {self.message} ({self.rule_id})"


def _parse_dotenv(path: Path) -> dict[str, str]:
    if not path.is_file():
        return {}
    out: dict[str, str] = {}
    try:
        text = path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return {}
    for line in text.splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#") or "=" not in stripped:
            continue
        key, _, value = stripped.partition("=")
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        if key and value:
            out[key] = value
    return out


def _load_local_yaml_patterns(repo_root: Path) -> list[tuple[str, re.Pattern[str], str]]:
    """Optional local file (gitignored) with extra regexes."""
    path = repo_root / "tools" / "publish_security_local.yaml"
    if not path.is_file():
        return []
    try:
        import yaml
    except ImportError:
        return []
    try:
        data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    except (OSError, yaml.YAMLError):
        return []
    patterns: list[tuple[str, re.Pattern[str], str]] = []
    for i, row in enumerate(data.get("patterns") or []):
        if not isinstance(row, dict):
            continue
        rule_id = str(row.get("id") or f"local_{i}")
        regex = str(row.get("regex") or "").strip()
        message = str(row.get("message") or "Padrão local de PII")
        if not regex:
            continue
        flags = re.I if row.get("ignore_case", True) else 0
        try:
            patterns.append((rule_id, re.compile(regex, flags), message))
        except re.error:
            continue
    return patterns


def _env_literal_patterns(repo_root: Path) -> list[tuple[str, re.Pattern[str], str]]:
    """Build PII patterns from local .env values (never committed)."""
    env = {**os.environ, **_parse_dotenv(repo_root / ".env")}
    patterns: list[tuple[str, re.Pattern[str], str]] = []

    nick = (env.get("CLICKBANK_NICKNAME") or "").strip()
    if nick and nick.lower() not in _AFFILIATE_ALLOWLIST:
        # Only affiliate=… — bare nick can collide with public GitHub username.
        patterns.append(
            (
                "clickbank_nickname_env",
                re.compile(rf"affiliate={re.escape(nick)}\b"),
                "Nickname ClickBank do .env em hoplink",
            )
        )

    ds24 = (env.get("DIGISTORE24_AFFILIATE_ID") or "").strip()
    if ds24 and len(ds24) >= 3:
        patterns.append(
            (
                "ds24_affiliate_env",
                re.compile(re.escape(ds24), re.I),
                "ID Digistore24 do .env",
            )
        )

    for key in ("PERSONAL_EMAIL", "CONTACT_EMAIL", "OPERATOR_EMAIL"):
        email = (env.get(key) or "").strip()
        if email and "@" in email:
            patterns.append(
                (
                    "personal_email_env",
                    re.compile(re.escape(email), re.I),
                    f"E-mail pessoal ({key}) do .env",
                )
            )
            break

    return patterns


@lru_cache(maxsize=4)
def get_pii_patterns(repo_root: str | None = None) -> tuple[tuple[str, re.Pattern[str], str], ...]:
    root = Path(repo_root) if repo_root else Path.cwd()
    combined: list[tuple[str, re.Pattern[str], str]] = list(_GENERIC_PII_PATTERNS)
    combined.extend(_env_literal_patterns(root))
    combined.extend(_load_local_yaml_patterns(root))
    return tuple(combined)


# Back-compat for tests that import PII_PATTERNS (generic only; env loaded via get_pii_patterns).
PII_PATTERNS: tuple[tuple[str, re.Pattern[str], str], ...] = _GENERIC_PII_PATTERNS


def _run_git(repo_root: Path, *args: str) -> str:
    result = subprocess.run(
        ["git", *args],
        cwd=repo_root,
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode not in (0, 1):
        raise RuntimeError(
            f"git {' '.join(args)} failed: {result.stderr.strip() or result.stdout}"
        )
    return result.stdout


def git_staged_files(repo_root: Path) -> list[str]:
    out = _run_git(repo_root, "diff", "--cached", "--name-only", "--diff-filter=ACM")
    return [line.strip() for line in out.splitlines() if line.strip()]


def git_tracked_files(repo_root: Path) -> list[str]:
    out = _run_git(repo_root, "ls-files")
    return [line.strip() for line in out.splitlines() if line.strip()]


def _is_allowlisted_match(match: re.Match[str], rule_id: str) -> bool:
    """Skip when the matched segment is a known placeholder."""
    text = match.group(0)
    if rule_id == "affiliate_non_placeholder" and match.lastindex:
        nick = match.group(1).lower()
        return nick in _AFFILIATE_ALLOWLIST

    for token in ALLOWLIST_LITERALS:
        pattern = re.compile(
            rf"(?<![A-Za-z0-9_]){re.escape(token)}(?![A-Za-z0-9_])",
            re.I,
        )
        if pattern.search(text):
            return True
    return False


def scan_text(
    rel_path: str,
    text: str,
    *,
    patterns: tuple[tuple[str, re.Pattern[str], str], ...],
) -> list[SecurityFinding]:
    findings: list[SecurityFinding] = []
    for line_no, line in enumerate(text.splitlines(), start=1):
        for rule_id, pattern, message in patterns:
            for match in pattern.finditer(line):
                if _is_allowlisted_match(match, rule_id):
                    continue
                findings.append(
                    SecurityFinding(
                        severity="error",
                        path=rel_path,
                        line=line_no,
                        rule_id=rule_id,
                        message=message,
                    )
                )
                break
            else:
                continue
            break
    return findings


def scan_file(
    repo_root: Path,
    rel_path: str,
    *,
    pii_patterns: tuple[tuple[str, re.Pattern[str], str], ...] | None = None,
) -> list[SecurityFinding]:
    path = repo_root / rel_path
    if not path.is_file():
        return []
    # Never scan the scanner itself for env-derived PII (false positives on docs).
    skip_pii = rel_path.replace("\\", "/") in {
        "tools/publish_security.py",
        "tools/publish_security_check.py",
        "tools/publish_security_local.example.yaml",
    }
    try:
        text = path.read_text(encoding="utf-8", errors="replace")
    except OSError as exc:
        return [
            SecurityFinding(
                severity="warning",
                path=rel_path,
                line=None,
                rule_id="read_error",
                message=str(exc),
            )
        ]
    findings = scan_text(rel_path, text, patterns=SECRET_PATTERNS)
    if not skip_pii:
        patterns = pii_patterns or get_pii_patterns(str(repo_root.resolve()))
        findings.extend(scan_text(rel_path, text, patterns=patterns))
    return findings


def check_forbidden_tracked(tracked: list[str]) -> list[SecurityFinding]:
    findings: list[SecurityFinding] = []
    for rel in tracked:
        rel_s = rel.replace("\\", "/")
        if rel_s in FORBIDDEN_TRACKED_EXACT:
            findings.append(
                SecurityFinding(
                    severity="error",
                    path=rel_s,
                    line=None,
                    rule_id="forbidden_tracked",
                    message="Arquivo não pode estar versionado — adicione ao .gitignore",
                )
            )
            continue
        for prefix in FORBIDDEN_TRACKED_PREFIXES:
            if rel_s == prefix.rstrip("/") or rel_s.startswith(prefix):
                findings.append(
                    SecurityFinding(
                        severity="error",
                        path=rel_s,
                        line=None,
                        rule_id="forbidden_tracked",
                        message=f"Path proibido no Git ({prefix}*) — revise .gitignore",
                    )
                )
                break
    return findings


def audit_public_push(
    repo_root: Path | None = None,
    *,
    scan_tracked: bool = True,
    scan_staged: bool = True,
) -> list[SecurityFinding]:
    """Return all security findings for a push to the public mirror."""
    root = (repo_root or Path.cwd()).resolve()
    get_pii_patterns.cache_clear()
    pii = get_pii_patterns(str(root))
    findings: list[SecurityFinding] = []

    tracked = git_tracked_files(root)
    findings.extend(check_forbidden_tracked(tracked))

    to_scan: set[str] = set()
    if scan_staged:
        to_scan.update(git_staged_files(root))
    if scan_tracked:
        to_scan.update(tracked)

    for rel in sorted(to_scan):
        findings.extend(scan_file(root, rel, pii_patterns=pii))

    return findings


def format_report(findings: list[SecurityFinding]) -> str:
    if not findings:
        return "OK — nenhum dado sensível detectado nos arquivos versionados/staged."
    errors = [f for f in findings if f.severity == "error"]
    warnings = [f for f in findings if f.severity == "warning"]
    lines = ["Falha na auditoria de publicação — push bloqueado.", ""]
    for item in errors:
        lines.append(item.format())
    if warnings:
        lines.append("")
        lines.append("Avisos:")
        for item in warnings:
            lines.append(item.format())
    lines.extend(
        [
            "",
            "Corrija ou adicione ao .gitignore antes de git push.",
            "Rodar manualmente: python tools/publish_security_check.py",
        ]
    )
    return "\n".join(lines)
