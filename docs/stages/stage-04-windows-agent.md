# Stage 4: Windows Agent Integration

## Objective

Connect a Windows endpoint to the Wazuh monitoring environment and establish the foundation for centralised security event collection.

## Architecture

The current lab uses two separate virtual machines:

- **Wazuh Server VM:** Runs the Wazuh Manager, Indexer, and Dashboard.
- **Windows Endpoint VM:** Runs Windows 11, Sysmon, and the Wazuh Agent.

This design isolates endpoint experiments from the host machine and separates monitoring infrastructure from the monitored endpoint.

## Implementation

The following steps were completed:

1. Created a separate Windows virtual machine in VirtualBox.
2. Installed the Wazuh Agent on the Windows endpoint.
3. Configured the agent to communicate with the Wazuh server.
4. Registered and connected the endpoint to the monitoring environment.
5. Confirmed that the agent appeared connected in the Wazuh Dashboard.

## Agent Responsibilities

The Wazuh Agent collects configured endpoint data and forwards it to the Wazuh Manager for processing.

Depending on the enabled configuration, this may include:

- Windows Event Channel events.
- Sysmon operational events.
- File integrity monitoring events.
- Security configuration assessment results.

The availability of each data source must be verified independently. An active agent does not automatically prove that every configured event channel is being collected.

## Verification

The initial connection was reported as successful when the Windows endpoint appeared connected in the Wazuh Dashboard.

Further verification should establish that:

- The agent remains active and connected.
- Windows events reach the Wazuh server.
- Sysmon events are collected from `Microsoft-Windows-Sysmon/Operational`.
- Relevant events can be located and inspected in Wazuh.
- Raw-event archives are available if archive collection and indexing are configured.

## Troubleshooting Considerations

Potential issues include:

- Incorrect manager address or agent configuration.
- Network connectivity or firewall restrictions between the VMs.
- An agent service that is running but not connected.
- Event channels that are not configured for collection.
- Events that are collected but not indexed or displayed in the expected view.

When troubleshooting, inspect agent status and logs, verify connectivity, and search for a known test event before changing the configuration.

## Security Considerations

- Do not publish agent authentication keys or credentials.
- Avoid exposing private IP addresses or other unnecessary lab-specific details.
- Generate test activity only within the authorised lab environment.
- Use event evidence to verify collection instead of relying solely on dashboard status.

## Result

The Windows endpoint has been connected to the Wazuh monitoring environment. This establishes the endpoint integration needed for subsequent Sysmon telemetry validation and custom detection development.

The full telemetry pipeline remains subject to event-level verification.

## Related Documentation

- [Stage 2: Lab Architecture](stage-02-lab-architecture.md)
- [Stage 3: Wazuh Deployment](stage-03-wazuh-deployment.md)
- [Stage 5: Sysmon and Windows Telemetry](stage-05-sysmon-telemetry.md)
- [Stage 6: Infrastructure Rebuild](stage-06-infrastructure-rebuild.md)
