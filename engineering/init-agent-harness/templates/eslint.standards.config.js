// TypeScript Coding Standards — mechanically-enforceable rules.
//
// Decomposed from the TypeScript Coding Standards gist. These are the rules an
// agent CANNOT ship without tripping a lint error. Semantic/judgment rules are
// enforced by the ts-standards-reviewer agent (see AGENTS.md).
//
// IMPORTANT flat-config semantics: when two config blocks both define
// `no-restricted-syntax`, the LATER block's array REPLACES the earlier one for
// any file it matches — it does not merge. So every scoped block below carries
// its COMPLETE set of selectors for that scope.

import jsdoc from "eslint-plugin-jsdoc"

// Selectors that apply EVERYWHERE (src + tests + config). Agents cannot ship
// these regardless of file location.
const universalBans = [
  {
    selector: "TSAsExpression:not([typeAnnotation.typeName.name='const'])",
    message:
      "`as` casts are banned (Coding Standards §Casts). Use a type annotation, a brand parser, or `as const`. If unavoidable, add a `// SAFETY: ...` comment and an inline eslint-disable-next-line no-restricted-syntax.",
  },
  {
    selector: "TSTypeAssertion",
    message:
      "Angle-bracket casts `<T>x` are banned (Coding Standards §Casts). Use a type annotation or a brand parser.",
  },
  {
    selector: "CallExpression[callee.object.name='vi'][callee.property.name='mock']",
    message:
      "vi.mock is banned (Coding Standards §Testing). Use real seams: constructor-injected interfaces, service/layer overrides, in-memory fakes.",
  },
  {
    selector: "CallExpression[callee.object.name='jest'][callee.property.name='mock']",
    message:
      "jest.mock is banned (Coding Standards §Testing). Use real seams.",
  },
  {
    selector: "Identifier[name='assertNever']",
    message:
      "Use `casesHandled` / `shouldNeverHappen` from a shared prelude instead of ad-hoc assertNever helpers.",
  },
  {
    selector: "Identifier[name='absurd']",
    message:
      "Use `casesHandled` / `shouldNeverHappen` from a shared prelude instead of ad-hoc absurd helpers.",
  },
  {
    selector: "Identifier[name='unreachable']",
    message:
      "Use `casesHandled` / `shouldNeverHappen` from a shared prelude instead of ad-hoc unreachable helpers.",
  },
  {
    selector: "ExportAllDeclaration",
    message:
      "`export *` (barrel re-export) is banned (Coding Standards §Imports). Import directly from the file that owns the abstraction.",
  },
]

// Selectors for TEST files. Casts are relaxed for test fixtures (consistent with
// the project's existing test relaxations of `any` and `!`); the module-mock
// ban, barrel ban, and helper-name bans still apply.
const testBans = [
  universalBans[2], // vi.mock
  universalBans[3], // jest.mock
  universalBans[4], // assertNever
  universalBans[5], // absurd
  universalBans[6], // unreachable
  universalBans[7], // export *
]

/** @type {import("eslint").Linter.Config[]} */
export const standardsConfigs = [
  // ── src (excluding config/bootstrap): universal bans + process.env ban + JSDoc ──
  {
    files: ["src/**/*"],
    ignores: ["src/config/**", "src/bootstrap/**"],
    plugins: { jsdoc },
    rules: {
      "no-restricted-syntax": ["error", ...universalBans, {
        selector: "MemberExpression[object.name='process'][property.name='env']",
        message:
          "process.env is only allowed in src/config/** or src/bootstrap/** (Coding Standards §Configuration). Parse env at startup into typed config.",
      }],

      // JSDoc on every exported symbol (Coding Standards §Comments and JSDoc).
      "jsdoc/require-jsdoc": [
        "error",
        {
          publicOnly: true,
          contexts: [
            "ExportNamedDeclaration:not([source]) > FunctionDeclaration",
            "ExportNamedDeclaration:not([source]) > ClassDeclaration",
            "ExportNamedDeclaration:not([source]) > VariableDeclaration",
            "ExportDefaultDeclaration > FunctionDeclaration",
            "ExportDefaultDeclaration > ClassDeclaration",
            "ClassDeclaration > MethodDefinition",
            "ClassDeclaration > PropertyDefinition",
          ],
        },
      ],
      "jsdoc/require-param": "error",
      "jsdoc/require-returns": "error",
    },
  },

  // ── src/config + src/bootstrap: universal bans + JSDoc, NO process.env ban ──
  // These are the legitimate locations to read process.env at startup.
  {
    files: ["src/config/**", "src/bootstrap/**"],
    plugins: { jsdoc },
    rules: {
      "no-restricted-syntax": ["error", ...universalBans],
      "jsdoc/require-jsdoc": [
        "error",
        {
          publicOnly: true,
          contexts: [
            "ExportNamedDeclaration:not([source]) > FunctionDeclaration",
            "ExportNamedDeclaration:not([source]) > ClassDeclaration",
            "ExportNamedDeclaration:not([source]) > VariableDeclaration",
            "ExportDefaultDeclaration > FunctionDeclaration",
            "ExportDefaultDeclaration > ClassDeclaration",
            "ClassDeclaration > MethodDefinition",
            "ClassDeclaration > PropertyDefinition",
          ],
        },
      ],
      "jsdoc/require-param": "error",
      "jsdoc/require-returns": "error",
    },
  },

  // ── Tests: universal bans minus casts, no JSDoc on test code ────────────────
  {
    files: ["tests/**/*"],
    rules: {
      "no-restricted-syntax": ["error", ...testBans],
      "jsdoc/require-jsdoc": "off",
      "jsdoc/require-param": "off",
      "jsdoc/require-returns": "off",
    },
  },
]
