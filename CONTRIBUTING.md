# Coding Standards

The goal of this project is to maintain a clean, readable, and modular codebase.

## General

* Favor readability over cleverness.
* Keep functions focused on a single responsibility.
* Avoid duplicated logic.
* Prefer descriptive names over abbreviations.
* Keep modules small and organized.

## Python

* Follow PEP 8 where practical.
* Use 4 spaces for indentation.
* Use `snake_case` for variables and functions.
* Use `PascalCase` for classes.
* Group imports as:

  1. Standard library
  2. Third-party packages
  3. Local project imports
* Prefer early returns over deeply nested conditionals.
* Catch only exceptions you expect.
* Do not expose internal exception messages to API clients.
* Use the project's logging facilities instead of `print()` for new code.

## JavaScript

* Use modern ES6+ syntax.
* Use `const` whenever a variable is not reassigned.
* Use `let` instead of `var`.
* Use `camelCase` for variables and functions.
* Use `PascalCase` for global modules attached to `window`.
* Always use braces for conditional statements.
* Prefer `async/await` over chained promises.
* Avoid deeply nested callbacks.

## HTML

* Use semantic HTML whenever possible.
* Keep indentation consistent.
* Avoid inline JavaScript.
* Prefer reusable components over duplicated markup.

## CSS

* Keep selectors specific but not overly complex.
* Reuse existing classes before creating new ones.
* Group related styles together.

## Flask

* Keep route handlers thin.
* Place business logic inside the `services` package.
* Keep application state inside the `core` package.
* Register new routes using Blueprints.

## Project Organization

* `core/` — shared application state and storage
* `routes/` — API endpoints
* `services/` — business logic
* `static/` — client-side assets
* `templates/` — HTML templates

## Documentation

* Add comments only where they improve understanding.
* Keep README documentation up to date.
* Document new configuration options.

## Performance

* Avoid unnecessary polling.
* Cache expensive operations where appropriate.
* Minimize duplicate API requests.
* Keep UI updates efficient.

## Security

* Never commit passwords, API keys, or SSH keys.
* Validate all user input.
* Return generic error messages to clients.
* Log detailed exceptions on the server.

## Formatting

Maintain consistent formatting throughout the project. Existing files should generally match the surrounding style rather than introducing a different formatting convention.
