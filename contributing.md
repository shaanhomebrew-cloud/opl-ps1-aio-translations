# Contributing Translations

## How to fix or improve a translation

1. Open `{language}.json` (e.g. `zh-CN.json`).
2. Edit the value on the right side of the `:`. Never change the key on the left.
3. Bump `_meta.version` (e.g. `"2"` → `"3"`).
4. Bump the same language's `version` in `manifest.json`.
5. Open a Pull Request.

CI runs automatically on every PR:
- JSON must parse
- All `en-US.json` keys must be present
- Placeholder counts must match (`{0}`, `{1}` …)
- No extra keys

## Placeholders

`{0}`, `{1}` etc. must be preserved exactly. `"Found {0} games"` → `"找到 {0} 个游戏"` ✓
`"Found {0} games"` → `"找到 {} 个游戏"` ✗ (CI will fail)

## Straight quotes

**Never use `"` (ASCII double-quote) inside a value.** It breaks JSON.
Use curly quotes for your language:
- Chinese: `"…"` (U+201C / U+201D)
- French: `« … »`
- Japanese: `「 … 」`
- Or fall back to single quotes `'…'`

## Comments

`//` and `/* */` comments are allowed and preserved.
