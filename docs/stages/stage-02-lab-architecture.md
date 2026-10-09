# Stage 2: Lab Architecture

## Objective

Design an isolated security monitoring lab that supports Windows telemetry collection, centralised event analysis, detection engineering, and SOC investigations.

## Architecture Decision

The lab uses VirtualBox to run the Wazuh server and Windows endpoint in separate virtual machines.

The original deployment plan used Docker Compose for the Wazuh components. Docker was later replaced with a VirtualBox-based deployment after storage consumption from Docker Desktop's WSL2 virtual disk became a constraint. The migration and its rationale are documented in Stage 6.

## Current Lab Architecture

```text
Host Machine
└── VirtualBox
    ├── Wazuh Server VM
    │   ├── Wazuh Manager
    │   ├── Wazuh Indexer
    │   └── Wazuh Dashboard
    │
    └── Windows Endpoint VM
        ├── Windows 11
        ├── Sysmon
        └── Wazuh Agent
                │
                └── Sends collected events to Wazuh Manager
```

## Component Responsibilities

| Component | Responsibility |
|---|---|
| Wazuh Manager | Receives endpoint data, evaluates rules, and generates alerts |
| Wazuh Indexer | Stores and indexes data for search and analysis |
| Wazuh Dashboard | Provides the interface for monitoring and investigation |
| Windows 11 VM | Acts as the monitored endpoint |
| Sysmon | Records detailed Windows system activity |
| Wazuh Agent | Collects configured endpoint events and forwards them to the server |

## Telemetry Flow

1. Windows generates operating system and application events.
2. Sysmon records configured system activity in its operational event channel.
3. The Wazuh Agent collects configured event data.
4. The Wazuh Manager processes incoming events and evaluates applicable detection rules.
5. Relevant alerts and indexed data are reviewed through the Wazuh Dashboard.

Raw-event archiving is also configured for investigation. Archive ingestion and searchability must be verified separately from normal alert generation.

## Design Considerations

- **Isolation:** Keep the monitored Windows endpoint separate from the host machine.
- **Resource management:** Allocate virtual machine resources within the host's available capacity.
- **Storage management:** Monitor virtual disk growth and retention settings.
- **Observability:** Verify event collection independently from alert generation.
- **Reproducibility:** Document deployment steps and relevant configuration without publishing credentials or sensitive environment details.
- **Safety:** Conduct experiments only within the authorised lab environment.

## Verification Criteria

The architecture is considered operational when:

- The Wazuh services are running.
- The Windows Agent is connected and active.
- Sysmon is generating the expected Windows events.
- Sysmon events are visible in Wazuh.
- Raw-event archives are available for investigation, if archive collection and indexing are configured.
- A controlled test event can be traced from the endpoint to the monitoring platform.

## Result

The lab architecture separates the Wazuh monitoring infrastructure from the Windows endpoint. This provides a foundation for validating telemetry, developing detections, and conducting repeatable SOC investigations.

The verification criteria above are intended to be checked against the current environment rather than treated as automatically satisfied.

## Related Documentation

- [Stage 3: Wazuh Deployment](stage-03-wazuh-deployment.md)
- [Stage 4: Windows Endpoint Integration](stage-04-windows-agent.md)
- [Stage 5: Sysmon and Windows Telemetry](stage-05-sysmon-telemetry.md)
- [Stage 6: Infrastructure Rebuild](stage-06-infrastructure-rebuild.md)
