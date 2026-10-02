# Stage 4: Windows Endpoint Integration

## Objective

Connect a Windows endpoint to the Wazuh Manager and verify authenticated communication.

## Components

- Windows 11 endpoint
- Wazuh Agent
- Wazuh Manager
- Wazuh Indexer
- Wazuh Dashboard
- Docker Compose

## Implementation

The Windows endpoint was enrolled with the Wazuh Manager using an authentication key.

## Verification

The Wazuh Agent successfully:

1. Requested authentication
2. Received a valid key
3. Connected to the Manager
4. Established communication
5. Reported as active in the Wazuh Dashboard

## Troubleshooting

The Agent initially experienced connection issues. Agent logs were used to identify the authentication and connection sequence.

## Result

The Windows endpoint is now actively communicating with the Wazuh Manager.

## Next Stage

Deploy Sysmon and begin collecting richer Windows telemetry.