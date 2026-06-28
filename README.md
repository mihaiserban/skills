# Agent Skills

Agent skills for engineering, frontend design direction, DESIGN.md style
translation, taste capture, and arXiv-backed research.

## Quickstart

```bash
git clone https://github.com/mihaiserban/skills.git ~/.agents/skills
cd ~/.agents/skills && bash scripts/setup.sh
```

The script auto-detects installed harnesses (pi, Claude Code, OpenCode, Codex)
and creates symlinks so each harness sees the skills. For pi, cloning into
`~/.agents/skills/` already works — no symlink needed.

It also initializes vendored skill-pack submodules before generating manifests.

## What `setup.sh` does

| Harness | Detection | Result |
|---|---|---|
| **pi** | `~/.agents/` exists | Cloning to `~/.agents/skills/` already satisfies pi — skips symlink |
| **Claude Code** | `claude` on PATH | `~/.claude/skills/mihaiserban-skills/` → repo |
| **OpenCode** | `opencode` on PATH | `~/.opencode/skills/mihaiserban-skills/` → repo |
| **Codex** | `codex` on PATH | `~/.codex/skills/mihaiserban-skills/` → repo |

Also auto-generates `.claude-plugin/plugin.json` so Claude Code discovers
our skills plus included vendored skills.

## Skills

| Skill | Invocation | Type | Description |
|---|---|---|---|
| `/setup-skills` | User | `disable-model-invocation` | Interactive bootstrap: issue tracker, triage labels, domain doc layout |
| `/domain-modeling` | Model | Auto-invoked | Build and sharpen a project's domain glossary and ADRs |
| `/frontend-design` | Model | Auto-invoked | Distinctive, intentional visual design for new or restyled UI |
| `/design-md-style-picker` | Model | Auto-invoked | Choose a source aesthetic from `voltagent/awesome-design-md` |
| `/design-md-style-apply` | Model | Auto-invoked | Translate a selected `DESIGN.md` aesthetic into product UI |
| `/design-md-style-audit` | Model | Auto-invoked | Audit UI against a selected `DESIGN.md` source aesthetic |
| `/design-taste-distiller` | Model | Auto-invoked | Distill references into a compact `TASTE.md` |
| `/research` | User | `disable-model-invocation` | Research a technical or scientific topic on arXiv |

### User-invoked skills

Reachable only by typing the slash-command. They orchestrate — the human drives
them, and they may invoke model-invoked skills along the way.

| Skill | When to use |
|---|---|
| `/setup-skills` | Once per repo. Configures issue tracker, labels, domain layout before other skills run |
| `/research` | Research a technical or scientific topic on arXiv |

### Model-invoked skills

Can be reached automatically by the agent when the task fits, or invoked
manually by the user.

| Skill | When it fires |
|---|---|
| `/domain-modeling` | Agent sees fuzzy domain language, needs to pin down terminology, or record an architectural decision |
| `/frontend-design` | Task involves building or restyling a frontend — landing page, dashboard, app shell, marketing site |
| `/design-md-style-picker` | User wants a source design direction or asks what style to use |
| `/design-md-style-apply` | User names a `DESIGN.md` style, brand, or source path to apply |
| `/design-md-style-audit` | User asks whether an implementation matches a selected source style |
| `/design-taste-distiller` | User wants reusable visual taste guidelines or a `TASTE.md` |

## DESIGN.md Catalog

The design skills use `https://github.com/voltagent/awesome-design-md`. Ensure a
local checkout exists with:

```bash
python3 ~/.agents/skills/scripts/design_md_catalog.py ensure
```

By default it clones to `~/.cache/agents/awesome-design-md`. Set
`DESIGN_MD_ROOT=/path/to/awesome-design-md` to use a different checkout.

## Included External Skills

This repo includes `https://github.com/DietrichGebert/ponytail` as a git
submodule under `vendor/ponytail`. Setup includes Ponytail's `skills/*`
entries in `.claude-plugin/plugin.json` so host agents can discover them
alongside this pack.

Update vendored packs with:

```bash
git submodule update --remote --recursive
```

## Maintenance

`AGENTS.md` defines the package rules: published buckets, manifest policy,
README policy, and invocation categories. `docs/invocation.md` defines the
difference between user-invoked and model-invoked skills.

After adding, deleting, moving, or renaming a skill, run:

```bash
bash scripts/check-pack.sh
```

## Verification

After setup, confirm skills are active:

```bash
# pi
subagent({ action: "list" })

# Claude Code
# Type /setup-skills — should appear as a slash command

# OpenCode / Codex
# Check the skills directory exists: ls ~/.opencode/skills/mihaiserban-skills/
```

## Uninstall

```bash
cd ~/.agents/skills && bash scripts/uninstall.sh
```

Removes all symlinks created by `setup.sh`. Does NOT delete the cloned repo.

## File structure

```
/
├── README.md
├── AGENTS.md             # package rules for agents editing this repo
├── docs/
│   └── invocation.md     # user-invoked vs model-invoked vocabulary
├── scripts/
│   ├── setup.sh          # detect harnesses → create symlinks + plugin.json
│   ├── check-pack.sh     # validate README/manifest/skill structure
│   ├── design_md_catalog.py # find/clone/search awesome-design-md profiles
│   └── uninstall.sh      # remove symlinks
├── vendor/
│   └── ponytail/          # git submodule, external skills included in manifest
├── .claude-plugin/
│   └── plugin.json       # auto-generated by setup.sh
├── design/
│   ├── design-md-style-picker/
│   ├── design-md-style-apply/
│   ├── design-md-style-audit/
│   └── design-taste-distiller/
├── engineering/
│   ├── setup-skills/
│   ├── domain-modeling/
│   └── frontend-design/
└── research/
```
