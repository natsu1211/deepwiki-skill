# Wiki Documentation Summary

Generated: 2026-06-25 03:52:49
Repository: deepwiki-skill
Commit: `5623db8cf158176a7d55791d6fb9bcb992834262`

## Generation Status

**Overall Status**: ⚠️ Incomplete

| Metric | Expected | Actual | Status |
|--------|----------|--------|--------|
| Pages | 6 | 6 | ✅ |
| Sections | 19 | 20 | ⚠️ |
| Citations | - | 373 | ✅ |
| Diagrams | 8 | 8 valid | ✅ |

## Page Details

| Page | Title | Sections | Citations | Diagrams | Status |
|------|-------|----------|-----------|----------|--------|
| 01_overview.md | Overview | 3/3 | 33 | 1 | ✅ |
| 02_architecture.md | Architecture | 3/3 | 44 | 2 | ✅ |
| 03_workflow.md | Workflow Phases and Execution Modes | 4/4 | 69 | 2 | ✅ |
| 04_scripts.md | Python Helper Scripts | 3/3 | 86 | 2 | ✅ |
| 05_policies.md | Policies, Schema, and Templates | 4/3 | 85 | 0 | ⚠️ |
| 06_cicd.md | Installation and CI/CD Integration | 3/3 | 56 | 1 | ✅ |

## Source Coverage

### Covered Files

- `.apm/agents/workflow-runner.agent.md` - cited in 02_architecture.md
- `.apm/prompts/gen-wiki.prompt.md` - cited in 02_architecture.md
- `.apm/skills/wiki/SKILL.md` - cited in 02_architecture.md
- `.apm/skills/wiki/references/doc_update_policy.md` - cited in 05_policies.md
- `.apm/skills/wiki/references/evidence_citation_policy.md` - cited in 05_policies.md
- `.apm/skills/wiki/references/mermaid_policy.md` - cited in 05_policies.md
- `.apm/skills/wiki/references/page_template.md` - cited in 05_policies.md
- `.apm/skills/wiki/references/toc_schema.md` - cited in 05_policies.md
- `.apm/skills/wiki/references/validation_policy.md` - cited in 05_policies.md
- `.apm/skills/wiki/references/workflow/doc-summary.md` - cited in 03_workflow.md
- `.apm/skills/wiki/references/workflow/doc-write.md` - cited in 03_workflow.md
- `.apm/skills/wiki/references/workflow/incremental-sync.md` - cited in 03_workflow.md
- `.apm/skills/wiki/references/workflow/repo-scan.md` - cited in 03_workflow.md
- `.apm/skills/wiki/references/workflow/toc-design.md` - cited in 03_workflow.md
- `.apm/skills/wiki/references/workflow/validate-docs.md` - cited in 03_workflow.md
- `.apm/skills/wiki/scripts/collect_context.py` - cited in 04_scripts.md
- `.apm/skills/wiki/scripts/collect_git_diff.py` - cited in 04_scripts.md
- `.apm/skills/wiki/scripts/collect_sync_context.py` - cited in 04_scripts.md
- `.apm/skills/wiki/scripts/collect_update_context.py` - cited in 04_scripts.md
- `.apm/skills/wiki/scripts/generate_summary.py` - cited in 04_scripts.md
- `.apm/skills/wiki/scripts/get_section_update_diff.py` - cited in 04_scripts.md
- `.apm/skills/wiki/scripts/read_files.py` - cited in 04_scripts.md
- `.apm/skills/wiki/scripts/requirements.txt` - cited in 04_scripts.md, 06_cicd.md
- `.apm/skills/wiki/scripts/validate_docs_structure.py` - cited in 04_scripts.md
- `.apm/skills/wiki/scripts/validate_mermaid.py` - cited in 04_scripts.md
- `.apm/skills/wiki/templates/toc.yaml.template` - cited in 05_policies.md
- `README.md` - cited in 01_overview.md, 06_cicd.md
- `apm.yml` - cited in 01_overview.md, 02_architecture.md, 06_cicd.md

### Uncovered Files

> Files listed in TOC but not cited in any documentation:

- `README.ja.md`
- `README.zh-CN.md`

## Issues

### Errors

None

### Recommendations

- Add citations for 2 uncovered source files
