# CreditBridge Product and Design Direction

**Purpose:** Give product and engineering contributors a quick entry point to the existing design system and the main user experiences.

## Product experience

CreditBridge serves two distinct user groups: MSMEs managing their business and credit profile, and lenders reviewing businesses and portfolio risk. The ERP modules support operational work; the credit-intelligence experience should make financial evidence and scoring understandable. Keep the two experiences consistent in the product identity while using workflows and information density appropriate to each audience.

### MSME experience

- Make business setup, data connection/upload, and record keeping clear.
- Show credit score together with grade, input coverage, score factors, flags, and next steps.
- Explain why a requested permission is needed before the user grants consent.
- Make incomplete, delayed, or unavailable data visible.

### Lender experience

- Make pool filtering and risk segmentation quick to scan.
- Show the evidence behind a score on business detail views.
- Distinguish a risk indicator from a final lending decision.
- Support review outcomes and portfolio monitoring with clear status and timestamps.

### ERP experience

- Organize navigation by business module and domain.
- Put frequently used work first, with less common domains discoverable through a complete module view.
- Keep list, create, detail, and edit workflows predictable across domains.

## Existing design-system source of truth

The detailed system lives in `doc/engineering/design/` and its implementation rules in `doc/engineering/01_DESIGN_SYSTEM_IMPLEMENTATION_GUIDE.md`.

- [Product experience principles](doc/engineering/design/01_PRODUCT_EXPERIENCE_PRINCIPLES.md)
- [Color system](doc/engineering/design/02_COLOR_SYSTEM.md)
- [Typography system](doc/engineering/design/03_TYPOGRAPHY_SYSTEM.md)
- [Spacing system](doc/engineering/design/04_SPACING_SYSTEM.md)
- [Layout grid](doc/engineering/design/05_LAYOUT_GRID_SYSTEM.md)
- [Motion system](doc/engineering/design/06_MOTION_SYSTEM.md)
- [Component guidelines](doc/engineering/design/07_COMPONENT_GUIDELINES.md)
- [Token architecture](doc/engineering/design/08_TOKEN_ARCHITECTURE.md)
- [Design-system API contract](doc/DESIGN_SYSTEM_API_CONTRACT.md)

Use the existing tokens and component rules as the source of truth. This file does not replace their numeric specifications or component APIs.

## Design requirements for new work

- Follow the established color, type, spacing, layout, and motion tokens.
- Design loading, empty, error, success, and permission states—not only the ideal populated screen.
- Use plain language for financial terms and provide explanations for scores and risk signals.
- Keep forms accessible, keyboard usable, and clear about required versus optional information.
- Avoid adding a new visual pattern when a documented component or pattern already serves the need.
- Update the relevant design-system docs when a shared token or component contract changes.
