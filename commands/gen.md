# Wiki Document Generator

**Your response MUST be written in the language specified by the locale code (default: en-US).**

## Command Usage

```
/deepwiki-local:gen                         # Automatic mode: full pipeline
/deepwiki-local:gen --structure             # Structure-only model: generate TOC only
/deepwiki-local:gen <toc.yaml>              # TOC-based model: generate from existing TOC
/deepwiki-local:gen <toc.yaml> --update     # Incremental update model: update based on changes
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