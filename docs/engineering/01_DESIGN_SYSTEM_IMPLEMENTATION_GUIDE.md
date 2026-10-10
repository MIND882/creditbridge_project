# CreditBridge Design System Implementation Guide

Version: 1.0
Status: Stable
Owner: CreditBridge Engineering
Audience:
- Frontend Engineers
- Design Engineers
- AI Coding Assistants (Claude, DeepSeek, Codex, ChatGPT)
- Future Contributors

---

# Purpose

This document defines the engineering standards for implementing the CreditBridge Design System.

The Design Bible defines WHAT should be built.

This document defines HOW it must be built.

Every implementation must follow these standards.

No exceptions without architectural approval.

---

# Guiding Principles

The Design System exists to achieve:

- Consistency
- Scalability
- Predictability
- Reusability
- Maintainability
- Accessibility
- Performance
- Excellent Developer Experience

When multiple solutions exist:

Always choose the one that is easier to maintain over the next 5–10 years.

---

# Project Architecture

The Design System lives only here:

src/shared/design-system/

It must NEVER contain business logic.

Business logic belongs inside:

features/

The dependency direction is always:

Business Screens

↓

Business Components

↓

Patterns

↓

Composite Components

↓

Primitive Components

↓

Tokens

Never reverse this dependency.

---

# Folder Conventions

Allowed folders

design-system/

tokens/

theme/

providers/

hooks/

utils/

primitives/

composites/

patterns/

Every folder has a single responsibility.

Never mix responsibilities.

---

# Naming Conventions

Folders

PascalCase

Example

Button

Card

Drawer

MetricCard

Files

PascalCase.tsx

Button.tsx

Card.tsx

Drawer.tsx

Utility files

camelCase.ts

spacing.ts

colors.ts

motion.ts

Hooks

Always start with use

useTheme.ts

useDrawer.ts

Constants

camelCase

colors.ts

radius.ts

spacing.ts

Never abbreviate names.

Good

FinancialStatementCard

Bad

FSCard

---

# Import Rules

Always use absolute imports.

Good

import { Button } from "@/shared/design-system";

Bad

../../../Button

Never import across feature boundaries.

CRM must never import Lending components.

Shared components must never import Feature components.

---

# Export Rules

Always use named exports.

Never use default exports.

Good

export const Button

Bad

export default Button

Every folder exposes an index.ts

---

# Token Rules

Every visual value must come from tokens.

Never hardcode

colors

spacing

radius

shadows

font sizes

z-index

animations

Good

spacing.md

Bad

padding: 13px

Good

colors.primary.600

Bad

"#2563EB"

---

# Component Rules

Components are divided into three levels.

Primitive

Pure UI

No business knowledge

Examples

Button

Input

Badge

Avatar

Composite

Combinations of primitives

Examples

Card

Drawer

Modal

Table

Patterns

Business-agnostic workflows

Examples

PageHeader

MetricCard

FilterBar

SearchBar

AIInsightCard

Business components belong inside features/

Never inside Design System.

---

# State Management

Primitives should be as stateless as possible.

Prefer controlled components.

Avoid internal state unless required.

Never access Zustand directly.

Never call APIs.

---

# Styling Rules

Prefer utility-first styling.

Use design tokens.

No inline styles except dynamic positioning.

No random spacing.

No magic colors.

No duplicated classes.

---

# Tailwind Rules

Never write arbitrary values unless absolutely necessary.

Good

px-4

rounded-lg

Bad

px-[17px]

rounded-[11px]

Use semantic utilities wherever possible.

---

# TypeScript Rules

Strict mode only.

Never use any.

Prefer explicit types.

Prefer readonly.

Prefer immutable objects.

Use discriminated unions instead of booleans when appropriate.

Example

variant

instead of

isPrimary

---

# Props Design

Components should expose a minimal API.

Good

variant

size

disabled

loading

children

Avoid exposing styling props.

Bad

padding

fontSize

color

borderRadius

These come from tokens.

---

# Accessibility Rules

Every interactive component must support

Keyboard navigation

Focus visibility

ARIA attributes

Screen readers

Color contrast

Never remove focus styles.

Forms must always expose labels.

Buttons must always expose accessible names.

---

# Performance Rules

Avoid unnecessary re-renders.

Memoize only when profiling justifies it.

Avoid deep prop drilling.

Keep bundle size small.

Tree-shake everything.

Lazy load heavy components.

---

# Testing Rules

Every reusable component should eventually have

Unit Test

Accessibility Test

Visual Regression Test

Storybook Story

Tests are not required during MVP but architecture must support them.

---

# Documentation Rules

Every exported component should include

Purpose

Usage

Example

Props

Accessibility notes

Limitations

Every token file must explain

Why the token exists

When to use it

When NOT to use it

---

# AI Coding Rules

AI assistants must NEVER

Invent design decisions

Hardcode values

Duplicate components

Skip accessibility

Ignore tokens

Create feature-specific logic inside Design System

If information is missing,

STOP

Explain what is missing.

Request clarification.

Do not guess.

---

# Code Review Checklist

Before merging any Design System code verify

✓ No hardcoded values

✓ Uses design tokens

✓ Named exports

✓ Absolute imports

✓ No duplicated code

✓ Accessible

✓ Strong typing

✓ Tree-shakeable

✓ Responsive

✓ Clean documentation

✓ Follows folder conventions

✓ No business logic

---

# Future Compatibility

The Design System must be compatible with future

Dark Mode

White Label Branding

CSS Variables

React Native

Storybook

Micro Frontends

Additional Products

Never make implementation decisions that block these possibilities.

---

# Engineering Philosophy

Build for the next engineer.

Code should be obvious.

Readable beats clever.

Consistency beats creativity.

Predictability beats shortcuts.

Maintainability beats speed.

Every line of code should reduce future engineering cost.

---

# Final Rule

If an implementation conflicts with

Design Bible

or

Implementation Guide

The implementation must be rejected.

The architecture is the source of truth.