---
name: gen
description: Generate or update wiki-style documentation for the current repository using the wiki skill. Parses CLI-style arguments and invokes the skill in the appropriate execution mode.
---
# Wiki Document Generator

**Your response MUST be written in the language specified by the locale code (default: en-US).**

## Command Usage

```
gen                         # Automatic mode: full pipeline
gen --structure             # Structure-only model: generate TOC only
gen <toc.yaml>              # TOC-based model: generate from existing TOC
gen <toc.yaml> --update     # Incremental update model: update based on changes
```

## Arguments

| Argument | Description |
|----------|-------------|
| `<toc.yaml>` | Path to existing TOC file |
| `--structure` | Generate only TOC structure, stop before docs |
| `--update` | Incremental update mode (requires TOC file) |
| `--output <dir>` | Output directory (default: `./docs/wiki/`) |
| `--language <locale>` | Output language (default: `en-US`) |
| `--include <pattern>` | Include files matching pattern |
| `--exclude <pattern>` | Exclude files matching pattern |

## Workflow
Parse argument and use `wiki` skill to generate wiki document for current repository.
