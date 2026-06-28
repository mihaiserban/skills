# Invocation

Skills split on one axis: who can invoke them.

## User-Invoked

User-invoked skills are slash-command workflows. They run only when the human
asks for them by name.

Frontmatter:

```yaml
disable-model-invocation: true
```

Use this for heavy, stateful, or interactive flows that should not start
surprisingly.

The `description` should be human-facing: a concise summary, not a trigger list.

## Model-Invoked

Model-invoked skills can be selected by the agent when the task fits. They may
also be invoked by the user.

Frontmatter:

```yaml
# omit disable-model-invocation
```

Use this for reusable discipline, references, and narrow workflows that are safe
for the model to apply proactively.

The `description` should be model-facing: include clear trigger phrasing such as
"Use when..." and "Do not use when..." where needed.

## Dependencies

Prefer skill-to-skill dependencies in prose: "Use `/domain-modeling` when...".
Avoid reaching into another skill's private reference files unless that file is
part of a documented public interface.

Shared deterministic helpers belong in top-level `scripts/`.

## Current Pack

User-invoked:

- `/setup-skills`
- `/research`

Model-invoked:

- `/design-md-style-apply`
- `/design-md-style-audit`
- `/design-md-style-picker`
- `/design-taste-distiller`
- `/domain-modeling`
- `/frontend-design`
