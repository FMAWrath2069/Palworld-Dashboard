# Contributor Guidelines

Thank you for your interest in contributing to Palworld Dashboard.

Contributions of all sizes are welcome, including bug fixes, documentation improvements, performance enhancements, and new features.

## Before You Begin

* Search existing Issues before creating a new one.
* If you're planning a large feature, open an Issue first to discuss the design.
* Keep pull requests focused on a single feature or bug fix whenever possible.

## Reporting Bugs

When reporting a bug, please include:

* Dashboard version or commit hash
* Operating system
* Python version
* Steps to reproduce the issue
* Expected behavior
* Actual behavior
* Screenshots or logs (if applicable)

## Feature Requests

Feature requests should include:

* The problem you're trying to solve
* Your proposed solution
* Any alternatives you've considered

## Pull Requests

Before submitting a pull request:

* Verify the project runs without errors.
* Ensure new code follows the project's coding standards.
* Remove debugging statements before submitting.
* Update documentation when appropriate.
* Keep commits clean and descriptive.

## Commit Messages

Use concise commit messages such as:

* Add SSH tunnel auto-reconnect
* Fix player refresh race condition
* Refactor polling service
* Improve server status handling

## Branch Naming

Examples:

* feature/server-status
* feature/log-viewer
* bugfix/polling-thread
* refactor/api-service
* docs/readme-update

## Code Reviews

Please be receptive to feedback. Code reviews are intended to improve code quality and maintain consistency throughout the project.

## Questions

If you're unsure about a change, open a GitHub Discussion or Issue before beginning implementation.
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
