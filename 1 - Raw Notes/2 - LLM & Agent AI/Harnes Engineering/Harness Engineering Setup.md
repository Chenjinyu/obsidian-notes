---
sr-due: 2026-05-19
sr-interval: 1
sr-ease: 2.5
---

Date: 2026-05-19
Course:
Tags: 

# Content

I have the Anthropic article. The OpenAI one blocked direct fetching — let me find its content another way.Let me verify the current GitHub Copilot customization file conventions so my advice maps to what VS Code actually supports.I read both. The OpenAI page blocks direct fetching, but I pulled its substance from the article itself and secondary coverage; the Anthropic one I have in full. Here's what matters for your setup, then a concrete blueprint — including where your current mental model needs adjusting.

## What the two articles actually teach

**Anthropic (Harness design for long-running apps)** — the three-agent GAN-style loop:

- A **Planner** turns a short prompt into an ambitious product spec, but deliberately stays _high-level on technical implementation_. The reasoning matters: if the planner specifies granular technical details upfront and gets something wrong, the errors cascade into downstream implementation. Constrain _deliverables_, not the _path_.
- A **Generator** builds one feature at a time and self-checks before handoff.
- An **Evaluator** drives the _running_ app with Playwright, clicking through it like a user, then grades against criteria with hard pass/fail thresholds. The key finding: out of the box Claude is a poor QA agent — it identifies real issues then talks itself into approving the work anyway. Separating the builder from the judge, and explicitly tuning the judge to be skeptical, is the load-bearing trick.
- For frontend specifically, they made subjective quality gradable with four weighted criteria: **design quality, originality, craft, functionality** — weighting design and originality heavily because models default to bland, safe layouts.

**OpenAI (Harness engineering)** — the documentation architecture:

- The single-big-instructions-file approach fails. When everything is marked important, nothing is; the file goes stale and can't be verified mechanically. Treat the always-on instruction file as a **~100-line table of contents** that points into a structured `docs/` directory which is the actual system of record.
- From the agent's point of view, anything it cannot access in-context effectively does not exist — decisions in Slack/docs/your head are invisible. Push them into versioned repo files.
- Enforce architecture **mechanically** (linters, structural tests, hooks), and write lint error messages that inject the fix instruction into the agent's context.

The two are complementary: OpenAI tells you _how to structure the knowledge and guardrails_; Anthropic tells you _how to structure the agents and the feedback loop_.

## Where your current model needs correcting

A few things to adjust before you build:

1. **`.github/scripts` isn't a Copilot primitive.** Scripts are fine to _have_, but Copilot won't auto-discover them. The real VS Code Copilot primitives (these changed recently — verify on your version) are:
    
    - `.github/copilot-instructions.md` — always-on, every request. This is your table of contents.
    - `.github/instructions/*.instructions.md` — path-scoped rules via an `applyTo` glob in frontmatter.
    - `.github/prompts/*.prompt.md` — manually invoked reusable prompts.
    - `.github/agents/*.agent.md` — **personas with their own tool sets**. Note: `.chatmode.md` was renamed to `.agent.md`; rename old files if you have them. This is where your planner / executor / reviewer live.
    - `.github/skills/<name>/SKILL.md` — progressive-disclosure capability packages (instructions + scripts + templates), loaded only when relevant.
    - **Hooks** + **MCP servers** — hooks enforce hard gates at execution time; MCP gives agents live tools (Playwright, your DB).
2. **"One agent that screenshots and fixes itself" is the exact anti-pattern Anthropic warns about.** The agent that writes the code should not be the one that judges it. You want the executor to build, and a _separate_ reviewer/evaluator with a skeptical persona and Playwright access to screenshot, analyze, and file concrete failures — which the executor then fixes. The loop is the point, not a single self-correcting agent.
    
3. **"Handoffs" are a real Copilot feature** — `.agent.md` files support a `handoffs` block, so Plan → Implement → Review can be a guided chain with pre-filled context, which is the file-based handoff Anthropic describes.
    

## Recommended structure

```
your-app/
├── .github/
│   ├── copilot-instructions.md          # ~100 lines: TABLE OF CONTENTS only
│   ├── agents/
│   │   ├── planner.agent.md             # read-only tools, produces spec
│   │   ├── executor.agent.md            # full edit tools, builds one feature
│   │   ├── ui-reviewer.agent.md         # Playwright MCP, NO edit tools, skeptical
│   │   └── code-reviewer.agent.md       # read + lint tools, NO edit tools
│   ├── instructions/
│   │   ├── backend.instructions.md      # applyTo: "server/**"
│   │   ├── frontend.instructions.md     # applyTo: "web/**"
│   │   └── tests.instructions.md        # applyTo: "**/*.test.*"
│   ├── prompts/
│   │   ├── plan-feature.prompt.md
│   │   ├── implement-from-contract.prompt.md
│   │   └── qa-screenshot-pass.prompt.md
│   └── skills/
│       └── ui-qa/
│           ├── SKILL.md                 # how to run app, screenshot, grade
│           └── grading-criteria.md
├── docs/                                # THE SYSTEM OF RECORD
│   ├── README.md                        # index of all docs (cross-linked)
│   ├── product/
│   │   ├── requirements.md              # business logic, user stories
│   │   └── domain-model.md              # entities, relationships, data model
│   ├── design/
│   │   ├── design-language.md           # tokens, type, spacing, color
│   │   ├── components.md                # canonical component patterns
│   │   └── grading-criteria.md          # the 4 weighted criteria
│   ├── architecture/
│   │   ├── overview.md                  # layers + allowed dependency direction
│   │   └── decisions/ADR-0001-*.md      # architecture decision records
│   └── plans/
│       └── <feature>/spec.md            # planner output, per feature
└── ...
```

The split is deliberate: `.github/` holds _behavior_ (who does what, with which tools); `docs/` holds _truth_ (what we're building, how it should look, what rules can't be broken). The agents reference `docs/` via Markdown links so rules live in exactly one place.

## The four agents, concretely

**`planner.agent.md`** — read-only tools only (search, fetch, read), no edit capability so it can't drift into building. Its job: take your 1–4 sentence feature description plus `docs/product/requirements.md` and `docs/design/design-language.md`, and emit a spec into `docs/plans/<feature>/spec.md`. Instruct it to be ambitious on scope but to stay at the level of user stories, data model, and acceptance criteria — explicitly _not_ to dictate file structure or function signatures. End it with a handoff to the executor.

**`executor.agent.md`** — full edit tools + git + your DB MCP. It reads the spec, and before writing code it produces a short **sprint contract** (`docs/plans/<feature>/contract.md`): what it will build and exactly how each behavior will be verified. This is the negotiation step from the Anthropic piece — it bridges high-level spec to testable implementation. It builds one feature/slice at a time, runs the test suite, then hands off to review.

**`ui-reviewer.agent.md`** — Playwright MCP, read tools, **no edit tools**. This is your screenshot + self-analysis agent, done correctly. It launches the running app, clicks through the contract's behaviors like a real user, screenshots each state, and grades against `docs/design/grading-criteria.md`. Each criterion gets a hard threshold; any miss fails the whole pass and produces a specific, file-and-line-level bug list. The skepticism has to be written into the persona explicitly — something like: _"You are a hostile QA engineer. Assume the implementation is broken until you have clicked the actual control and observed the actual result. Never approve based on code reading. A feature that 'looks implemented' but wasn't exercised is a FAIL."_ Without that wording it will rubber-stamp.

**`code-reviewer.agent.md`** — separate from UI review on purpose; correctness-of-behavior and quality-of-code are different problems (a point the OpenAI commentary makes directly — the harness enforces how code is organized but doesn't validate that it does what users need; you need both). Read + lint tools, no edits. It checks the diff against `docs/architecture/overview.md` (layer/dependency violations), your `.instructions.md` conventions, security, and test coverage. Output is a review file the executor consumes.

The flow: **Planner → (handoff) → Executor builds + contract → Code-Reviewer → UI-Reviewer → Executor fixes → re-review.** Communication is file-based (spec.md, contract.md, review.md, qa-report.md) exactly as Anthropic describes — each agent writes a file the next one reads.

## How detailed should the design docs be — your specific question

This is where the two articles point in slightly different directions, and the resolution is what you want:

**Business logic / requirements (`docs/product/`)** — be _detailed_. This is the safe place for specificity because it describes _what_, not _how_. Use the structure from Anthropic's appendix example: an overview paragraph, then per-feature **user stories in "As a user, I want X so that Y" form**, plus an explicit **data model** (entities, fields, relationships, constraints). For an internal app, also document the non-obvious business rules and edge cases explicitly — those are exactly the things invisible to the agent if they only live in your head.

**Design style (`docs/design/`)** — detailed but at the level of a _system_, not pixels. The Anthropic insight is that subjective quality only becomes usable when it's gradable, so write it as something the UI-reviewer can score against:

- `design-language.md`: concrete tokens — color palette with hex + semantic roles, a type scale (specific sizes/weights/line-heights), a spacing scale, border radius, elevation, motion. Concrete enough that "is the spacing consistent" has a yes/no answer.
- `components.md`: canonical patterns for the recurring pieces (forms, tables, empty states, error states, primary/secondary actions) so the executor doesn't reinvent them per feature — this is your defense against the architectural drift OpenAI warns about, applied to UI.
- `grading-criteria.md`: the four criteria adapted to an internal app. For internal tooling I'd reweight from Anthropic's defaults — they weighted _originality_ heavily because they wanted aesthetic risk-taking; an internal business app usually wants the opposite, so weight **functionality and craft (consistency, clarity, task completion) highest**, design-quality medium, originality low. Internal users want to finish tasks, not admire a museum-quality 3D gallery.

The thing _not_ to do: don't write granular implementation specs (component file layout, prop signatures, state management choices). That's the planner-over-specification failure mode — let the executor decide the path, judge it on the deliverable.

## Two things to add that you didn't mention but should

- **Hooks for hard gates.** Put your linters/structural tests behind a hook so layer violations and convention breaks are _structurally impossible to merge_, not just discouraged in prose. This is the single highest-leverage OpenAI lesson and it's cheap. Write the lint messages to tell the agent how to fix the violation.
- **Keep `copilot-instructions.md` short and resist growth.** Every time you're tempted to add a paragraph, ask whether it belongs in a `docs/` file the instruction file _links to_ instead. Both articles independently converged on this; the always-on file should be a map, not the territory.

One closing caveat from the Anthropic piece worth internalizing: the evaluator/reviewer is worth its cost when the task sits beyond what the model does reliably solo, and harness complexity should be re-examined as models improve — components encode assumptions about model weakness that go stale. Start with the full four-agent loop, but once it's running, periodically pull a piece out and see if quality actually drops. If it doesn't, that piece was scaffolding you no longer need.

Want me to draft the actual file contents — a starter `copilot-instructions.md`, the four `.agent.md` files with frontmatter and personas, and a `grading-criteria.md` tuned for an internal app? I'd want to know your frontend stack and whether you can run a Playwright MCP server in your environment first.


# Note


# Reference

