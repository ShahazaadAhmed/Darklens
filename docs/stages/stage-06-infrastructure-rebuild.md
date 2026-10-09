# Stage 6: Infrastructure Rebuild

## Objective

Rebuild the DarkLens lab after encountering storage and resource constraints with the original Docker-based deployment.

## Background

The initial Wazuh deployment used Docker Compose through Docker Desktop on Windows. During development, the Docker WSL2 virtual disk grew substantially, consuming significant host storage.

This made the original deployment approach unsuitable for the available resources and motivated a change in infrastructure.

## Decision

The lab was migrated to VirtualBox, using separate virtual machines for the Wazuh server and Windows endpoint.

The objective remained unchanged: establish a functional security monitoring environment for detection engineering and SOC investigations.

## Implementation

The rebuild involved the following work:

1. Removed the previous deployment and rebuilt the lab environment.
2. Deployed the Wazuh server environment in a VirtualBox virtual machine.
3. Created a separate Windows endpoint virtual machine.
4. Installed and connected the Wazuh Agent on the Windows endpoint.
5. Installed Sysmon and integrated its event collection with Wazuh.
6. Enabled Wazuh archive collection to support raw-event investigation.

## Final Architecture

```text
Host Machine
└── VirtualBox
    ├── Wazuh Server VM
    │   ├── Wazuh Manager
    │   ├── Wazuh Indexer
    │   └── Wazuh Dashboard
    │
    └── Windows Endpoint VM
        ├── Windows 10
        ├── Sysmon
        └── Wazuh Agent
```

The Windows endpoint and Wazuh server operate in separate virtual machines. The endpoint sends collected telemetry to the monitoring environment.

## Verification Status

The project owner reports that the Wazuh server is running, the Windows Agent is connected, Sysmon is integrated, and archive collection is enabled.

These conditions establish the reported deployment status. Event-level verification is still required to establish that Sysmon events reach Wazuh and that raw archives are available for search and investigation.

## Lessons Learned

- Infrastructure resource requirements must be considered before selecting a deployment approach.
- Docker's convenience does not eliminate the storage overhead of its underlying virtual disks.
- A migration can be a valid engineering decision when the original approach no longer fits the available environment.
- Separating the monitored endpoint from the host provides a more controlled environment for security experiments.
- Successful service deployment and successful telemetry ingestion are separate verification requirements.

## Result

The original Docker-based deployment was replaced with a VirtualBox-based lab consisting of a Wazuh server VM and a separate Windows endpoint VM.

The migration preserved the project's security monitoring objectives while addressing the constraints encountered during the original implementation.

The next step is to verify telemetry end to end before developing and testing custom detections.

## Related Documentation

- [Stage 2: Lab Architecture](stage-02-lab-architecture.md)
- [Stage 3: Wazuh Deployment](stage-03-wazuh-deployment.md)
- [Stage 4: Windows Agent Integration](stage-04-windows-agent.md)
- [Stage 5: Sysmon and Windows Telemetry](stage-05-sysmon-telemetry.md)
