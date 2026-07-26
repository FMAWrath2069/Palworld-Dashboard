# Security Policy

## Supported Versions

Security updates are provided for the latest version available on the `main` branch.

Older releases may not receive security fixes.

---

## Reporting a Vulnerability

If you discover a security vulnerability, please **do not** open a public GitHub Issue.

Instead, report the vulnerability privately by contacting the project maintainer.

When reporting a vulnerability, please include:

* A description of the issue
* Steps to reproduce the problem
* Potential impact
* Any proof-of-concept code (if applicable)
* Suggested mitigation (optional)

Every report will be reviewed as quickly as possible.

---

## Response Process

Once a vulnerability has been reported:

1. The report will be acknowledged.
2. The issue will be investigated.
3. A fix will be developed and tested.
4. The fix will be released.
5. Public disclosure may occur after a fix is available.

---

## Scope

This project primarily consists of:

* Flask web application
* REST API
* SSH tunnel management
* Palworld server administration
* Local configuration and data storage

Potential security issues include, but are not limited to:

* Authentication bypass
* Remote code execution
* Command injection
* Path traversal
* Cross-site scripting (XSS)
* Cross-site request forgery (CSRF)
* Privilege escalation
* Sensitive information disclosure
* Improper access control
* SSH tunnel vulnerabilities
* Dependency vulnerabilities

---

## Out of Scope

The following are generally considered out of scope:

* Vulnerabilities in third-party software (Flask, Requests, Python, etc.)
* Issues requiring physical access to the machine
* Denial-of-service attacks requiring unrealistic resources
* Vulnerabilities caused solely by unsupported operating systems
* Social engineering attacks

---

## Security Best Practices

When deploying Palworld Dashboard:

* Keep Python and all dependencies up to date.
* Keep the operating system updated with security patches.
* Restrict dashboard access using a firewall or reverse proxy.
* Use strong administrator passwords.
* Protect SSH private keys with appropriate filesystem permissions.
* Avoid exposing the dashboard directly to the public Internet unless appropriate authentication and transport security are in place.
* Use HTTPS when the dashboard is accessible over a network.
* Regularly back up configuration and server data.

---

## Responsible Disclosure

Please allow reasonable time for a fix before publicly disclosing any vulnerability.

Responsible disclosure helps protect users while security updates are prepared and released.

---

## Acknowledgements

Contributors who responsibly disclose valid security vulnerabilities may be acknowledged in the project's release notes or documentation, unless they prefer to remain anonymous.
