# DarkLens: Detection Engineering & SOC Investigation Platform

DarkLens is a hands-on cybersecurity portfolio project focused on security monitoring, detection engineering, threat hunting, and incident investigation. It combines an isolated Wazuh lab with Windows Sysmon telemetry and a Python-based investigation engine to demonstrate practical SOC workflows.

The project covers the detection lifecycle: collecting endpoint telemetry, validating detections through controlled simulations, correlating events, documenting evidence gaps, and producing repeatable investigation reports.

## Key Capabilities

- **Security monitoring:** Wazuh-based monitoring of a Windows endpoint with Sysmon telemetry.
- **Detection engineering:** Custom Wazuh rules and controlled validation of detection behaviour.
- **Detection validation:** Positive and negative test cases, including analysis of overlapping built-in and custom alerts.
- **Event ingestion:** Offline loading of JSON, JSON Lines, and supported Wazuh/OpenSearch search-result exports.
- **Event correlation:** Correlation of Sysmon process-creation and file-creation events using process GUIDs.
- **Investigation reporting:** Chronological event timelines and JSON/Markdown investigation reports.
- **Detection context:** Associated Wazuh rule IDs, descriptions, observed alert levels, and analyst follow-up checks.
- **Evidence handling:** Explicit documentation of missing evidence, correlation limitations, and unconfirmed conclusions.
- **Interactive dashboard:** Streamlit interface for event exploration, investigation review, and report downloads.
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
| DarkLens Streamlit Dashboard | Provides a visual interface for offline event exploration, investigations, and reporting |

**Telemetry flow:** Windows Endpoint with Sysmon and Wazuh Agent → Wazuh Server → Wazuh Dashboard and event analysis → Offline DarkLens investigation engine → DarkLens Streamlit dashboard.

The Python investigation engine processes exported event data independently of the live Wazuh infrastructure. The Streamlit dashboard currently uses included offline JSON samples and does not have live Wazuh API integration enabled.

## Investigation Engine

The offline investigation engine is implemented in `tools/investigator/engine.py`.

### Current Functionality

1. Load JSON arrays, individual JSON objects, JSON Lines, and supported Wazuh/OpenSearch search-result exports.
2. Prefer available Sysmon event timestamps over Wazuh ingestion timestamps.
3. Build a chronological event timeline.
4. Correlate events sharing a process GUID.
5. Identify process-creation and file-creation relationships using Sysmon Event IDs 1 and 11.
6. Record PID-only matches as candidates rather than treating them as confirmed process correlations.
7. Enrich findings with associated Wazuh rule context and the highest observed alert level.
8. Generate JSON and Markdown investigation reports.
9. Document evidence gaps and recommended analyst follow-up checks.

### Important Analytical Limitations

DarkLens is an investigation aid, not an automated verdict engine.

- A process GUID correlation supports a relationship between events but does not establish malicious intent.
- Wazuh alert levels represent configured alert severity, not a calculated threat probability.
- PID-only matches do not prove process identity because process IDs can be reused.
- File creation does not prove subsequent execution or deletion.
- Conclusions depend on the quality, completeness, and accuracy of the supplied telemetry.

## Streamlit Investigation Dashboard

DarkLens includes a Streamlit dashboard that provides a visual interface for the offline investigation engine.

### Dashboard Features

- **Overview:** Displays event counts, process correlations, findings, and the highest observed alert level for the selected sample.
- **Event Explorer:** Search and filter events by event ID, rule, process, and command line. Expand events to inspect available details and the complete event record.
- **Investigations:** Review findings, process GUID correlations, PID-only match candidates, detection context, and evidence limitations.
- **Reports:** Download investigation results as JSON or Markdown.

The dashboard allows users to switch between the included `Real events` and `Correlated events` samples. Results are generated from the selected offline sample.

Live Wazuh API integration is not enabled. The dashboard does not currently retrieve events directly from a running Wazuh deployment.

### Launch the Dashboard

Requirements:

- Python 3.10 or newer.
- Streamlit for the dashboard.
- pytest for running the test suite.

From the repository root, activate your Python virtual environment and install the required packages:

```powershell
python -m pip install streamlit pytest
```

Start the dashboard:

```powershell
python -m streamlit run dashboard\app.py
```

Select a sample in the sidebar, then navigate through Overview, Event Explorer, Investigations, and Reports.

### Dashboard Reporting

The Reports page provides JSON and Markdown downloads for the selected sample.

The JSON report contains structured investigation data, including the timeline, process correlations, findings, detection context, and limitations.

The Markdown report presents the investigation in a readable format, including findings, observed evidence, analyst follow-up checks, and evidence gaps.

Reports should be reviewed in the context of the supplied telemetry. Correlation results are not proof of malicious activity.

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
├── dashboard/              # Streamlit investigation dashboard
│   └── app.py
├── detections/              # Detection rules and related artefacts
├── docs/
│   ├── hunts/               # Threat-hunting documentation
│   ├── investigations/     # Investigation write-ups
│   └── stages/              # Implementation and validation stages
├── evidences/               # Screenshots and investigation evidence
├── samples/                 # Synthetic and real-derived event data
├── tests/                   # Automated regression tests
├── tools/
│   └── investigator/        # Offline Python investigation engine
│       └── engine.py
└── README.md
```

Generated investigation output is written to `output/` by default when using the command-line engine. Generated reports should not be committed unless a specific report is intentionally included as project evidence.

The `demo-video/` directory may contain local recordings used to assemble the portfolio demonstration. Keep raw recordings and temporary exports out of Git unless you intentionally decide to publish selected media.

## Setup

### Investigation Engine

The investigation engine uses Python and standard-library modules for its core processing.

To run the automated test suite, install pytest:

```powershell
python -m pip install pytest
```

The engine can be used independently of the dashboard and Wazuh lab with supported event exports.

### Streamlit Dashboard

Install Streamlit and pytest:

```powershell
python -m pip install streamlit pytest
```

Launch the dashboard:

```powershell
python -m streamlit run dashboard\app.py
```

The Wazuh lab requires its own configured virtual machines. The offline investigation engine and dashboard can be used separately with the included samples.

## Usage

### Run an Investigation Against the Real-Derived Sample

```powershell
python tools\investigator\engine.py samples\real-events.json --output output\real-investigation
```

The command generates:

- `output/real-investigation/investigation.json`
- `output/real-investigation/investigation.md`

### Run the Synthetic Correlation Sample

```powershell
python tools\investigator\engine.py samples\correlated-events.json --output output\test-investigation
```

### Run the Automated Test Suite

```powershell
python -m pytest -v
```

The current regression suite contains 14 tests covering event ingestion, timestamp selection, process correlation, evidence gaps, detection context, and report generation.

## Evidence and Documentation

The `docs/stages/` directory records implementation milestones, detection validation, technical decisions, and troubleshooting. The `docs/hunts/` directory contains threat-hunting work, while `docs/investigations/` contains investigation write-ups. The `evidences/` directory stores supporting artefacts.

The project also documents the migration from Docker-based experimentation to VirtualBox after encountering local resource constraints. This history is retained to explain engineering decisions and the final lab architecture.

The sample `samples/real-events.json` contains a reduced representation of observed Wazuh events. It is intended to demonstrate the investigation workflow, not to represent a complete production telemetry export.

## Security and Scope

DarkLens is a defensive cybersecurity learning and portfolio project. Testing is performed in an isolated lab using controlled, documented activity.

Before publishing evidence or event samples, remove credentials, private keys, certificates, sensitive host information, and unnecessary internal network details.

Review screenshots and reports before publication to ensure they do not expose sensitive environment details.

## Technologies

- Wazuh
- Sysmon
- Windows
- VirtualBox
- Python
- Streamlit
- pytest
- JSON and Markdown reporting
- MITRE ATT&CK for detection mapping
- Docker Compose for historical deployment experimentation

## Project Status

The core Wazuh lab, offline Python investigation engine, and Streamlit investigation dashboard are implemented. The dashboard supports offline sample selection, event exploration, investigation review, and JSON/Markdown report downloads.

The regression suite currently contains 14 passing tests. The included real-derived sample demonstrates process-to-file event correlation while explicitly documenting evidence gaps and the limitations of the available telemetry.

Live Wazuh API integration is not enabled in the dashboard. The current dashboard operates on the included offline JSON samples; live SIEM integration remains future work.

Potential future enhancements include additional event correlation patterns, richer detection-to-investigation workflows, more comprehensive analyst playbooks, and live Wazuh integration. These should be added only when they provide demonstrable value.

## Disclaimer

DarkLens is an educational portfolio project, not a production SIEM or autonomous incident-response system. Findings require analyst interpretation and should be assessed against the available evidence, collection coverage, and operational context.