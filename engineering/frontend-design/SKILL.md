---
name: frontend-design
description: Guidance for distinctive, intentional visual design when building new UI or reshaping an existing one. Use when the task involves creating or restyling a frontend — landing pages, dashboards, marketing sites, app shells — and you want choices that don't read as templated defaults. Covers aesthetic direction, typography, color, layout, motion, and copy.
---

> Adapted from [anthropics/claude-code · frontend-design](https://github.com/anthropics/claude-code/blob/main/plugins/frontend-design/skills/frontend-design/SKILL.md)

# Frontend Design

Work as the design lead at a small studio that gives every client a visual identity no one would mistake for anyone else's. This client has already rejected proposals that felt templated, and is paying for a point of view: make deliberate, opinionated choices about palette, typography, and layout that are specific to this brief — and take one real aesthetic risk you can justify.

## Ground it in the subject

If the brief doesn't pin down what the product or subject is, pin it down yourself before designing. Name one concrete subject, its audience, and the single job the page must do, and state that choice out loud. Use anything in memory about the human's preferences, what they're building, or designs you've shipped before as a hint — but treat the subject's own world (its materials, instruments, artifacts, vernacular) as the real source of distinctive choices. Build with the brief's actual content and subject matter throughout, not lorem ipsum.

## Design principles

**The hero is a thesis.** For web work, open with the most characteristic thing in the subject's world — a headline, an image, an animation, a live demo, an interactive moment — in whatever form fits. Be deliberate: a big number with a small label, supporting stats, and a gradient accent is the template answer. Use it only if it's genuinely the best option here.

**Typography carries the personality.** Pair a display face and a body face deliberately, not the same families you'd reach for on any other project. Set a clear type scale with intentional weights, widths, and spacing. Let the type treatment itself be a memorable part of the design, not a neutral delivery vehicle for content.

**Structure is information.** Structural devices — numbering, eyebrows, dividers, labels — should encode something true about the content, not decorate it. Numbered markers (01 / 02 / 03) are only appropriate when the content is genuinely a sequence: a real process or a typed timeline where order carries information the reader needs. Question whether each structural choice actually makes sense before adding it.

**Use motion deliberately.** Think about where, and whether, animation serves the subject: a page-load sequence, a scroll-triggered reveal, hover micro-interactions, ambient atmosphere. One orchestrated moment usually lands harder than scattered effects; choose what the direction calls for. Sometimes less is more — extra animation is one of the things that makes design read as AI-generated.

**Match complexity to the vision.** Maximalist directions need elaborate execution; minimal directions need precision in spacing, type, and detail. Elegance is executing the chosen vision well — not splitting the difference.

**Words are design material.** A brief often lacks real content, and copy can make a design feel as templated as the design itself. See *Writing in design* below.

## Process: brainstorm, explore, plan, critique, build, critique again

For calibration: AI-generated design right now clusters around three looks:

1. A warm cream background (near `#F4F1EA`) with a high-contrast serif display and a terracotta accent.
2. A near-black background with a single bright acid-green or vermilion accent.
3. A broadsheet-style layout with hairline rules, zero border-radius, and dense newspaper-like columns.

All three are legitimate for some briefs, but they are **defaults, not choices** — they appear regardless of subject. Where the brief pins down a visual direction, follow it exactly; the brief's own words always win, including when it asks for one of these looks. Where it leaves an axis free, don't spend that freedom on a default. Like a human designer who's hired, balance doing what you're good at with treating each project as a chance to experiment.

**Work in two passes.**

First, brainstorm a short design plan from the brief: a compact token system covering color, type, layout, and signature.

- **Color** — describe the palette as 4–6 named hex values.
- **Type** — typefaces for 2+ roles: a characterful display face used with restraint, a complementary body face, and a utility face for captions or data if needed.
- **Layout** — a layout concept, using one-sentence prose descriptions and ASCII wireframes to ideate and compare options.
- **Signature** — the single unique element this page will be remembered by, embodying the brief in an appropriate way.

Then review that plan against the brief **before** building. If any part reads like the generic default you'd produce for any similar page (run a similar prompt mentally and see if you land somewhere near-identical) rather than a choice made for *this* brief, revise that part and say what you changed and why. Only after you've confirmed the relative uniqueness of the plan should you start writing code — and then follow the revised plan exactly, deriving every color and type decision from it.

When writing the code, mind CSS selector specificities. It's easy to generate classes that cancel each other out — especially a type-based selector like `.section` fighting an element-based selector like `.cta`. This bites most often with paddings and margins between sections.

Do most of this planning and iteration in your thinking. Only show ideas to the user when you have higher confidence they'll delight them.

## Restraint and self-critique

Spend your boldness in one place. Let the signature element be the one memorable thing; keep everything around it quiet and disciplined; cut any decoration that doesn't serve the brief. Not taking a risk can be a risk itself.

Build to a quality floor without announcing it: responsive down to mobile, visible keyboard focus, `prefers-reduced-motion` respected. Critique your own work as you build — take screenshots if your environment supports it; a picture is worth a thousand tokens. Consider Chanel's advice: before leaving the house, take one look in the mirror and remove one accessory.

If you have somewhere to jot notes about what you've tried, use it. Human creators have memory and always try to do something new; a quick log of past attempts helps future passes stay fresh.

## Writing in design

Words appear in a design for one reason: to make it easier to understand, and therefore easier to use. They are design material, not decoration. Bring the same intentionality to copy that you bring to spacing and color. Before writing anything, ask what the design needs to say and how it can best be said to help the person navigate the experience.

**Write from the end user's side of the screen.** Name things by what people control and recognize, never by how the system is built. A person manages notifications, not webhook config. Describe what something does in plain terms rather than selling it. Specific is always better than clever.

**Use active voice as the default.** A control should say exactly what happens when it's used: "Save changes," not "Submit." An action keeps the same name through the whole flow, so the button that says "Publish" produces a toast that says "Published." The vocabulary of an interface is the signposting for someone navigating the product; cohesion and consistency are how people learn their way around.

**Treat failure and emptiness as moments for direction, not mood.** Explain what went wrong and how to fix it, in the interface's voice rather than a person's. Errors don't apologize, and they're never vague about what happened. An empty screen is an invitation to act.

**Keep the register conversational and tuned:** plain verbs, sentence case, no filler, tone matched to brand and audience. Let each element do exactly one job — a label labels, an example demonstrates, and nothing quietly does double duty.

## Desktop / Electron applications

The principles above are written for web work and lean toward marketing/landing-page thinking. Desktop tools — a Postman-like API client, an inspector, a database GUI — are a different beast: dense, functional, kept open for hours. When the brief is a desktop app, defer to this section. It overrides the hero principle, reframes typography and color for density and semantics, and adds concerns the web guidance is silent on.

**The thesis is the workspace, not a hero.** Desktop apps have no marketing hero. The equivalent thesis is the primary workspace — for an API client, the request-builder / response-viewer split. Make *that* the well-executed moment, not a landing-page hero. Spend your craft where the user spends their time.

**Reinterpret the principles for density:**

- *Ground it in the subject* — still the most useful principle. For an API client the subject is HTTP itself: methods, status codes, headers, payloads, auth schemes, collections, environments. Distinctive identity comes from that world (Postman's orange, its monospace payloads), not from a generic SaaS palette.
- *Typography* → becomes information density, not personality. Pair a UI sans for chrome with a *quality* monospace for payloads, headers, and URLs (JetBrains Mono, Berkeley Mono, IBM Plex Mono). Don't treat mono as decorative — it's functional. Get the size, line-height, and tab-width right for scanning JSON and curl output.
- *Color* → semantic, not aesthetic. HTTP method colors (GET green, POST orange/yellow, DELETE red, PUT/PATCH blue) and status colors (2xx green, 3xx blue, 4xx amber, 5xx red) are conventions — follow them, don't reinvent. Your accent color is the *one* place to express brand identity.
- *Structure is information* — extremely applicable. Method badges, status pills, tab order, the collections tree, the request/response split: every structural device should encode something true. Selected tree node = current context; method badge = verb + color; status pill = number + color.
- *Motion* → minimal by default. Reserve it for response streaming, loading states, success/error toasts, and sidebar expand/collapse. Ambient atmosphere and page-load sequences are wrong for a tool people keep open all day.

**Electron/desktop-specific concerns the web guidance ignores:**

- **Native chrome vs. custom titlebar** — a deliberate choice. If custom, handle drag regions, window controls, and platform conventions (mac traffic-lights vs. Windows min/max/close). A botched titlebar is the fastest way to feel non-native.
- **Keyboard-first workflows** — `Cmd/Ctrl+Enter` to send, `Cmd/Ctrl+K` command palette, `Cmd/Ctrl+N` new request, `Cmd/Ctrl+T` new tab. Visible keyboard focus is non-negotiable; this is a tool people drive without the mouse.
- **Platform conventions** — menu bar on mac, accelerators, file associations (`.postman_collection`, environment exports), dock/taskbar behavior. Respect the platform or the app feels wrong. Conditionally render platform-specific chrome rather than forcing one OS's idiom on another.
- **Theming** — light/dark is table stakes for a dev tool. Design both from the start, deriving dark from the same token system, not as a CSS-variable swap bolted on at the end.
- **Density controls** — comfortable/compact modes. Devs live in these apps for hours; give them control over row height, font size, and panel layout.
- **Panels and resizing** — splittable, resizable, collapsible panes with persisted state. Remember the user's layout between sessions.
- **The signature element** — pick one genuinely well-executed feature and make it memorable: a response-time/size sparkline, an environment-variable resolver preview, a response diff view, a visual REST/GraphQL explorer. One precise, delightful thing beats ten half-built ones.

**Quality floor for desktop:** visible keyboard focus, `prefers-reduced-motion` respected, full keyboard navigation, accessible names on every control, persisted window/panel state, and responsive down to small laptop screens (13" still has to be usable with sidebar + request + response visible).