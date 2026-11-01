# Disclaimer — Air Draw 🎨

**Project:** Air Draw  
**Developer:** Ankon Polley  
**Repository:** [anknpolley123/Air-Draw](https://github.com/anknpolley123/Air-Draw)

---

Please read this disclaimer before installing, running, modifying, or redistributing Air Draw.

## ⚠️ 1. Educational & Creative Purpose

Air Draw is a webcam-based hand-gesture drawing application intended for learning, experimentation, and personal creative use. It is provided as a software project and is not a certified product or a guarantee of secure service.

## 📷 2. Camera, Images & Data

- The browser requests access to the user's camera.
- Camera frames are transmitted from the browser to the server for hand tracking. Use only a server you trust and make this data flow clear to anyone using your instance.
- Saved drawings and account records are stored in the local SQLite database created by the application.
- When Gemini analysis is requested, the selected drawing image is sent to Google's Gemini service for processing.
- Do not submit confidential, sensitive, or identifying images unless you have permission and understand how they will be processed and stored.

## 🔐 3. Security Limitations

This repository has not been independently security-audited and is not represented as production-ready. The current code includes a predictable fallback Flask secret key and permissive Socket.IO cross-origin configuration. These settings require review before any network-facing deployment.

Other risks may exist in authentication, sessions, dependencies, data retention, request handling, and deployment configuration. Setting a secret key or using Docker does not automatically make the application secure.

Do not expose a development instance to the public internet. Anyone operating a hosted instance is responsible for its configuration, access controls, HTTPS, monitoring, backups, updates, and incident response.

## 🔑 4. API Keys & Accounts

Users are responsible for protecting passwords and API keys, using unique credentials, and removing exposed keys promptly. Never commit secrets to source control or include them in public bug reports.

The project author does not control third-party API availability, billing, quotas, model behavior, or provider policies.

## ⚖️ 5. Lawful & Respectful Use

Use the software only with devices, camera feeds, drawings, and data you own or are authorized to process. Respect privacy, consent, intellectual-property rights, and applicable laws.

You are responsible for obtaining any permissions required to record, transmit, store, or analyze images.

## 🌐 6. Third-Party Software & Services

Air Draw uses third-party libraries and may integrate with external services, including Google Gemini. Those components and services are governed by their own licenses, terms, and privacy policies.

Product names and trademarks belong to their respective owners. Mention of a third-party service does not imply sponsorship or endorsement.

## 🚫 7. No Warranty

To the maximum extent permitted by applicable law, the software is provided **“AS IS” and “AS AVAILABLE,” without warranties of any kind**, whether express or implied, including warranties of merchantability, fitness for a particular purpose, title, non-infringement, availability, accuracy, or security.

The author does not guarantee uninterrupted operation, error-free behavior, preservation of saved data, compatibility with every device, or the accuracy of AI-generated analysis. AI output may be incomplete or incorrect and should not be treated as professional advice.

## 🛡️ 8. Limitation of Liability

To the maximum extent permitted by applicable law, the author and contributors are not liable for indirect, incidental, special, consequential, exemplary, or punitive damages, data loss, service interruption, unauthorized access, API charges, or other losses arising from use of or inability to use the software.

Nothing in this disclaimer excludes liability that cannot lawfully be excluded.

## 📜 9. License & Redistribution

This repository includes a [GNU General Public License v3.0](LICENSE) file. Review the license and applicable third-party licenses before copying, modifying, or redistributing the project.

This disclaimer does not replace or modify the software license.

## 📧 10. Contact & Reporting

For questions or responsible reports, open a [GitHub Issue](https://github.com/anknpolley123/Air-Draw/issues).

Do not include passwords, API keys, private drawings, database files, or other sensitive information in public issues.

**Developer:** Ankon Polley  
**GitHub:** [@anknpolley123](https://github.com/anknpolley123)  
**Email:** [ankonpolley@proton.me](mailto:ankonpolley@proton.me)

---

<p align="center">
  <b>Air Draw — Ankon Polley</b>
  <br>
  Made with ❤️ by Ankon Polley
</p>

<sub>This document is informational and is not legal advice. Applicable rights and obligations depend on your jurisdiction and circumstances.</sub>
