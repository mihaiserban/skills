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

## Authored Skills

| Skill | Invocation | Type | Description |
|---|---|---|---|
| `/setup-skills` | User | `disable-model-invocation` | Interactive bootstrap: issue tracker, triage labels, domain doc layout |
| `/domain-modeling` | Model | Auto-invoked | Build and sharpen a project's domain glossary and ADRs |
| `/design` | Model | Auto-invoked | Orchestrate the design workflow: picker → apply → audit |
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
| `/design` | User asks to design a website, landing page, dashboard, app shell, or UI |
| `/design-md-style-picker` | User wants a source design direction or asks what style to use |
| `/design-md-style-apply` | User names a `DESIGN.md` style, brand, or source path to apply |
| `/design-md-style-audit` | User asks whether an implementation matches a selected source style |
| `/design-taste-distiller` | User wants reusable visual taste guidelines or a `TASTE.md` |

## DESIGN.md Catalog

The design skills use `https://github.com/voltagent/awesome-design-md`, vendored
as a git submodule at `vendor/awesome-design-md`. The `design_md_catalog.py`
script discovers it automatically — no extra setup needed.

```bash
python3 scripts/design_md_catalog.py list
python3 scripts/design_md_catalog.py search "dark dashboard trading"
python3 scripts/design_md_catalog.py show vercel --lines 100
```

## Included External Skills

Vendored skill packs live as git submodules under `vendor/`. Setup automatically
discovers any `vendor/*/skill*/` directory containing `SKILL.md` files and
includes them in `.claude-plugin/plugin.json`.

Add a new vendor skill:

```bash
bash scripts/add-vendor.sh https://github.com/vercel-labs/agent-browser
bash scripts/add-vendor.sh https://github.com/vercel-labs/agent-browser --name agent-browser
```

Remove a vendor skill:

```bash
bash scripts/remove-vendor.sh agent-browser
```

After adding or removing, re-run `bash scripts/setup.sh` to update the manifest.

Update all vendored packs:

```bash
git submodule update --remote --recursive
```

### Included

| Vendor | Source | Skills |
|---|---|---|
| **ponytail** | [DietrichGebert/ponytail](https://github.com/DietrichGebert/ponytail) | `/ponytail`, `/ponytail-review`, `/ponytail-audit`, `/ponytail-debt`, `/ponytail-gain`, `/ponytail-help` |
| **awesome-design-md** | [voltagent/awesome-design-md](https://github.com/voltagent/awesome-design-md) | DESIGN.md catalog for style picker/apply/audit |

## Maintenance

`AGENTS.md` defines the package rules: published buckets, manifest policy,
README policy, and invocation categories. `docs/invocation.md` defines the
difference between user-invoked and model-invoked skills.

After adding, deleting, moving, or renaming a skill, run:

```bash
bash scripts/check-pack.sh
```

Expected result today: `8 published skill(s), 14 manifest skill(s)`.

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

Removes all symlinks created by `setup.sh`. Does NOT delete the cloned repo or
vendored submodules.

## File structure

```
/
├── README.md
├── AGENTS.md             # package rules for agents editing this repo
├── docs/
│   └── invocation.md     # user-invoked vs model-invoked vocabulary
├── scripts/
│   ├── setup.sh          # detect harnesses → create symlinks + plugin.json
│   ├── uninstall.sh      # remove symlinks
│   ├── check-pack.sh     # validate README/manifest/skill structure
│   ├── add-vendor.sh     # add an external skill pack as a git submodule
│   ├── remove-vendor.sh  # remove a vendored skill pack submodule
│   └── design_md_catalog.py # find/search awesome-design-md profiles
├── vendor/
│   ├── ponytail/
│   │   └── skills/        # git submodule, 6 external skills
│   └── awesome-design-md/ # git submodule, DESIGN.md catalog
├── .claude-plugin/
│   └── plugin.json       # auto-generated by setup.sh, 14 skills total
├── design/
│   ├── SKILL.md               # root orchestrator — design workflow entry point
│   ├── design-md-style-picker/
│   ├── design-md-style-apply/
│   ├── design-md-style-audit/
│   └── design-taste-distiller/
├── engineering/
│   ├── setup-skills/
│   └── domain-modeling/
└── research/
```
