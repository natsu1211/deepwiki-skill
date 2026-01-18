# Phase: toc-design (Phase 2)

## Goal

Collect project context needed for TOC design and documentation generation.

## Inputs

| Name | Required | Default | Description |
|------|----------|---------|-------------|
| `repo_path` | Yes | - | Absolute repository path |
| `output_dir` | No | `docs/wiki` | Documentation output directory |
| `context_pack` | No | `{output_dir}/_context/context_pack.json` | Context JSON from `repo-scan` |
| `language` | No | `en-US` | Output language/locale |

## Outputs

| Path | Description |
|------|-------------|
| `{output_dir}/toc.yaml` | TOC definition following schema |

## Scripts

Use `/scripts/read_files.py` to read file contents.

**Usage**:
```bash
python3 /scripts/read_files.py \
  --repo-path "{repo_path}" \
  --files '["path/to/file1", "path/to/file2"]' \
  --no-line-numbers
```

**Parameters**:

| Parameter | Required | Default | Description |
|-----------|----------|---------|-------------|
| `--repo-path` | Yes | - | Absolute repository root path |
| `--files` | Yes | - | JSON array of file paths (repo-relative) |
| `--line-numbers` | No | `true` | Include line numbers |
| `--max-size` | No | `1048576` | Max bytes per file |
| `--output` | No | stdout | Output JSON path |

## Workflow

### 1. Generate Wiki Structure

Analyze the `{output_dir}/_context/context_pack.json` and create a logical wiki structure.

1. **Review Context**:
   - Examine the project structure to identify main source directories
   - Read README to understand project purpose and features

2. **Deep Dive into Code**:
   - Identify representative files from main source directories
   - Use `/scripts/read_files.py` script to read these files
   - Understand: What classes/modules exist? What do they do? How are they organized?
   - DO NOT simply map folder names to pages

3. **Identify Logical Groupings**:
   - Based on actual code content, group related functionality
   - Example: If you find `Engine.cs`, `Renderer.cs`, `Physics.cs` → "Core Systems" page
   - Example: If you find `Button.cs`, `Toggle.cs`, `Slider.cs` → "UI Components" page

4. **Design Wiki Structure**:
   - Create pages based on logical groupings (step 3)
   - Map actual source files to each page
   - Design sections that cover different aspects of each grouping

5. **Write toc.yaml**:
   - Read `/references/toc_schema.md` to understand the schema of toc file
   - Generate `{output_dir}/toc.yaml` following the schema

#### Structure Design Principles

1. **Understand the Project Type**:
   - Web application → Frontend, Backend, API, Deployment sections
   - Library/Framework → Architecture, Core APIs, Usage Guide, Extension
   - Data pipeline → Data Sources, Processing, Storage, Orchestration
   - Unity game → Gameplay, Systems, UI, Assets, Performance
   - DevOps tool → Configuration, Workflow, Integration, Monitoring

2. **Decide Page Categories**:
   - **Overview**: General information, purpose, key features
   - **Getting Started**: Installation, setup, quick start
   - **Architecture**: System design, components, patterns
   - **Core Features**: Main functionality, modules, systems
   - **API Reference**: Endpoints, interfaces, contracts
   - **Data Management**: Database schema, data flow, state management
   - **Frontend/UI**: Components, pages, styling, interactions
   - **Backend/Services**: Server architecture, business logic, middleware
   - **Configuration**: Settings, environment variables, options
   - **Deployment**: Build process, deployment strategies, infrastructure
   - **Development**: Contributing guide, code standards, testing
   - **Extensibility**: Plugins, hooks, customization points
   - **Performance**: Optimization techniques, benchmarks
   - **Troubleshooting**: Common issues, debugging, FAQ

3. **Page Count Guidelines**:
   | Project Size | Files | Recommended Pages |
   |--------------|-------|-------------------|
   | Small | < 10 | 3-5 pages |
   | Medium | 10-50 | 5-8 pages |
   | Large | 50-200 | 8-12 pages |
   | Very Large | > 200 | 10-15 pages |

   - Focus on thorough documentation of all major aspects
   - Include both essential and specialized topics

## Validation

- [ ] TOC file generated sucessfully. All fields have valid value
- [ ] All page/section IDs in toc file are unique
- [ ] IDs use kebab-case, no special characters
- [ ] Each page has at least 1 `source_files` entry
- [ ] Nesting depth is at most 3 levels