"""FTC affiliate disclosure for public HTML."""

FTC_HTML = """
<div class="affiliate-disclosure" style="margin-bottom:1.5rem;padding:1rem;border-left:4px solid #f59e0b;background:#fffbeb;">
  <strong>Affiliate Disclosure:</strong> This article contains affiliate links.
  If you purchase through them, I may earn a commission at no extra cost to you.
  I only recommend products I have researched and believe solve a real problem.
</div>
""".strip()

FTC_MARKDOWN = """
> **Affiliate Disclosure:** This article contains affiliate links. If you purchase through them, I may earn a commission at no extra cost to you.
""".strip()


def wrap_html(body: str) -> str:
    return f"{FTC_HTML}\n{body}"
