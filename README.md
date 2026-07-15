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
| `/adversarial-verify` | Model | Auto-invoked | Review a diff against the goal spec assuming the code is BROKEN |
| `/axiomatic-rewrite` | User | `disable-model-invocation` | Decompose a document into axioms, approve each, reassemble a fresh document |
| `/bisect-regression` | Model | Auto-invoked | Binary-search git history to find the commit that introduced a bug |
| `/blog-post` | User | `disable-model-invocation` | Distill a conversation or completed task into a mihaiserban.dev blog post |
| `/changelog-from-diff` | Model | Auto-invoked | Turn commits or a diff into a clean user-facing changelog entry |
| `/clean-commits` | Model | Auto-invoked | Turn messy WIP into clean, atomic commits |
| `/context-budget` | Model | Auto-invoked | Keep agent context lean on long sessions or big files |
| `/contract-test` | Model | Auto-invoked | Test the boundary between two systems by the contract |
| `/decision-record` | Model | Auto-invoked | Capture an architectural decision so the next session knows WHY |
| `/design` | Model | Auto-invoked | Orchestrate the design workflow: picker → apply → audit |
| `/design-md-style-picker` | Model | Auto-invoked | Choose a source aesthetic from `voltagent/awesome-design-md` |
| `/design-md-style-apply` | Model | Auto-invoked | Translate a selected `DESIGN.md` aesthetic into product UI |
| `/design-md-style-audit` | Model | Auto-invoked | Audit UI against a selected `DESIGN.md` source aesthetic |
| `/design-taste-distiller` | Model | Auto-invoked | Distill references into a compact `TASTE.md` |
| `/show-first` | User | `disable-model-invocation` | Plan a feature with a low-fi wireframe + systems plan before coding |
| `/domain-modeling` | Model | Auto-invoked | Build and sharpen a project's domain glossary and ADRs |
| `/input-validation` | Model | Auto-invoked | Validate untrusted input at the boundary |
| `/kill-dead-code` | Model | Auto-invoked | Find and remove unreachable/unused code safely |
| `/pr-from-diff` | Model | Auto-invoked | Write a PR description a reviewer can approve fast |
| `/rebase-safely` | Model | Auto-invoked | Rebase, squash, or rewrite history without losing work |

| `/research` | User | `disable-model-invocation` | Research a technical or scientific topic on arXiv |
| `/secret-scan` | Model | Auto-invoked | Catch hardcoded secrets before they get committed |
    | `/setup-skills` | User | `disable-model-invocation` | Interactive bootstrap: issue tracker, triage labels, domain doc layout |
    | `/revert-surgical` | Model | Auto-invoked | Revert a specific commit cleanly without touching unrelated changes |
    | `/skill-eval-runner` | Model | Auto-invoked | Run runtime evals on a skill to measure whether it improves agent behavior |
    | `/skill-evaluation` | Model | Auto-invoked | Evaluate a skill across 4 axes with an evidence-cited scorecard |
    | `/sql-review` | Model | Auto-invoked | Review SQL and ORM queries for correctness, safety, and performance |
    | `/governance-fanout` | Model | Auto-invoked | Fan out independent sub-jobs across fresh-context workers using file-based task specs |
    | `/systematic-debugging` | Model | Auto-invoked | Reproduce-then-isolate before proposing a fix — no guessing |
    | `/bisect-regression` | Model | Auto-invoked | Binary-search git history to find the commit that introduced a bug |
    | `/using-skills` | Model | Auto-invoked | Discover which skill applies to the current task |

### User-invoked skills

| Skill | When to use |
|---|---|
| `/axiomatic-rewrite` | Rewrite or restructure a document where every claim must be deliberate |
| `/blog-post` | User wants to turn a conversation or task into a blog post |
| `/research` | Research a technical or scientific topic on arXiv |
| `/setup-skills` | Once per repo. Configures issue tracker, labels, domain layout before other skills run |
| `/show-first` | User wants to see a feature plan + wireframe before any code is written |

### Model-invoked skills

| Skill | When it fires |
|---|---|
| `/adversarial-verify` | After code changes, before marking work done or committing |
| `/changelog-from-diff` | Before a release or writing a PR description |
| `/clean-commits` | Before opening a PR with messy commit history |
| `/context-budget` | Long sessions, big files, or agent hallucinating |
| `/contract-test` | APIs, integrations, shared interfaces |
| `/decision-record` | After any non-obvious technical choice |
| `/design` | User asks to design a website, landing page, dashboard, app shell, or UI |
| `/design-md-style-picker` | User wants a source design direction or asks what style to use |
| `/design-md-style-apply` | User names a `DESIGN.md` style, brand, or source path |
| `/design-md-style-audit` | User asks whether an implementation matches a source style |
| `/design-taste-distiller` | User wants reusable visual taste guidelines or a `TASTE.md` |
| `/domain-modeling` | Fuzzy domain language, needs to pin down terminology, or record an ADR |
| `/input-validation` | Any handler that accepts external data |
| `/kill-dead-code` | Cleanup or before a refactor |
| `/pr-from-diff` | Opening any pull request |
| `/rebase-safely` | Before any history rewrite |

| `/secret-scan` | Before any commit, on files with credentials |
    | `/skill-eval-runner` | User asks to run evals, benchmark a skill, or measure skill impact |
    | `/skill-evaluation` | User asks to evaluate, rate, audit, or compare a skill |
    | `/skill-eval-runner` | User asks to run evals, benchmark a skill, or measure skill impact |
| `/sql-review` | New queries, migrations, N+1 suspicions, slow endpoints |
| `/governance-fanout` | A goal that branches into many independent pieces |
| `/systematic-debugging` | ANY bug, test failure, crash, or unexpected behavior |
| `/bisect-regression` | A bug appeared between two known commits |
| `/revert-surgical` | A specific commit needs to be undone without reverting the whole PR |
| `/using-skills` | Starting a session or deciding which skill to apply |

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

Expected result today: `26 published skill(s), 32 manifest skill(s)`.

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
    │   ├── design_md_catalog.py # find/search awesome-design-md profiles
    │   ├── eval-runner.py       # run with/without-skill evals via opencode
    │   ├── eval-grade.py        # grade outputs against assertions
    │   ├── eval-aggregate.py    # aggregate into benchmark.json + HTML
    │   └── start-evals.sh       # full pipeline: run → grade → aggregate
├── vendor/
│   ├── ponytail/
│   │   └── skills/        # git submodule, 6 external skills
│   └── awesome-design-md/ # git submodule, DESIGN.md catalog
├── .claude-plugin/
│   └── plugin.json
├── agents/
│   ├── context-budget/
│   └── governance-fanout/
├── design/
│   ├── SKILL.md               # root orchestrator — design workflow entry point
│   ├── design-md-style-picker/
│   ├── design-md-style-apply/
│   ├── design-md-style-audit/
│   ├── design-taste-distiller/
│   └── show-first/
├── documentation/
│   ├── axiomatic-rewrite/
│   ├── changelog-from-diff/
│   └── decision-record/
├── engineering/
│   ├── adversarial-verify/
│   ├── bisect-regression/
│   ├── contract-test/
│   ├── domain-modeling/
│   ├── input-validation/
│   ├── kill-dead-code/
    │   ├── secret-scan/
│   ├── setup-skills/
│   ├── sql-review/
│   └── systematic-debugging/
    ├── general/
    │   ├── skill-eval-runner/
    │   └── skill-evaluation/
├── git-ops/
│   ├── clean-commits/
│   ├── pr-from-diff/
│   ├── rebase-safely/
│   └── revert-surgical/
├── mihaiserban.dev/
│   └── blog-post/
└── research/
```
