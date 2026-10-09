# DarkLens: Detection Engineering & SOC Investigation Platform

DarkLens is a hands-on cybersecurity lab focused on security monitoring, detection engineering, threat hunting, and incident investigation. The project uses Wazuh, Windows telemetry, and Sysmon to develop and validate practical detection capabilities in an isolated virtual environment.

## Project Objectives

- Collect and investigate Windows security telemetry.
- Develop and test custom detection rules.
- Map suspicious activity to MITRE ATT&CK.
- Investigate alerts and distinguish malicious activity from legitimate behaviour.
- Document incident findings, false positives, and detection improvements.
- Develop Python-based automation and incident response playbooks.

## Lab Architecture

The current lab uses separate virtual machines to isolate the monitoring infrastructure from the monitored endpoint.

| Component | Purpose |
|---|---|
| Wazuh Server VM | Centralised security monitoring and alert analysis |
| Windows Endpoint VM | Generates endpoint and system activity |
| Wazuh Agent | Forwards collected endpoint events to Wazuh |
| Sysmon | Provides detailed Windows process and system telemetry |
| Wazuh Dashboard | Supports event review, alert analysis, and investigations |

**Architecture:** Windows VM with Sysmon and Wazuh Agent → Wazuh Server VM → Dashboard and event analysis.

Wazuh archives are enabled for raw-event investigation. Their successful ingestion and availability will be documented as verified only after testing.

## Project Status

- [x] SOC fundamentals and lab planning
- [x] Wazuh deployment and initial lab configuration
- [x] Windows endpoint integration
- [x] Sysmon installation and integration
- [x] Lab migration from Docker to VirtualBox
- [ ] Verify raw-event ingestion and telemetry coverage
- [ ] Develop the first custom detection
- [ ] Test detections using controlled lab activity
- [ ] Document investigations and false-positive analysis
- [ ] Add detection automation and response playbooks

## Detection Engineering Roadmap

Planned work includes:

1. **Windows detections:** identify suspicious process execution and other relevant endpoint activity.
2. **Threat hunting:** investigate telemetry for suspicious patterns and behaviours.
3. **MITRE ATT&CK mapping:** associate detections with relevant techniques.
4. **Investigation workflow:** document alert triage, evidence, findings, and conclusions.
5. **Detection tuning:** evaluate false positives and improve rule quality.
6. **Automation:** develop scripts and response playbooks for repeatable SOC workflows.

All testing will be performed in the isolated lab using controlled, documented activity.

## Repository Structure

```text
Darklens/
├── README.md
└── docs/
    └── stages/
        ├── stage-01-soc-foundations.md
        ├── stage-02-lab-architecture.md
        ├── stage-03-wazuh-deployment.md
        ├── stage-04-windows-agent.md
        ├── stage-05-sysmon-telemetry.md
        └── stage-06-infrastructure-rebuild.md
```

Additional directories for detections, investigations, hunting, automation, and playbooks will be introduced as those artifacts are developed.

## Documentation

The `docs/stages/` directory records the project's implementation stages, technical decisions, troubleshooting, and lessons learned. The Docker-to-VirtualBox migration is retained as part of the project's engineering history.

## Security and Scope

This is a defensive cybersecurity learning project. Experiments are conducted in an isolated lab. Public documentation must not contain credentials, private keys, certificates, sensitive host information, or unnecessary internal network details.

## Technologies

- Wazuh
- Sysmon
- Windows
- VirtualBox
- Docker Compose (historical deployment approach)
- MITRE ATT&CK
- Python (planned detection and investigation automation)

## Disclaimer

DarkLens is an educational portfolio project. Detection results and investigation conclusions will be documented with supporting evidence and limitations.
