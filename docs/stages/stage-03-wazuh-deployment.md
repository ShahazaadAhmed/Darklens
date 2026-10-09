# Stage 3: Wazuh Deployment

## Objective

Deploy a Wazuh monitoring environment and understand the roles of its core components in a Security Operations Centre (SOC).

## Initial Deployment: Docker Compose

The initial deployment used Docker Compose to run the Wazuh single-node environment.

The deployment included:

- **Wazuh Manager:** Event processing and detection rule evaluation.
- **Wazuh Indexer:** Security data indexing and storage.
- **Wazuh Dashboard:** Interface for monitoring and investigation.

Docker Compose provided a convenient way to define and manage the services as a coordinated environment.

## Deployment Challenges

During implementation, the lab encountered infrastructure constraints, including:

- Port-binding conflicts on the host.
- Kernel parameter configuration requirements for the indexer.
- Significant storage consumption by Docker Desktop's WSL2 virtual disk.

These issues provided practical experience with service configuration, resource management, and infrastructure troubleshooting.

## Infrastructure Decision

Docker was subsequently replaced by a VirtualBox-based environment. The decision was driven by the storage and resource constraints encountered during the original deployment.

The current environment uses a Wazuh server virtual machine, with the Windows endpoint running separately in its own virtual machine.

The migration process is documented in [Stage 6: Infrastructure Rebuild](stage-06-infrastructure-rebuild.md).

## Current Deployment Status

The current Wazuh server environment has been rebuilt in VirtualBox. The project owner reports that the server components are running and the Windows Agent is connected.

The current deployment must be distinguished from the original Docker Compose environment. Docker Compose is retained here as historical implementation context, not as the current architecture.

## Verification Criteria

The deployment should be considered verified when:

- Wazuh Manager, Indexer, and Dashboard are operational.
- The Dashboard is accessible.
- The Windows Agent appears active in Wazuh.
- Endpoint telemetry can be located in the monitoring platform.
- Raw-event archive availability is checked separately if required.

## Lessons Learned

- Successful container startup does not guarantee that every service is fully operational.
- Port conflicts and kernel parameter requirements can prevent successful deployment.
- Storage consumption must be considered when choosing an infrastructure approach.
- Infrastructure choices should support the project's primary objective: reliable telemetry collection and detection engineering.

## Result

The initial Docker Compose deployment established the project's monitoring architecture and exposed practical infrastructure challenges. The subsequent migration to VirtualBox retained the project's objectives while changing the deployment method.

The project now proceeds using the VirtualBox-based environment.

## Related Documentation

- [Stage 2: Lab Architecture](stage-02-lab-architecture.md)
- [Stage 4: Windows Agent Integration](stage-04-windows-agent.md)
- [Stage 6: Infrastructure Rebuild](stage-06-infrastructure-rebuild.md)
