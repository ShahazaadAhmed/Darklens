# DarkLens: Detection Engineering & SOC Investigation Platform

DarkLens is a hands-on cybersecurity portfolio project focused on security monitoring, detection engineering, threat hunting, and incident investigation. It combines an isolated Wazuh lab with Windows Sysmon telemetry and a Python-based investigation engine to demonstrate practical SOC workflows.

The project covers the detection lifecycle: collecting endpoint telemetry, validating detections through controlled simulations, correlating events, documenting evidence gaps, and producing repeatable investigation reports.

## Key Capabilities

- **Security monitoring:** Wazuh-based monitoring of a Windows endpoint with Sysmon telemetry.
- **Detection engineering:** Custom Wazuh rules and controlled validation of detection behaviour.
- **Detection validation:** Positive and negative test cases, including analysis of overlapping built-in and custom alerts.
- **Event ingestion:** Offline loading of JSON, JSON Lines, and Wazuh/OpenSearch search-result exports.
- **Event correlation:** Correlation of Sysmon process-creation and file-creation events using process GUIDs.
- **Investigation reporting:** Chronological event timelines and JSON/Markdown investigation reports.
- **Detection context:** Associated Wazuh rule IDs, descriptions, observed alert levels, and analyst follow-up checks.
- **Evidence handling:** Explicit documentation of missing evidence, correlation limitations, and unconfirmed conclusions.
- **Automated testing:** Regression tests for ingestion, timestamps, correlation, report generation, and evidence handling.

## Architecture

The lab separates the monitoring infrastructure from the monitored endpoint using VirtualBox.

| Component | Purpose |
|---|---|
| Wazuh Server VM | Centralised event collection, alerting, and analysis |
| Windows Endpoint VM | Generates endpoint and system telemetry |
| Wazuh Agent | Forwards collected endpoint events to the server |
| Sysmon | Provides detailed process and file-system event telemetry |
| Wazuh Dashboard | Supports alert review and investigation |
| DarkLens Investigation Engine | Performs offline event correlation and generates investigation reports |

**Telemetry flow:** Windows Endpoint with Sysmon and Wazuh Agent -> Wazuh Server -> Dashboard and event analysis -> Offline DarkLens investigation engine.

The Python engine processes exported event data independently of the live Wazuh infrastructure. It does not replace Wazuh or require direct access to a running SIEM to generate reports.

## Investigation Engine

The offline investigation engine is implemented in `tools/investigator/engine.py`.

### Current functionality

1. Load JSON arrays, individual JSON objects, JSON Lines, and supported Wazuh/OpenSearch search-result exports.
2. Prefer available Sysmon event timestamps over Wazuh ingestion timestamps.
3. Build a chronological event timeline.
4. Correlate events sharing a process GUID.
5. Identify process-creation and file-creation relationships using Sysmon Event IDs 1 and 11.
6. Record PID-only matches as candidates rather than treating them as confirmed process correlations.
7. Enrich findings with associated Wazuh rule context and the highest observed alert level.
8. Generate JSON and Markdown investigation reports.
9. Document evidence gaps and recommended analyst follow-up checks.

### Important analytical limitations

DarkLens is an investigation aid, not an automated verdict engine.

- A process GUID correlation supports a relationship between events but does not establish malicious intent.
- Wazuh alert levels represent configured alert severity, not a calculated threat probability.
- PID-only matches do not prove process identity because process IDs can be reused.
- File creation does not prove subsequent execution or deletion.
- Conclusions depend on the quality, completeness, and accuracy of the supplied telemetry.

## Detection Engineering and Validation

The lab includes controlled detection validation and documented investigation work.

Examples include:

- A custom Wazuh rule for encoded PowerShell launched through `cmd.exe`.
- Positive and negative simulation results used to assess detection behaviour.
- Analysis of built-in Wazuh alerts and potential false positives.
- Review of PowerShell-created temporary files and security assessment activity.
- Documentation of evidence gaps and decisions not to suppress alerts without sufficient justification.

Detection results are documented with their supporting evidence and limitations. Observing an alert is not, by itself, proof of malicious activity.

## Repository Structure

```text
Darklens/
├── detections/          # Detection rules and related artefacts
├── docs/
│   ├── hunts/           # Threat-hunting documentation
│   └── stages/          # Implementation and validation stages
├── evidences/           # Screenshots and investigation evidence
├── samples/             # Synthetic and reduced real-derived event data
├── tests/               # Automated regression tests
├── tools/
│   └── investigator/    # Offline Python investigation engine
└── README.md
```

Generated investigation output is written to `output/` by default and should not be committed unless a specific report is intentionally included as project evidence.

## Setup

Requirements:

- Python 3.10 or newer
- `pytest` for running the test suite
- A Windows or Linux environment capable of running the Python investigation engine

The Wazuh lab requires its own configured virtual machines. The offline investigation engine can be used separately with supported event exports.

Activate your Python virtual environment and install `pytest` if it is not already installed.

## Usage

Run an investigation against the included real-derived event sample:

```powershell
python tools\investigator\engine.py samples\real-events.json --output output\real-investigation
```

The command generates:

- `output/real-investigation/investigation.json`
- `output/real-investigation/investigation.md`

Run the synthetic correlation sample:

```powershell
python tools\investigator\engine.py samples\correlated-events.json --output output\test-investigation
```

Run the automated test suite:

```powershell
python -m pytest -v
```

The current regression suite contains 14 tests covering event ingestion, timestamp selection, process correlation, evidence gaps, detection context, and report generation.

## Evidence and Documentation

The `docs/stages/` directory records implementation milestones, detection validation, technical decisions, and troubleshooting. The `docs/hunts/` directory contains threat-hunting work, while `evidences/` stores supporting artefacts.

The project also documents the migration from Docker-based experimentation to VirtualBox after encountering local resource constraints. This history is retained to explain engineering decisions and the final lab architecture.

The sample `samples/real-events.json` contains a reduced representation of observed Wazuh events. It is intended to demonstrate the investigation workflow, not to represent a complete production telemetry export.

## Security and Scope

DarkLens is a defensive cybersecurity learning and portfolio project. Testing is performed in an isolated lab using controlled, documented activity.

Before publishing evidence or event samples, remove credentials, private keys, certificates, sensitive host information, and unnecessary internal network details.

## Technologies

- Wazuh
- Sysmon
- Windows
- VirtualBox
- Python
- pytest
- JSON and Markdown reporting
- MITRE ATT&CK for detection mapping
- Docker Compose for historical deployment experimentation

## Project Status

The core lab and offline investigation engine are implemented. The investigation engine has a regression suite of 14 passing tests, and the real-derived sample demonstrates process-to-file event correlation with explicit evidence limitations.

Further enhancements may include richer detection-to-investigation workflows, additional event correlation patterns, more comprehensive analyst playbooks, and improved report presentation. These should be added only when they provide demonstrable value.

## Disclaimer

DarkLens is an educational portfolio project, not a production SIEM or autonomous incident-response system. Findings require analyst interpretation and should be assessed against the available evidence, collection coverage, and operational context.