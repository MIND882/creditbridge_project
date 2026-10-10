# 01_DESIGN_SYSTEM_API_CONTRACT.md

**CreditBridge Design System – API Contract**  
Version: Based on source code as of 2026-07-30  
Audience: Engineering Teams, AI Agents, Platform Integrators

---

## 1 Introduction

### Purpose
This document defines the public API surface of the CreditBridge Design System. It serves as the authoritative reference for all consuming applications, ensuring consistent usage, predictable behavior, and architectural integrity. The contract is derived directly from the source code and reflects only what is implemented.

### Scope
The contract covers all exported modules from `@creditbridge/design-system`, including:
- Primitives (atomic UI elements)
- Composites (composition of primitives)
- Patterns (opinionated, ready‑to‑use UI blocks)
- Hooks
- Providers
- Utilities
- Design Tokens
- Themes

### Goals
- Provide unambiguous API documentation for developers.
- Define extension boundaries to prevent architectural drift.
- Enable AI agents to generate correct code without hallucinations.
- Serve as a source of truth for tooling (linting, auto‑completion, codegen).

### Non‑Goals
- Not a tutorial or user guide.
- Not a design rationale document.
- No explanations of React, TypeScript, or general accessibility.
- No future roadmaps or feature proposals.

### Audience
- Frontend engineers building features on top of the Design System.
- Platform teams integrating the Design System into applications.
- AI development agents consuming the system programmatically.
- Code reviewers enforcing API compliance.

### Architecture Philosophy
The Design System follows a strict layered architecture where **dependencies flow downwards**:
- Tokens → Theme → Providers → Utilities → Primitives → Composites → Patterns → Feature Components → Pages.
- Every layer has a single responsibility and is isolated from higher layers.
- Components are **functional**, **accessible**, and **theme‑aware** via CSS custom properties.
- Composition over inheritance: higher‑level components compose lower‑level ones.
- No runtime polymorphism – use explicit props and slots.

---

## 2 Design System Layers

The following layers are implemented and documented. Layers marked “Not implemented” are architectural placeholders for future expansion.

| Layer | Responsibility | Examples | Status |
|-------|----------------|----------|--------|
| **Tokens** | Immutable design decisions (colors, spacing, typography, etc.) | `colors`, `typography`, `spacing`, `radius`, `shadows`, `motion`, `zIndex`, `breakpoints` | Implemented |
| **Theme** | Maps tokens to CSS custom properties for light/dark modes | `lightTheme`, `darkTheme` | Implemented |
| **Providers** | Injects theme context and global state into the app | `ThemeProvider` | Implemented |
| **Utilities** | Shared helper functions | `cn` (classname merging) | Implemented |
| **Primitives** | Minimal, unstyled (or minimally styled) building blocks | `Button`, `Input`, `Select`, `Checkbox`, etc. | Implemented |
| **Composites** | Compositions of primitives that create cohesive UI patterns | `Card`, `Modal`, `Tabs`, `Table`, `Drawer` | Implemented |
| **Patterns** | Opinionated, feature‑rich components for common use cases | `MetricCard`, `PageHeader`, `AIInsightCard`, `FilterBar`, `SearchBar`, `CommandPalette`, `FormSection` | Implemented |
| **Feature Components** | Business‑specific components that encapsulate domain logic | Not implemented | Placeholder |
| **Pages** | Full page layouts assembling patterns and features | Not implemented | Placeholder |

---

## 3 Component Inventory

### Primitives
| Component | Exported | Description |
|-----------|----------|-------------|
| `Avatar` | Yes | User profile image or initials with status indicator. |
| `Badge` | Yes | Small visual indicator for statuses, labels, or counts. |
| `Button` | Yes | Fully accessible button with variants, sizes, icons, and loading state. Supports polymorphic `as` prop. |
| `Checkbox` | Yes | Styled checkbox with indeterminate state and label. |
| `Icon` | Yes | Wrapper for SVG icons with consistent sizing and theming. |
| `Input` | Yes | Text input with error, helper text, prefix, and suffix. |
| `Radio` | Yes | Styled radio input with label. |
| `Select` | Yes | Custom select dropdown with single selection and keyboard navigation. |
| `Switch` | Yes | Toggle switch with loading state. |
| `Textarea` | Yes | Multi‑line text input with error, helper, character counter, and resize control. |
| `Tooltip` | Yes | Popup that displays additional information on hover/focus. |

### Composites
| Component | Exported | Subcomponents | Description |
|-----------|----------|---------------|-------------|
| `Breadcrumb` | Yes | – | Navigation trail showing current page with ellipsis overflow. |
| `Card` | Yes | `CardHeader`, `CardTitle`, `CardDescription`, `CardContent`, `CardFooter` | Flexible card with themed subcomponents. |
| `Drawer` | Yes | – | Slide‑in panel with overlay, focus trap, and keyboard support. |
| `EmptyState` | Yes | – | Displayed when no data is available, with optional actions. |
| `Modal` | Yes | `ModalHeader`, `ModalBody`, `ModalFooter` | Centered dialog with overlay, focus trap, and keyboard support. |
| `Skeleton` | Yes | – | Loading placeholder with pulse animation. |
| `Table` | Yes | `TableHeader`, `TableBody`, `TableRow`, `TableHead`, `TableCell` | Composable table with sticky header, loading, empty states, and row selection. |
| `Tabs` | Yes | `TabsList`, `Tab`, `TabPanel` | Tab component with keyboard navigation and ARIA support. |

### Patterns
| Component | Exported | Description |
|-----------|----------|-------------|
| `AIInsightCard` | Yes | Card displaying AI‑generated insights with confidence and actions. |
| `CommandPalette` | Yes | Global command palette with search and keyboard navigation. |
| `FilterBar` | Yes | Bar with search, filters, and select dropdown. |
| `FormSection` | Yes | Section with title, description, and grid layout for form fields. |
| `MetricCard` | Yes | Card displaying a key metric with value, trend, and optional badge. |
| `PageHeader` | Yes | Consistent page header with breadcrumb, title, subtitle, search, and actions. |
| `SearchBar` | Yes | Search input with clear action and keyboard support. |

### Hooks
| Hook | Exported | Description |
|------|----------|-------------|
| `useTheme` | Yes | Returns current theme mode and controls. |

### Providers
| Provider | Exported | Description |
|----------|----------|-------------|
| `ThemeProvider` | Yes | Manages theme mode, persists choice, and applies CSS custom properties. |
| `ThemeContext` | Yes | React context for theme. |

### Utilities
| Utility | Exported | Description |
|---------|----------|-------------|
| `cn` | Yes | Merges class names using `clsx` and `twMerge`. |

### Tokens
| Category | Exported | Description |
|----------|----------|-------------|
| `colors` | Yes | All color tokens (brand, neutral, semantic, surface, border, text, chart, risk, loan, ai, interaction). |
| `typography` | Yes | Font families, sizes, line heights, weights, letter spacing. |
| `spacing` | Yes | 4‑px based spacing scale. |
| `radius` | Yes | Border radius tokens. |
| `shadows` | Yes | Elevation shadows. |
| `motion` | Yes | Duration and easing tokens. |
| `zIndex` | Yes | Z‑index stacking order. |
| `breakpoints` | Yes | Screen size breakpoints. |

### Themes
| Theme | Exported | Description |
|-------|----------|-------------|
| `lightTheme` | Yes | CSS custom properties for light mode. |
| `darkTheme` | Yes | CSS custom properties for dark mode. |

---

## 4 Component API

### 4.1 Primitives

#### Avatar

**Name**: `Avatar`  
**Purpose**: Displays a user profile image or initials with a status indicator.  
**Import Path**: `@/shared/design-system/primitives/Avatar`

**Props** (extends `ImgHTMLAttributes<HTMLImageElement>`):

| Prop | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `size` | `'sm' \| 'md' \| 'lg' \| 'xl'` | No | `'md'` | Avatar size. |
| `status` | `'online' \| 'offline' \| 'away' \| null` | No | `null` | Status indicator. |
| `name` | `string` | No | – | Used to generate initials if image is unavailable. |
| `src` | `string` | No | – | Image source URL. |
| `alt` | `string` | No | – | Image alt text. |

**ForwardRef**: Yes (ref forwarded to the outer `div`).

**Accessibility**:  
- Status indicator has `aria-label` set to the status string.
- If image fails to load, initials are shown.

**Composition Rules**:  
- Should be used as a standalone element or inside `Button`, `Card`, etc.

**Limitations**:  
- No fallback icon beyond initials.

**Extension Rules**:  
- New sizes can be added by extending the `size` union and the `sizeClasses` mapping.

**Notes**:  
- The component uses `img` and handles `onError` to show initials.

---

#### Badge

**Name**: `Badge`  
**Purpose**: A small visual indicator for status, labels, or counts.  
**Import Path**: `@/shared/design-system/primitives/Badge`

**Props** (extends `HTMLAttributes<HTMLSpanElement>`):

| Prop | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `variant` | `'primary' \| 'secondary' \| 'success' \| 'warning' \| 'error' \| 'outline' \| 'ghost'` | No | `'primary'` | Visual style. |
| `size` | `'sm' \| 'md'` | No | `'md'` | Badge size. |
| `icon` | `ReactNode` | No | – | Optional icon rendered before children. |
| `children` | `ReactNode` | Yes | – | Badge content. |

**ForwardRef**: Yes (ref forwarded to `span`).

**Accessibility**:  
- No specific ARIA attributes; use `aria-label` if needed via props.

**Composition Rules**:  
- Typically used inside `MetricCard`, `AIInsightCard`, `FilterBar`, etc.

**Limitations**:  
- Cannot be used as a button; if clickable, wrap in `button`.

**Extension Rules**:  
- New variants can be added by extending `BadgeVariant` and `variantClasses`.

**Notes**:  
- Uses rounded‑full shape.

---

#### Button

**Name**: `Button`  
**Purpose**: A fully accessible button with support for variants, sizes, loading, icons, and polymorphic rendering.  
**Import Path**: `@/shared/design-system/primitives/Button`

**Props** (extends `ButtonHTMLAttributes<HTMLButtonElement>` and `AnchorHTMLAttributes<HTMLAnchorElement>` via Omit):

| Prop | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `as` | `ElementType` | No | `'button'` | The HTML element or custom component to render. |
| `variant` | `'primary' \| 'secondary' \| 'success' \| 'warning' \| 'error' \| 'outline' \| 'ghost'` | No | `'primary'` | Visual style. |
| `size` | `'sm' \| 'md' \| 'lg'` | No | `'md'` | Button size. |
| `isLoading` | `boolean` | No | `false` | Shows a spinner and disables interactions. |
| `disabled` | `boolean` | No | `false` | Disables the button. |
| `leftIcon` | `ReactNode` | No | – | Icon displayed before children. |
| `rightIcon` | `ReactNode` | No | – | Icon displayed after children. |
| `children` | `ReactNode` | Yes | – | Button content. |

**ForwardRef**: Yes (ref forwarded to the underlying element).

**Variants**:  
- `primary`, `secondary`, `success`, `warning`, `error`, `outline`, `ghost`

**Sizes**:  
- `sm`, `md`, `lg`

**States**:  
- `isLoading`: disables button, shows spinner, hides children visually (but keeps for screen readers with `aria-hidden`).  
- `disabled`: disables interactions and applies opacity.

**Accessibility**:  
- Uses `aria-disabled` and `aria-busy` when appropriate.
- Focus visible ring is provided.
- Spinner is marked `aria-hidden`.

**Controlled/Uncontrolled**: N/A.

**Dependencies**: Uses `cn`.

**Composition Rules**:  
- Can be used as a standalone or inside composites like `ModalFooter`, `CardFooter`, `AIInsightCard`, etc.
- Polymorphic `as` allows rendering as `<a>` for links.

**Limitations**:  
- When `as` is not `'button'`, the `disabled` prop is not applied to the DOM element (relies on CSS `pointer-events-none` and `onClick` prevention).
- The `onClick` handler is prevented if `isDisabled`.

**Extension Rules**:  
- New variants and sizes can be added by extending the respective unions and class maps.

**Notes**:  
- The component uses `forwardRef` and handles ref merging correctly.

---

#### Checkbox

**Name**: `Checkbox`  
**Purpose**: A fully accessible checkbox with indeterminate state.  
**Import Path**: `@/shared/design-system/primitives/Checkbox`

**Props** (extends `InputHTMLAttributes<HTMLInputElement>` with `checked`/`defaultChecked` overrides):

| Prop | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `checked` | `boolean` | No | – | Controlled checked state. |
| `defaultChecked` | `boolean` | No | – | Uncontrolled initial checked state. |
| `indeterminate` | `boolean` | No | `false` | Sets the indeterminate state visually. |
| `label` | `ReactNode` | No | – | Label rendered to the right of the checkbox. |
| `disabled` | `boolean` | No | – | Disables the checkbox. |
| *other input props* | – | No | – | Standard input props (name, value, etc.). |

**ForwardRef**: Yes (ref forwarded to `input`).

**Accessibility**:  
- Uses native `<input type="checkbox">` for full screen reader support.
- Indeterminate state is reflected via DOM property.

**Controlled/Uncontrolled**: Supports both.

**Composition Rules**:  
- Can be used in forms, inside `FormSection`, etc.

**Limitations**:  
- No custom checkbox icon; uses SVG overlay.

**Extension Rules**:  
- None defined.

**Notes**:  
- The `indeterminate` prop does not control the `checked` state; it's a visual state.

---

#### Icon

**Name**: `Icon`  
**Purpose**: A wrapper for SVG icons ensuring consistent sizing and theming.  
**Import Path**: `@/shared/design-system/primitives/Icon`

**Props** (extends `SVGAttributes<SVGSVGElement>`):

| Prop | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `size` | `'xs' \| 'sm' \| 'md' \| 'lg' \| 'xl'` | No | `'md'` | Icon size. |
| `color` | `'primary' \| 'secondary' \| 'success' \| 'warning' \| 'error' \| 'text' \| 'muted' \| 'current'` | No | `'current'` | Icon color (uses CSS classes). |
| `children` | `ReactNode` | Yes | – | SVG path(s) or content. |

**ForwardRef**: Yes (ref forwarded to `svg`).

**Accessibility**:  
- No ARIA attributes are automatically added; consumers should provide `aria-label` if needed.

**Composition Rules**:  
- Used within other components (e.g., `Button`, `SearchBar`, `AIInsightCard`).

**Limitations**:  
- Only supports stroke‑based icons (default `strokeWidth=2`).

**Extension Rules**:  
- New sizes/colors can be added by extending the respective unions and maps.

**Notes**:  
- The `svg` is rendered with `fill="none"` and `stroke="currentColor"`.

---

#### Input

**Name**: `Input`  
**Purpose**: A fully accessible text input with support for error states, helper text, prefix, and suffix.  
**Import Path**: `@/shared/design-system/primitives/Input`

**Props** (extends `InputHTMLAttributes<HTMLInputElement>` with `prefix`/`suffix` overrides):

| Prop | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `error` | `string` | No | – | Error message; triggers error styling. |
| `helper` | `string` | No | – | Helper text displayed below (if no error). |
| `prefix` | `ReactNode` | No | – | Content rendered before the input. |
| `suffix` | `ReactNode` | No | – | Content rendered after the input. |
| `disabled` | `boolean` | No | – | Disables the input. |
| `required` | `boolean` | No | – | Marks as required. |
| *other input props* | – | No | – | Standard input props (type, placeholder, value, onChange, etc.). |

**ForwardRef**: Yes (ref forwarded to `input`).

**Accessibility**:  
- Automatically generates an `id` if not provided.
- Uses `aria-invalid` and `aria-describedby` referencing helper/error IDs.
- Error and helper texts are linked via `aria-describedby`.

**Composition Rules**:  
- Used in forms, `FilterBar`, `SearchBar`, etc.

**Limitations**:  
- No support for multiple errors.

**Extension Rules**:  
- Not intended for extension; use as is.

**Notes**:  
- The container has `focus-within` styling for focus ring.

---

#### Radio

**Name**: `Radio`  
**Purpose**: A styled radio input for single selection.  
**Import Path**: `@/shared/design-system/primitives/Radio`

**Props** (extends `InputHTMLAttributes<HTMLInputElement>` with `type` removed):

| Prop | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `label` | `ReactNode` | No | – | Label rendered to the right. |
| `disabled` | `boolean` | No | – | Disables the radio. |
| *other input props* | – | No | – | Standard input props (name, value, checked, onChange, etc.). |

**ForwardRef**: Yes (ref forwarded to `input`).

**Accessibility**:  
- Native `<input type="radio">` ensures full accessibility.

**Composition Rules**:  
- Typically used in groups (by same `name`).

**Limitations**:  
- No custom radio icon; uses native appearance.

**Extension Rules**:  
- None.

**Notes**:  
- Styled with CSS for checked state.

---

#### Select

**Name**: `Select`  
**Purpose**: A custom styled select dropdown with single selection and keyboard support.  
**Import Path**: `@/shared/design-system/primitives/Select`

**Props** (extends `ButtonHTMLAttributes<HTMLButtonElement>` with `onChange`/`value` overrides):

| Prop | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `options` | `SelectOption[]` ( `{ value: string; label: string }` ) | Yes | – | List of options. |
| `value` | `string` | No | – | Controlled selected value. |
| `onChange` | `(value: string) => void` | No | – | Called when selection changes. |
| `placeholder` | `string` | No | `'Select...'` | Placeholder text when no value selected. |
| `error` | `boolean` | No | `false` | If `true`, applies error styling. |
| `disabled` | `boolean` | No | – | Disables the select. |
| `className` | `string` | No | – | Additional classes. |

**ForwardRef**: Yes (ref forwarded to `button` trigger).

**Accessibility**:  
- Uses `role="listbox"` and `role="option"`.
- `aria-haspopup`, `aria-expanded`, `aria-disabled`.
- Keyboard navigation: ArrowDown/Up to highlight, Enter to select, Escape to close.

**Controlled/Uncontrolled**: Controlled via `value` and `onChange`.

**Dependencies**: None.

**Composition Rules**:  
- Used inside `FilterBar`, forms, etc.

**Limitations**:  
- Not multi‑select.
- No async loading.

**Extension Rules**:  
- Could be extended to support async options, but not currently.

**Notes**:  
- Dropdown list is rendered absolutely; handles click‑outside to close.

---

#### Switch

**Name**: `Switch`  
**Purpose**: A toggle switch with loading state.  
**Import Path**: `@/shared/design-system/primitives/Switch`

**Props** (extends `ButtonHTMLAttributes<HTMLButtonElement>` with `onChange` overrides):

| Prop | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `checked` | `boolean` | No | – | Controlled checked state. |
| `onCheckedChange` | `(checked: boolean) => void` | No | – | Called when toggled. |
| `loading` | `boolean` | No | `false` | Shows spinner and disables. |
| `disabled` | `boolean` | No | – | Disables the switch. |

**ForwardRef**: Yes (ref forwarded to `button`).

**Accessibility**:  
- `role="switch"`, `aria-checked`, `aria-disabled`.

**Controlled/Uncontrolled**: Controlled.

**Composition Rules**:  
- Used in forms, settings panels.

**Limitations**:  
- No default unchecked state management; must be controlled.

**Extension Rules**:  
- None.

**Notes**:  
- When `loading`, children (knob) hidden and spinner shown.

---

#### Textarea

**Name**: `Textarea`  
**Purpose**: A fully accessible multi‑line text input with error, helper, character counter, and resize control.  
**Import Path**: `@/shared/design-system/primitives/Textarea`

**Props** (extends `TextareaHTMLAttributes<HTMLTextAreaElement>`):

| Prop | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `error` | `string` | No | – | Error message; triggers error styling. |
| `helper` | `string` | No | – | Helper text displayed below (if no error). |
| `resize` | `'none' \| 'vertical' \| 'horizontal' \| 'both'` | No | `'both'` | CSS resize property. |
| `showCount` | `boolean` | No | `false` | If `true`, shows character count (requires `maxLength`). |
| `maxLength` | `number` | No | – | Maximum character length; used for counter. |
| `disabled` | `boolean` | No | – | Disables the textarea. |
| `required` | `boolean` | No | – | Marks as required. |
| `value` | `string` | No | – | Controlled value. |
| *other textarea props* | – | No | – | Standard textarea props. |

**ForwardRef**: Yes (ref forwarded to `textarea`).

**Accessibility**:  
- Automatically generates `id`.
- Uses `aria-invalid` and `aria-describedby` for error/helper/counter.
- Counter text is linked via `aria-describedby`.

**Composition Rules**:  
- Used in forms.

**Limitations**:  
- No auto‑resize.

**Extension Rules**:  
- New resize options can be added.

**Notes**:  
- Character counter only appears when `showCount` and `maxLength` are set.

---

#### Tooltip

**Name**: `Tooltip`  
**Purpose**: A popup that displays additional information on hover or focus.  
**Import Path**: `@/shared/design-system/primitives/Tooltip`

**Props**:

| Prop | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `content` | `ReactNode` | Yes | – | The content to show in the tooltip. |
| `placement` | `'top' \| 'bottom' \| 'left' \| 'right'` | No | `'top'` | Preferred placement. |
| `delay` | `number` | No | `300` | Delay in ms before showing the tooltip. |
| `children` | `ReactNode` | Yes | – | The element that triggers the tooltip. |
| `className` | `string` | No | – | Additional classes for the tooltip popup. |

**ForwardRef**: Yes (ref forwarded to the outer `div`).

**Accessibility**:  
- `role="tooltip"` on the popup.
- Triggers on `mouseenter`/`mouseleave` and `focus`/`blur`.

**Composition Rules**:  
- Wraps a single child element.

**Limitations**:  
- Does not automatically manage `aria-describedby` on the child; consumers should handle if needed.

**Extension Rules**:  
- New placements can be added.

**Notes**:  
- Uses `setTimeout` for delay and cleanup.

---

### 4.2 Composites

#### Breadcrumb

**Name**: `Breadcrumb`  
**Purpose**: A navigation trail showing the current page.  
**Import Path**: `@/shared/design-system/composites/Breadcrumb`

**Props** (extends `HTMLAttributes<HTMLElement>`):

| Prop | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `items` | `BreadcrumbItem[]` ( `{ label: ReactNode; href?: string; icon?: ReactNode; isCurrent?: boolean }` ) | Yes | – | Breadcrumb items. |
| `separator` | `ReactNode` | No | `'/'` | Separator between items. |
| `maxItems` | `number` | No | – | Maximum number of items to show; if exceeded, ellipsis is inserted. |

**ForwardRef**: Yes (ref forwarded to `nav`).

**Accessibility**:  
- `aria-label="Breadcrumb"` on `nav`.
- `aria-current="page"` on the current item.

**Controlled/Uncontrolled**: N/A.

**Composition Rules**:  
- Used within `PageHeader` as `breadcrumb` slot.

**Limitations**:  
- Ellipsis truncation is simplistic; it always keeps first and last items, and inserts an ellipsis.

**Extension Rules**:  
- Could be extended with custom renderers.

**Notes**:  
- The current item is determined by `isCurrent` prop or if it's the last and has no `href`.

---

#### Card

**Name**: `Card`  
**Purpose**: A flexible card component with subcomponents for header, content, and footer.  
**Import Path**: `@/shared/design-system/composites/Card`

**Props** (extends `HTMLAttributes<HTMLDivElement>`):

| Prop | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `variant` | `'default' \| 'elevated' \| 'outline'` | No | `'default'` | Visual style. |
| `children` | `ReactNode` | Yes | – | Card content. |

**ForwardRef**: Yes (ref forwarded to the outer `div`).

**Subcomponents**:  
- `CardHeader`, `CardTitle`, `CardDescription`, `CardContent`, `CardFooter`  
  Each extends `HTMLAttributes<HTMLDivElement>` (or `HTMLHeadingElement` for `CardTitle`) and accepts `children` and `className`.

**Composition Rules**:  
- The subcomponents should be used as children of `Card`.
- `CardHeader` includes padding and flex column gap.
- `CardFooter` includes a top border and flex layout.

**Limitations**:  
- No intrinsic spacing between subcomponents; relies on padding.

**Extension Rules**:  
- New variants can be added by extending `CardVariant` and `variantClasses`.

**Notes**:  
- Uses `bg-card`, `border-border-subtle` tokens via CSS classes.

---

#### Drawer

**Name**: `Drawer`  
**Purpose**: A slide‑in panel with overlay, focus trap, and keyboard support.  
**Import Path**: `@/shared/design-system/composites/Drawer`

**Props**:

| Prop | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `open` | `boolean` | Yes | – | Controls visibility. |
| `onClose` | `() => void` | Yes | – | Called when overlay is clicked or Escape is pressed. |
| `placement` | `'right' \| 'left' \| 'top' \| 'bottom'` | No | `'right'` | Side from which the drawer slides in. |
| `children` | `ReactNode` | Yes | – | Drawer content. |
| `className` | `string` | No | – | Additional classes for the drawer panel. |
| `overlayClassName` | `string` | No | – | Additional classes for the overlay. |

**ForwardRef**: Not supported (no ref forwarding).

**Accessibility**:  
- Portaled to `document.body`.
- `role="dialog"`, `aria-modal="true"`.
- Focus trap: when open, focus is moved to the drawer; clicking outside or focusing outside will refocus the drawer.
- `Escape` key closes drawer.
- Overlay click triggers `onClose`.
- Close button has `aria-label="Close drawer"`.

**Controlled/Uncontrolled**: Controlled via `open`.

**Dependencies**: `createPortal`.

**Composition Rules**:  
- Should be used as a top‑level component; not inside overflow containers.

**Limitations**:  
- No animations on mount/unmount (uses transition classes but depends on `open` toggling; no `onEnter/onExit` hooks).
- Focus trap may be aggressive (prevents focus leaving even if content is interactive).

**Extension Rules**:  
- New placements can be added.

**Notes**:  
- The drawer panel uses `transform: none` to prevent initial offset; CSS transitions are applied.

---

#### EmptyState

**Name**: `EmptyState`  
**Purpose**: A component displayed when no data is available.  
**Import Path**: `@/shared/design-system/composites/EmptyState`

**Props**:

| Prop | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `title` | `ReactNode` | Yes | – | Main title. |
| `description` | `ReactNode` | No | – | Optional description. |
| `icon` | `ReactNode` | No | – | Icon to display. |
| `illustration` | `ReactNode` | No | – | Illustration (replaces icon if both provided? Both shown). |
| `primaryAction` | `{ label: string; onClick: () => void }` | No | – | Primary action button. |
| `secondaryAction` | `{ label: string; onClick: () => void }` | No | – | Secondary action button (outline variant). |
| `className` | `string` | No | – | Additional classes. |

**ForwardRef**: No.

**Accessibility**:  
- Uses `Button` components which are accessible.

**Composition Rules**:  
- Can be used inside `Card`, `Table`, etc.

**Limitations**:  
- Only two actions supported.

**Extension Rules**:  
- Could be extended with more actions.

**Notes**:  
- Uses `Button` primitives internally.

---

#### Modal

**Name**: `Modal`  
**Purpose**: A centered dialog with overlay, focus trap, and keyboard support.  
**Import Path**: `@/shared/design-system/composites/Modal`

**Props**:

| Prop | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `open` | `boolean` | Yes | – | Controls visibility. |
| `onClose` | `() => void` | Yes | – | Called when overlay is clicked or Escape is pressed. |
| `children` | `ReactNode` | Yes | – | Modal content. |
| `className` | `string` | No | – | Additional classes for modal panel. |
| `overlayClassName` | `string` | No | – | Additional classes for overlay. |

**ForwardRef**: Yes (ref forwarded to the outer `div` (the portal container)).

**Subcomponents**:  
- `ModalHeader`, `ModalBody`, `ModalFooter` – simple div wrappers with appropriate padding/borders.

**Accessibility**:  
- Portaled to `document.body`.
- `role="dialog"`, `aria-modal="true"`.
- Focus trap: when open, focus moves to modal; clicking outside or focusing outside refocuses modal.
- `Escape` key closes modal.
- Overlay click triggers `onClose`.

**Controlled/Uncontrolled**: Controlled via `open`.

**Composition Rules**:  
- Subcomponents are optional but recommended for consistency.

**Limitations**:  
- Similar focus trap issues as Drawer.

**Extension Rules**:  
- None.

**Notes**:  
- Uses `createPortal`.

---

#### Skeleton

**Name**: `Skeleton`  
**Purpose**: A loading placeholder with pulse animation.  
**Import Path**: `@/shared/design-system/composites/Skeleton`

**Props** (extends `HTMLAttributes<HTMLDivElement>`):

| Prop | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `variant` | `'text' \| 'circle' \| 'rect' \| 'avatar' \| 'button'` | No | `'text'` | Shape and size of the placeholder. |

**ForwardRef**: Yes (ref forwarded to `div`).

**Accessibility**:  
- No ARIA; should be hidden from screen readers using `aria-hidden` when used in loading contexts.

**Composition Rules**:  
- Used inside `MetricCard`, `TableBody` (loading state), etc.

**Limitations**:  
- No custom sizing except via variant.

**Extension Rules**:  
- New variants can be added.

**Notes**:  
- Uses `animate-pulse` class.

---

#### Table

**Name**: `Table` (and subcomponents)  
**Purpose**: A composable table with sticky header, loading, empty state, and row selection.  
**Import Path**: `@/shared/design-system/composites/Table`

**Table Props** (extends `TableHTMLAttributes<HTMLTableElement>`):

| Prop | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `children` | `ReactNode` | Yes | – | Table content. |
| `stickyHeader` | `boolean` | No | `true` | Whether the header should be sticky. |

**ForwardRef**: Yes (ref forwarded to `table`).

**Subcomponents**:

- **TableHeader** (ref `thead`): Props: `children`, `className`.
- **TableBody** (ref `tbody`): Additional props:
  - `loading`: `boolean` – shows skeleton rows.
  - `empty`: `boolean` – shows empty message.
  - `emptyMessage`: `ReactNode` – custom empty message.
  - `loadingRows`: `number` – number of skeleton rows (default 5).
- **TableRow** (ref `tr`): Additional props:
  - `selected`: `boolean` – applies a selected background.
- **TableHead** (ref `th`): Props: `children`, `className`.
- **TableCell** (ref `td`): Props: `children`, `className`.

**Accessibility**:  
- Uses semantic table elements.

**Composition Rules**:  
- Should be structured with `thead` and `tbody` sections.
- `TableBody` can be used with `loading` or `empty` states.

**Limitations**:  
- No column definitions or sorting.

**Extension Rules**:  
- Could be extended with sorting, filtering, but not implemented.

**Notes**:  
- The table wrapper adds `overflow-auto` and relative positioning.

---

#### Tabs

**Name**: `Tabs` (and subcomponents)  
**Purpose**: Tab component with keyboard navigation and ARIA support.  
**Import Path**: `@/shared/design-system/composites/Tabs`

**Tabs Props**:

| Prop | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `defaultValue` | `string` | No | – | Uncontrolled initial active tab value. |
| `value` | `string` | No | – | Controlled active tab value. |
| `onValueChange` | `(value: string) => void` | No | – | Callback when tab changes. |
| `children` | `ReactNode` | Yes | – | Should include `TabsList` and `TabPanel`s. |
| `className` | `string` | No | – | Additional classes. |

**Subcomponents**:

- **TabsList**: Props: `children`, `className`. (ref `div` with `role="tablist"`).
- **Tab**: Props:
  - `value`: `string` (required)
  - `disabled`: `boolean` (optional)
  - `children`: `ReactNode`
  - `className`? (extends button attributes)
  - Ref forwarded to `button`.
- **TabPanel**: Props:
  - `value`: `string` (required)
  - `children`: `ReactNode`
  - `className`? (extends div attributes)
  - Renders only when active.

**Hooks**: `useTabs` – returns the context (activeValue, onValueChange).

**Accessibility**:  
- `role="tablist"`, `role="tab"`, `role="tabpanel"`.
- `aria-selected`, `aria-disabled`.
- Keyboard navigation: not explicitly implemented; but buttons are focusable and can be navigated with arrow keys if consumers add handlers (but the current implementation does not). Actually, the code does not include arrow key handling; only click. So keyboard navigation is limited to Tab focusing on the button.

**Controlled/Uncontrolled**: Supports both via `value`/`onValueChange` or `defaultValue`.

**Composition Rules**:  
- `Tabs` provides context; `TabsList` and `TabPanel` must be children.
- `Tab` must be inside `TabsList`.

**Limitations**:  
- No arrow key navigation; only click and focus.

**Extension Rules**:  
- Could be extended with keyboard navigation.

**Notes**:  
- The `useTabs` hook is exported for advanced use.

---

### 4.3 Patterns

#### AIInsightCard

**Name**: `AIInsightCard`  
**Purpose**: A card to display AI‑generated insights with confidence and actions.  
**Import Path**: `@/shared/design-system/patterns/AIInsightCard`

**Props**:

| Prop | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `title` | `ReactNode` | No | – | Optional title. |
| `content` | `ReactNode` | Yes | – | Main content (insight text). |
| `confidence` | `number` | No | – | Confidence percentage (0–100). |
| `statusBadge` | `{ label: string; variant?: BadgeVariant }` | No | – | Badge to show status. |
| `actions` | `ReactNode` | No | – | Action buttons or elements. |
| `className` | `string` | No | – | Additional classes. |

**ForwardRef**: Yes (ref forwarded to `Card`).

**Composition Rules**:  
- Composes `Card`, `CardContent`, `CardFooter`, `Badge`, `Icon`.

**Limitations**:  
- Confidence is just a number displayed as text; no visual indicator.

**Extension Rules**:  
- Could be extended with more AI‑specific features.

**Notes**:  
- Uses CSS classes `border-ai-border`, `bg-ai-background`, `text-ai-accent` for styling.

---

#### CommandPalette

**Name**: `CommandPalette`  
**Purpose**: A global command palette with search and keyboard navigation.  
**Import Path**: `@/shared/design-system/patterns/CommandPalette`

**Props**:

| Prop | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `open` | `boolean` | Yes | – | Controls visibility. |
| `onClose` | `() => void` | Yes | – | Called when closing (Escape, selection, outside click). |
| `commands` | `Command[]` ( `{ id: string; label: ReactNode; shortcut?: string; icon?: ReactNode; onSelect: () => void }` ) | Yes | – | List of commands. |
| `placeholder` | `string` | No | `'Search commands...'` | Input placeholder. |
| `emptyMessage` | `ReactNode` | No | `'No commands found.'` | Message when no results. |

**ForwardRef**: Yes (ref forwarded to `Modal`).

**Composition Rules**:  
- Composes `Modal`, `ModalBody`, `Input`, `Icon`, `Badge`.

**Accessibility**:  
- Uses `Modal` for focus trap and overlay.
- Keyboard: ArrowUp/Down, Enter, Escape.
- Search input auto‑focuses on open.

**Limitations**:  
- Command filtering is simple string match; no fuzzy search.
- No command grouping.

**Extension Rules**:  
- Could be extended with categories.

**Notes**:  
- The `commands` label is used for filtering; only if it's a string.

---

#### FilterBar

**Name**: `FilterBar`  
**Purpose**: A bar with search, filters, and select dropdown.  
**Import Path**: `@/shared/design-system/patterns/FilterBar`

**Props** (extends `HTMLAttributes<HTMLDivElement>`):

| Prop | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `searchValue` | `string` | No | – | Controlled search input value. |
| `onSearchChange` | `(value: string) => void` | No | – | Called when search input changes. |
| `onSearch` | `(value: string) => void` | No | – | Called when Enter is pressed in search. |
| `searchPlaceholder` | `string` | No | `'Search...'` | Placeholder for search. |
| `filters` | `Filter[]` ( `{ id: string; label: string; value: string; onRemove?: () => void }` ) | No | `[]` | Active filters displayed as badges. |
| `onClearFilters` | `() => void` | No | – | Called when "Clear all" is clicked. |
| `selectOptions` | `SelectOption[]` | No | – | Options for the select dropdown. |
| `selectValue` | `string` | No | – | Controlled select value. |
| `onSelectChange` | `(value: string) => void` | No | – | Called when select changes. |
| `selectPlaceholder` | `string` | No | `'Filter by...'` | Placeholder for select. |
| `children` | `ReactNode` | No | – | Additional elements rendered on the right (e.g., buttons). |

**ForwardRef**: Yes (ref forwarded to `div`).

**Composition Rules**:  
- Composes `SearchBar`, `Select`, `Badge`, `Button`, `Icon`.

**Limitations**:  
- Only one select dropdown.

**Extension Rules**:  
- Could be extended with more filter types.

**Notes**:  
- The filters are displayed as badges with an optional remove button.

---

#### FormSection

**Name**: `FormSection`  
**Purpose**: A section with title, description, and grid layout for form fields.  
**Import Path**: `@/shared/design-system/patterns/FormSection`

**Props** (extends `HTMLAttributes<HTMLDivElement>` with `title` override):

| Prop | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `title` | `ReactNode` | Yes | – | Section title. |
| `description` | `ReactNode` | No | – | Optional description. |
| `children` | `ReactNode` | Yes | – | Form fields. |
| `columns` | `1 \| 2 \| 3` | No | `1` | Number of columns in the grid. |

**ForwardRef**: Yes (ref forwarded to `div`).

**Composition Rules**:  
- Used to structure forms.

**Limitations**:  
- No custom gap control.

**Extension Rules**:  
- Could be extended with more column options.

**Notes**:  
- Uses responsive grid classes (`md:grid-cols-2`, etc.).

---

#### MetricCard

**Name**: `MetricCard`  
**Purpose**: A card displaying a key metric with value, trend, and optional badge.  
**Import Path**: `@/shared/design-system/patterns/MetricCard`

**Props**:

| Prop | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `title` | `ReactNode` | Yes | – | Metric label. |
| `value` | `ReactNode` | Yes | – | Metric value. |
| `trend` | `number` | No | – | Percentage change (positive/negative). |
| `badge` | `{ label: string; variant?: BadgeVariant }` | No | – | Optional badge. |
| `icon` | `ReactNode` | No | – | Optional icon next to title. |
| `footer` | `ReactNode` | No | – | Optional footer content. |
| `loading` | `boolean` | No | `false` | Shows skeleton placeholders. |
| `className` | `string` | No | – | Additional classes. |

**ForwardRef**: Yes (ref forwarded to `Card`).

**Composition Rules**:  
- Composes `Card`, `CardContent`, `CardFooter`, `Badge`, `Icon`, `Skeleton`.

**Limitations**:  
- Trend icon uses a simple up/down arrow based on sign.

**Extension Rules**:  
- Could be extended with additional metric visualization.

**Notes**:  
- When `loading`, renders skeletons.

---

#### PageHeader

**Name**: `PageHeader`  
**Purpose**: A consistent page header with slots for breadcrumb, title, subtitle, search, and actions.  
**Import Path**: `@/shared/design-system/patterns/PageHeader`

**Props** (extends `HTMLAttributes<HTMLElement>` with `title` override):

| Prop | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `breadcrumb` | `ReactNode` | No | – | Breadcrumb navigation. |
| `title` | `ReactNode` | Yes | – | Main title (can be string for automatic h1). |
| `subtitle` | `ReactNode` | No | – | Subtitle or description. |
| `search` | `ReactNode` | No | – | Search bar component. |
| `actions` | `ReactNode` | No | – | Action buttons. |

**ForwardRef**: Yes (ref forwarded to `header`).

**Composition Rules**:  
- Typically placed at the top of a page.

**Limitations**:  
- Title is wrapped in `h1` if string; otherwise, rendered as a div.

**Extension Rules**:  
- Could be extended with more slots.

**Notes**:  
- Uses flex layout with wrapping.

---

#### SearchBar

**Name**: `SearchBar`  
**Purpose**: A search input with clear action and keyboard support.  
**Import Path**: `@/shared/design-system/patterns/SearchBar`

**Props** (extends `InputHTMLAttributes<HTMLInputElement>` with `onChange` override):

| Prop | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `value` | `string` | No | – | Controlled value. |
| `defaultValue` | `string` | No | – | Uncontrolled initial value. |
| `onChange` | `(value: string) => void` | No | – | Called when input changes. |
| `onSearch` | `(value: string) => void` | No | – | Called when Enter is pressed. |
| `placeholder` | `string` | No | `'Search...'` | Placeholder text. |
| *other input props* | – | No | – | Standard input props. |

**ForwardRef**: Yes (ref forwarded to `input`).

**Accessibility**:  
- Clear button has `aria-label="Clear search"`.

**Controlled/Uncontrolled**: Supports both via `value` or `defaultValue`.

**Composition Rules**:  
- Used in `FilterBar`, `PageHeader`.

**Limitations**:  
- No debouncing.

**Extension Rules**:  
- Could be extended with debouncing.

**Notes**:  
- Uses `Icon` for search icon and close icon.

---

## 5 Props Reference

This section lists all public interfaces and their properties. For each, the type, default, and whether required/optional are provided.

*(Due to length, we provide a summary; the detailed props are covered per component above.)*

**BreadcrumbItem**  
- `label: ReactNode` (required)  
- `href?: string`  
- `icon?: ReactNode`  
- `isCurrent?: boolean`

**SelectOption**  
- `value: string` (required)  
- `label: string` (required)

**Filter**  
- `id: string` (required)  
- `label: string` (required)  
- `value: string` (required)  
- `onRemove?: () => void`

**Command**  
- `id: string` (required)  
- `label: ReactNode` (required)  
- `shortcut?: string`  
- `icon?: ReactNode`  
- `onSelect: () => void` (required)

**ThemeContextValue**  
- `mode: ThemeVariant`  
- `toggleTheme: () => void`  
- `setTheme: (mode: ThemeVariant) => void`

---

## 6 Variants

| Component | Variants |
|-----------|----------|
| `Badge` | `primary`, `secondary`, `success`, `warning`, `error`, `outline`, `ghost` |
| `Button` | `primary`, `secondary`, `success`, `warning`, `error`, `outline`, `ghost` |
| `Card` | `default`, `elevated`, `outline` |
| `Skeleton` | `text`, `circle`, `rect`, `avatar`, `button` |
| `Tooltip` | `top`, `bottom`, `left`, `right` (placement) |

---

## 7 Sizes

| Component | Sizes |
|-----------|-------|
| `Avatar` | `sm`, `md`, `lg`, `xl` |
| `Badge` | `sm`, `md` |
| `Button` | `sm`, `md`, `lg` |
| `Icon` | `xs`, `sm`, `md`, `lg`, `xl` |

---

## 8 Accessibility

The following accessibility features are implemented across the Design System:

### ARIA Roles & Attributes
- **Modal / Drawer**: `role="dialog"`, `aria-modal="true"`.
- **Tabs**: `role="tablist"`, `role="tab"`, `role="tabpanel"`, `aria-selected`, `aria-disabled`.
- **Switch**: `role="switch"`, `aria-checked`.
- **Breadcrumb**: `aria-label="Breadcrumb"` on nav, `aria-current="page"` on current item.
- **Select**: `role="listbox"`, `role="option"`, `aria-haspopup`, `aria-expanded`, `aria-disabled`.
- **Tooltip**: `role="tooltip"`.

### Keyboard Support
- **Modal / Drawer**: `Escape` closes; focus trap maintains focus inside.
- **Select**: ArrowUp/Down to navigate options, Enter to select, Escape to close.
- **CommandPalette**: ArrowUp/Down, Enter, Escape.
- **Button**: Focusable via Tab, Enter/Space activates (native).
- **SearchBar**: Enter triggers `onSearch`.

### Focus Management
- **Modal / Drawer**: On open, focus moves to the container; on close, focus returns to previous element.
- **Tabs**: Focus is managed via `tabIndex` (only active tab is focusable).
- **CommandPalette**: Input auto‑focuses on open.

### Screen Reader Support
- **Input / Textarea**: Uses `aria-describedby` linking helper/error/counter text.
- **Button**: Uses `aria-disabled` and `aria-busy` for loading states.
- **Checkbox**: Native, supports indeterminate.
- **Switch**: Uses `aria-checked`.

### Visual Indicators
- Focus rings are provided on focusable elements (via `focus-visible`).
- Error states are visually indicated (red border) and linked via `aria-invalid`.

---

## 9 Composition Rules

The Design System encourages composition via nesting and prop drilling. Below are typical compositions from the source code.

### Card Composition
```tsx
<Card variant="elevated">
  <CardHeader>
    <CardTitle>Title</CardTitle>
    <CardDescription>Description</CardDescription>
  </CardHeader>
  <CardContent>Content</CardContent>
  <CardFooter>Footer</CardFooter>
</Card>
```

### Table Composition
```tsx
<Table stickyHeader>
  <TableHeader>
    <TableRow>
      <TableHead>Header 1</TableHead>
      <TableHead>Header 2</TableHead>
    </TableRow>
  </TableHeader>
  <TableBody loading={isLoading} empty={!data.length} emptyMessage="No data">
    {data.map(row => (
      <TableRow key={row.id}>
        <TableCell>{row.field1}</TableCell>
        <TableCell>{row.field2}</TableCell>
      </TableRow>
    ))}
  </TableBody>
</Table>
```

### Tabs Composition
```tsx
<Tabs defaultValue="tab1" onValueChange={handleChange}>
  <TabsList>
    <Tab value="tab1">Tab 1</Tab>
    <Tab value="tab2">Tab 2</Tab>
  </TabsList>
  <TabPanel value="tab1">Content 1</TabPanel>
  <TabPanel value="tab2">Content 2</TabPanel>
</Tabs>
```

### Modal Composition
```tsx
<Modal open={isOpen} onClose={closeModal}>
  <ModalHeader>Header</ModalHeader>
  <ModalBody>Body</ModalBody>
  <ModalFooter>
    <Button onClick={closeModal}>Close</Button>
  </ModalFooter>
</Modal>
```

### MetricCard Composition (internal)
- Uses `Card`, `CardContent`, `CardFooter`, `Badge`, `Icon`, `Skeleton`.

### AIInsightCard Composition
- Uses `Card`, `CardContent`, `CardFooter`, `Badge`, `Icon`.

### FilterBar Composition
- Uses `SearchBar`, `Select`, `Badge`, `Button`, `Icon`.

### PageHeader Composition
- Expects `Breadcrumb` in `breadcrumb`, `SearchBar` in `search`, `Button`s in `actions`.

### CommandPalette Composition
- Uses `Modal`, `ModalBody`, `Input`, `Icon`, `Badge`.

---

## 10 Design Tokens

All tokens are exported from `@/shared/design-system/tokens`.

### Colors
Full palette is defined in `colors.ts`, including:
- `brand.primary`, `brand.secondary` (50–950)
- `neutral` (50–950)
- `semantic.success`, `semantic.warning`, `semantic.error`, `semantic.info` (50–950)
- `surface` (background, surface, elevated, card, sidebar, drawer, overlay, raised)
- `border` (subtle, strong, inverse, focus, error)
- `text` (primary, secondary, tertiary, inverse, disabled, link)
- `chart` (1–10)
- `risk` (low, mediumLow, medium, mediumHigh, high)
- `loan` (draft, review, approved, disbursed, delinquent, rejected, partial)
- `ai` (accent, accentHover, background, border, processing)
- `interaction` (hover, active, disabled, focus)

### Typography
- `fontFamily.sans`, `fontFamily.mono`
- `fontSize.xs` through `fontSize.7xl`
- `lineHeight.none` through `lineHeight.loose`
- `fontWeight.thin` through `fontWeight.black`
- `letterSpacing.tighter` through `letterSpacing.widest`

### Spacing
- `0` to `64` (4‑px steps)

### Radius
- `none`, `sm`, `base`, `md`, `lg`, `xl`, `2xl`, `3xl`, `full`

### Shadows
- `xs`, `sm`, `base`, `md`, `lg`, `xl`, `2xl`, `inner`

### Motion
- `duration.instant` through `duration.slowest`
- `easing.linear`, `easing.in`, `easing.out`, `easing.inOut`, `easing.spring`

### Z‑Index
- `base`, `dropdown`, `sticky`, `overlay`, `drawer`, `modal`, `popover`, `toast`, `tooltip`, `topmost`

### Breakpoints
- `sm`, `md`, `lg`, `xl`, `2xl` (in px)

---

## 11 Hooks

### useTheme
**Import**: `@/shared/design-system/hooks/useTheme`

**Returns**: `ThemeContextValue` (`{ mode, toggleTheme, setTheme }`)

**Restrictions**: Must be used within a `ThemeProvider`.

**Description**: Provides access to the current theme mode and controls to change it.

---

## 12 Providers

### ThemeProvider
**Import**: `@/shared/design-system/providers/ThemeProvider`

**Props**: `children` (ReactNode)

**Behavior**:
- On mount, reads `localStorage` for stored theme (`creditbridge-theme`), defaults to `'light'`.
- Applies CSS custom properties to `document.documentElement` based on `lightTheme` or `darkTheme`.
- Persists theme choice in `localStorage`.
- Adds `data-theme="dark"` attribute to root when dark mode is active (for Tailwind dark mode).
- Provides `ThemeContext` to children.

**Usage**:
```tsx
<ThemeProvider>
  <App />
</ThemeProvider>
```

---

## 13 Utilities

### cn
**Import**: `@/shared/design-system/utils/cn`

**Signature**: `cn(...inputs: ClassValue[]): string`

**Description**: Merges class names using `clsx` and `twMerge` to handle Tailwind class conflicts.

**Usage**:
```tsx
<div className={cn('base-class', isActive && 'active', className)} />
```

---

## 14 Dependency Graph

```
Pages (Not implemented)
  └── Feature Components (Not implemented)
        └── Patterns
              ├── AIInsightCard
              │     ├── Card (Composite)
              │     ├── Badge (Primitive)
              │     └── Icon (Primitive)
              ├── CommandPalette
              │     ├── Modal (Composite)
              │     ├── Input (Primitive)
              │     ├── Icon (Primitive)
              │     └── Badge (Primitive)
              ├── FilterBar
              │     ├── SearchBar (Pattern)
              │     ├── Select (Primitive)
              │     ├── Badge (Primitive)
              │     └── Button (Primitive)
              ├── FormSection
              │     └── (uses spacing/grid)
              ├── MetricCard
              │     ├── Card (Composite)
              │     ├── Badge (Primitive)
              │     ├── Icon (Primitive)
              │     └── Skeleton (Composite)
              ├── PageHeader
              │     └── (expects Breadcrumb, SearchBar, Buttons)
              └── SearchBar
                    ├── Input (Primitive)
                    └── Icon (Primitive)

Composites
  ├── Breadcrumb
  │     └── (uses cn)
  ├── Card
  │     └── (uses cn)
  ├── Drawer
  │     └── (uses cn, createPortal)
  ├── EmptyState
  │     └── Button (Primitive)
  ├── Modal
  │     └── (uses cn, createPortal)
  ├── Skeleton
  │     └── (uses cn)
  ├── Table
  │     └── (uses cn)
  └── Tabs
        └── (uses cn, createContext, useState, useCallback)

Primitives
  ├── Avatar
  ├── Badge
  ├── Button
  ├── Checkbox
  ├── Icon
  ├── Input
  ├── Radio
  ├── Select
  ├── Switch
  ├── Textarea
  └── Tooltip

All primitives use `cn` and may use tokens via CSS classes.

Utilities: cn (depends on clsx, tailwind-merge)

Providers: ThemeProvider (depends on useTheme, lightTheme, darkTheme)

Hooks: useTheme (depends on ThemeContext)

Tokens: standalone, no dependencies.

Theme: depends on tokens (colors)
```

---

## 15 Extension Rules

Based on the existing architecture, the following rules guide how components should be extended or created.

### When to create a new Primitive
- When a new atomic UI element is needed that does not rely on other components.
- It must be minimal, style‑agnostic, and support accessibility.
- It should accept `className` and forward refs.
- Example: a new input type like `Range`.

### When to create a new Composite
- When multiple primitives are combined to form a reusable UI block.
- It should provide a cohesive API and manage state where necessary.
- Example: a `Pagination` composite.

### When to create a new Pattern
- When a composite is specialised for a specific business use case.
- It may incorporate logic, data fetching, or domain semantics.
- Example: a `CreditScoreCard` pattern.

### Extension of existing components
- New variants or sizes can be added by extending the relevant union types and updating the class maps.
- New props should follow the existing naming conventions (e.g., `isLoading`, `onXChange`).
- Components with forwardRef should continue to forward refs.

### Prohibited
- Do not modify existing component APIs in a breaking way.
- Do not remove existing variants or sizes.
- Do not change default values without a deprecation process.

---

## 16 Forbidden Assumptions

The following APIs or features are **not present** in the current implementation. Any assumption that they exist is incorrect and must not be used.

- **DataGrid** – no full‑featured data grid with sorting, filtering, or pagination.
- **Table columns definition** – no `columns` prop, no `render` functions per column.
- **Pagination component** – no built‑in pagination.
- **Async Select** – no async loading of options.
- **Multi‑select** – no multi‑value select.
- **DatePicker** – no date picker.
- **TimePicker** – no time picker.
- **FileUpload** – no file input component.
- **ProgressBar** – no progress indicator.
- **Spinner** – no standalone spinner (Button has internal spinner).
- **Toast/Notification** – no toast system.
- **Popover** – no popover (only Tooltip).
- **Stepper** – no step wizard.
- **Slider** – no range slider.
- **Accordion** – no accordion.
- **DropdownMenu** – no dropdown menu (Select is limited).
- **ContextMenu** – no context menu.
- **Tree** – no tree view.
- **Virtualized lists** – no virtualization.
- **Charts** – no chart components (only color tokens).
- **Form validation** – no built‑in validation (only error display).
- **Router integration** – no Link component.
- **Animation hooks** – no useTransition or useSpring.
- **Theming beyond light/dark** – only light and dark modes.
- **CSS-in-JS** – uses Tailwind classes, not CSS-in-JS.
- **Server Components** – components are client‑side only.
- **Next.js specific** – no Next.js optimizations.

---

## 17 AI Development Rules

For AI agents generating code that consumes the Design System, the following rules must be followed:

1. **Never invent props** – only use props documented in this contract.
2. **Never invent variants** – only use listed variants.
3. **Never invent sizes** – only use listed sizes.
4. **Never skip the Feature Layer** – the Design System ends at Patterns. Feature components and Pages are application‑specific and must be built outside the Design System.
5. **Never modify Design System source code** – all changes should be extensions through composition or new components in the appropriate layer.
6. **Never create undocumented extension points** – if a new component is needed, it should follow the established patterns and be documented.
7. **Always import from the correct paths** – use the exact import paths as provided (e.g., `@/shared/design-system/primitives/Button`).
8. **Always use `cn` for merging classes** – never manually concatenate strings.
9. **Respect accessibility** – always use accessible patterns as demonstrated.
10. **Prefer composition** – build complex UIs by composing existing components rather than creating new monolithic components.
11. **Use controlled components** – for stateful components (Select, Switch, Tabs, Input), prefer controlled mode with `value`/`onChange` unless appropriate for uncontrolled.

---

*This document is a faithful representation of the CreditBridge Design System as of the date of creation. Any deviation from this contract is subject to architectural review.*