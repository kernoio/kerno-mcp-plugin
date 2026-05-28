#!/usr/bin/env python3
"""Generate Cursor prompt deeplinks for prompts/install-cursor.md."""

from __future__ import annotations

from pathlib import Path
from urllib.parse import quote

ROOT = Path(__file__).resolve().parents[1]
PROMPT_FILE = ROOT / "prompts" / "install-cursor.md"
OUTPUT = ROOT / "references" / "cursor-install-deeplink.md"


def main() -> None:
    text = PROMPT_FILE.read_text().strip()
    encoded = quote(text, safe="")
    app = f"cursor://anysphere.cursor-deeplink/prompt?text={encoded}"
    web = f"https://cursor.com/link/prompt?text={encoded}"

    OUTPUT.write_text(
        f"""# Cursor — open install prompt in the IDE

Pre-fills the Cursor chat/Agent input with the [install-cursor](../prompts/install-cursor.md) prompt. **Does not run automatically** — review and send in Cursor.

Regenerate after editing the prompt:

```bash
python3 scripts/generate-cursor-install-deeplink.py
```

## Links

- **Web (GitHub, docs):** {web}
- **App (`cursor://`):** {app}

## Markdown (copy into README)

```markdown
**Open in Cursor:** [Open in Cursor]({web}) · [cursor:// link]({app})
```
""",
        encoding="utf-8",
    )
    print(f"Wrote {OUTPUT}")
    print(f"WEB: {web[:80]}… ({len(web)} chars)")


if __name__ == "__main__":
    main()
