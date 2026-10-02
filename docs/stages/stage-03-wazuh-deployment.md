# Stage 3: Wazuh Deployment

## Objective

Deploy and validate the core Wazuh infrastructure using Docker Compose.

## Components Deployed

The DarkLens environment uses:

- Wazuh Manager 4.14.8
- Wazuh Indexer 4.14.8
- Wazuh Dashboard 4.14.8

## Deployment Architecture

```text
Docker Compose
│
├── Wazuh Manager
│
├── Wazuh Indexer
│
└── Wazuh Dashboard