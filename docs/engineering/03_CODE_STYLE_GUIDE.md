# CreditBridge Code Style Guide

---

## TypeScript

Strict Mode

No any

Prefer interfaces for public contracts.

Prefer type for unions.

Readonly wherever possible.

---

## Naming

PascalCase

Components

camelCase

Functions

UPPER_CASE

Constants

useSomething

Hooks

---

## Files

One component per folder.

One responsibility.

No giant files.

Prefer files under 300 lines.

Split when necessary.

---

## Exports

Named exports only.

No default export.

---

## Imports

External

↓

Shared

↓

Feature

↓

Local

Alphabetically sorted.

---

## Functions

Small.

Pure whenever possible.

No side effects.

---

## Components

Receive data.

Don't fetch data.

Don't mutate props.

Don't know business logic.

---

## Comments

Explain WHY.

Never explain WHAT.

Bad

Increment count

Good

Avoid duplicate renders by caching previous value.

---

## Formatting

Consistent spacing.

Consistent order.

Consistent naming.

Readability first.