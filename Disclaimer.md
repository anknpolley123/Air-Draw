# Disclaimer — Air Draw

**Last updated:** 1 November 2026

Please read this disclaimer before installing, running, modifying, or redistributing Air Draw.

## 1. Educational and demonstration software

Air Draw is a webcam-based hand-gesture drawing application provided for learning, experimentation, accessibility exploration, and personal creative use. It is provided as a software project, not as a certified product or a guarantee of secure service.

## 2. Camera, image, and data handling

- The browser requests access to the user's camera.
- Camera frames are transmitted from the browser to the server for hand tracking. Only run the application with a server you trust and tell users clearly when their camera frames are being transmitted.
- Saved drawings and account records are stored in the local SQLite database created by the application. Anyone who gains access to that database or the host may be able to access its contents.
- If a user configures Gemini analysis, the drawing image is sent to Google's Gemini service for processing. The user is responsible for reviewing Google's current privacy terms, service terms, and data-handling settings before sending any image.
- Do not submit confidential, sensitive, or identifying images unless you have permission and understand how they will be processed and stored.

## 3. Security limitations

This repository is not represented as production-ready or independently security-audited. The code currently includes a predictable fallback Flask secret key and permissive Socket.IO cross-origin configuration. These settings should be reviewed and corrected before any network-facing deployment. Other application, dependency, authentication, session, rate-limit, transport-security, and data-retention risks may also exist.

Setting a secret key or running the application inside Docker does not by itself make the application secure. Do not expose a development instance to the public internet. If you operate a hosted instance, you are responsible for its configuration, access controls, HTTPS, monitoring, backups, updates, and incident response.

## 4. API keys and accounts

Users are responsible for keeping passwords and API keys confidential, using unique credentials, and removing exposed keys promptly. Never commit secrets to source control or include them in bug reports. The project author does not control third-party API availability, billing, quotas, model behavior, or provider policies.

## 5. Lawful and respectful use

Use the software only on devices, camera feeds, drawings, and data you own or are authorized to process. Respect privacy, consent, intellectual-property rights, and applicable laws. You are responsible for obtaining any permissions required for recording, transmitting, storing, or analyzing images.

## 6. Third-party software and services

Air Draw depends on third-party libraries and may integrate with external services, including Google Gemini. Those components and services are governed by their own licenses, terms, and privacy policies. Product names and trademarks belong to their respective owners. Mention of a third-party service does not imply sponsorship or endorsement.

## 7. No warranty

To the maximum extent permitted by applicable law, the software is provided **“AS IS” and “AS AVAILABLE,” without warranties of any kind**, whether express or implied, including warranties of merchantability, fitness for a particular purpose, title, non-infringement, availability, accuracy, or security.

The author does not guarantee uninterrupted operation, error-free behavior, preservation of saved data, compatibility with every device, or the accuracy of AI-generated analysis. AI output may be incomplete or incorrect and should not be treated as professional advice.

## 8. Limitation of liability

To the maximum extent permitted by applicable law, the author and contributors are not liable for indirect, incidental, special, consequential, exemplary, or punitive damages, data loss, service interruption, unauthorized access, API charges, or other losses arising from use of or inability to use the software. Nothing in this disclaimer excludes liability that cannot lawfully be excluded.

## 9. License and redistribution

The repository includes a GNU General Public License v3.0 license file. Review [LICENSE](LICENSE) and the applicable third-party licenses before copying, modifying, or redistributing the project. This disclaimer does not replace or modify the license.

## 10. Contact and reporting

For questions or responsible reports about this repository, open a [GitHub Issue](https://github.com/anknpolley123/Air-Draw/issues). Do not include passwords, API keys, private drawings, database files, or other sensitive data in public issues.

**Developer:** Ankon Polley  
**GitHub:** [@anknpolley123](https://github.com/anknpolley123)  
**Contact:** [ankonpolley@proton.me](mailto:ankonpolley@proton.me)

---

This document is informational and is not legal advice. Applicable legal rights and obligations depend on your jurisdiction and circumstances.
