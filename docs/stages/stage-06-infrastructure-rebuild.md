# Stage 6: Infrastructure Rebuild

## Objective

Rebuild the DarkLens security monitoring infrastructure using VirtualBox after identifying storage and deployment limitations with Docker Desktop.

## Initial Approach

The original DarkLens deployment used Docker Desktop with Wazuh components running in Docker containers.

The environment successfully demonstrated:

- Wazuh Manager
- Wazuh Indexer
- Wazuh Dashboard
- Windows Wazuh Agent
- Sysmon telemetry

However, Docker Desktop's WSL2 virtual disk grew significantly during telemetry collection, consuming substantial host storage.

## Infrastructure Decision

Docker was replaced with VirtualBox for the Wazuh infrastructure.

The decision was based on:

- Better control over virtual machine resources
- Explicit virtual disk allocation
- Separation from Docker Desktop's WSL2 storage
- Preservation of the existing Windows endpoint environment
- Easier resource management for the lab

## Final Architecture

Windows 11 Host
│
├── Sysmon
├── Wazuh Agent
│
└── VirtualBox
    └── DarkLens Wazuh Appliance
        ├── Wazuh Manager
        ├── Wazuh Indexer
        └── Wazuh Dashboard

## Deployment

The official Wazuh Virtual Machine appliance was imported into VirtualBox.

The Wazuh services were successfully started and verified.

The Wazuh Dashboard was also successfully accessed from the Windows host.

## Troubleshooting

An initial Ubuntu Server based installation was attempted.

The installation encountered multiple issues during deployment, including:

- Dashboard installation timeout and system soft-lockup
- Wazuh Manager installation failure
- Missing `wazuh-keystore` executable during Manager startup

The installation was abandoned in favor of the official Wazuh Virtual Machine appliance.

This reduced infrastructure complexity and allowed development to return to the security objectives of DarkLens.

## Engineering Lesson

Infrastructure is a means to support the security objective rather than the objective itself.

The DarkLens project therefore focuses on:

- Detection engineering
- Alert triage
- Threat hunting
- Incident investigation
- MITRE ATT&CK mapping
- Security automation

Wazuh provides the monitoring infrastructure required to perform these activities.

## Stage Result

The DarkLens Wazuh infrastructure is operational using VirtualBox.

## Next Stage

Reconnect the Windows endpoint and verify the complete telemetry pipeline before creating the first custom detection.
