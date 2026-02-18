# Hidden Gems — Architecture & Design

**FBLA 2026 | Byte-Sized Business Boost**

This document describes the modular, cross-platform architecture and design system used to deliver a production-ready desktop and web/mobile experience from a single codebase.

---

## 1. Design System (Single Source of Truth)

**Location:** `src/ui/design_system.py`

A centralized design system ensures consistent typography, color palettes, spacing, and layout tokens across:

- **Desktop (Tkinter/ttk)** — Applied via `src/ui/theme.py`, which configures ttk styles from these tokens.
- **Web** — Mirrored in `web/static/style.css` using CSS custom properties (variables) so the same palette and spacing drive the responsive UI.

**Tokens include:**

- **COLORS** — Background, surface, primary/secondary/danger, text hierarchy, table and input states.
- **TYPOGRAPHY / FONTS** — Title, heading, subheading, body, caption with family and size.
- **SPACING** — xs through xxl scale for padding and margins.
- **RADII** — Border radius for cards and buttons.
- **LAYOUT** — Content max width, min window size, row heights, input/button padding.

**Usage:** Import from `src.ui.design_system` in desktop code; keep `web/static/style.css` variables in sync for web.

---

## 2. Modular UI Components (Desktop)

**Location:** `src/ui/components/`

Reusable, themed building blocks used across windows:

- **layout** — `make_centered_content()`, `make_card_container()`, `make_centered_card()` for adaptive, fullscreen-friendly, and **card-based** layouts (elevated surface panel with subtle border).
- **buttons** — `PrimaryButton`, `SecondaryButton`, `DangerButton` (wrap ttk with consistent styles and a short **micro-interaction** delay so the pressed state is visible before the action runs).
- **labels** — `TitleLabel`, `HeadingLabel`, `SubheadingLabel`, `CaptionLabel` for typography hierarchy; **Card.*** variants for use on surface/card background.

All components rely on the design system and theme; no hard-coded colors or fonts in components.

---

## 3. Application State

**Location:** `src/state/app_state.py`

Centralized in-memory state for the desktop app:

- **User** — `set_user()`, `get_user()`, `clear_user()` for the current logged-in user.
- **Preferences** — `set_pref()`, `get_pref()` for optional UI settings (e.g. window geometry).

The web app uses Flask sessions for user state; business logic (auth, queries) is shared. State management is minimal and explicit to keep behavior predictable and testable.

---

## 4. Desktop Application (Tkinter)

- **Entry point:** `main.py` — Sets up path, calls `setup_theme()`, initializes DB and seed data, then launches the login flow.
- **Theme:** `src/ui/theme.py` — Applies the design system to ttk (clam theme), configures TFrame, TLabel, TButton variants, TEntry, TCombobox, Treeview, Separator, Scrollbar. Exposes `apply_window_bg()` for root/toplevel windows.
- **Screens:** Login (`login_window.py`), Main menu (`main_menu.py`), Directory and Business detail (`directory_window.py`), Favorites/Deals/Help/Recommendations/Trending/My Reviews (`screens.py`). Each uses the same design tokens and, where applicable, shared components and layout helpers.
- **Card-based layouts:** Main menu and login flows use `make_centered_card()` so content sits in an elevated surface panel (white card on gray background) for clear visual hierarchy.
- **Adaptive layout:** Centered content with a max width prevents over-stretching when the window is maximized; resizable windows with sensible minimum sizes from the design system.
- **Micro-interactions:** Buttons run their command after a brief delay so the pressed state is visible, giving smooth interaction feedback.

---

## 5. Web & Mobile (Flask + Responsive CSS)

- **Entry point:** `python -m web.app` (from project root). Serves the same SQLite database as the desktop app.
- **Backend:** `web/app.py` — Flask routes for login, register, directory, business detail, favorites, deals, trending, recommendations, help; session-based auth; parameterized queries via `src.database.queries`.
- **Templates:** Jinja2 base + page-specific templates; shared header/footer and flash messages.
- **Frontend:** Single `web/static/style.css` with design-system-aligned CSS variables, responsive breakpoints (e.g. tables stack on small screens), and focus-visible styles for keyboard users.
- **PWA-ready:** `web/static/manifest.json` with name, theme_color, background_color, display standalone. Optional: add icons and a service worker for offline later.
- **Accessibility:** Semantic HTML (header, main, nav, footer), ARIA where needed (e.g. aria-label on logo and menu button, role="main", role="navigation"), and focus management.

---

## 6. Data Layer & Security

- **Database:** SQLite via `src/database/db.py` (connection, schema, migrations). Path is project-root-relative so it works for both desktop and web when run from root.
- **Secure integration:** All SQL in `src/database/queries.py` uses **parameterized statements** only (e.g. `?` placeholders); no string concatenation of user input. This prevents SQL injection and aligns with secure database integration practices.
- **Auth:** `src/logic/auth.py` — Password hashing (salted), email/username validation, login and registration. Same logic for desktop and web; web uses Flask session to store user identity.

---

## 7. Cross-Platform Deployment

| Target        | How to run                          | Notes                                                |
|---------------|-------------------------------------|------------------------------------------------------|
| Desktop       | `python main.py`                    | Tkinter; design system via theme and components.    |
| Web (browser) | `python -m web.app` → http://127.0.0.1:5000 | Same DB; responsive layout.                  |
| Mobile        | Same URL on phone (same network) or deploy to a host | Responsive CSS + viewport; PWA manifest.   |

The same codebase serves desktop and web; only the UI layer differs (Tkinter vs HTML/CSS/JS). Business logic, database, and design tokens are shared.

---

## 8. Maintainability & Extensibility

- **Design changes** — Update `design_system.py` and theme; then sync CSS variables in `web/static/style.css` if needed.
- **New screens** — Add a window in `src/ui/` (or a new module) using components and layout helpers; add a route and template in `web/app.py` and `web/templates/` for web.
- **New features** — Add queries in `queries.py`, call from both desktop and web code paths.
- **State** — Extend `app_state.py` for new global UI or user preferences without scattering state across windows.

This structure supports scalability, consistent UX across platforms, and clear separation of concerns for long-term maintenance.
