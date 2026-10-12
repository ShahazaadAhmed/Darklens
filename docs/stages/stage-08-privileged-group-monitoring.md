# Stage 08: Privileged Local Group Monitoring

## Objective

Validate whether DarkLens can observe and investigate changes to membership of the local Windows Administrators group, and identify gaps in existing Wazuh detection coverage.

## Environment

- Windows 10 endpoint VM
- Wazuh Agent and Sysmon
- Wazuh Manager and Dashboard
- Test account: `DarkLensTest`

## Test Procedure

A disposable local account was created and added to the local Administrators group using an elevated Command Prompt.

The following command was executed:

```cmd
net localgroup Administrators DarkLensTest /add
```

The account's group membership was verified on the endpoint. Its SID was also retrieved to correlate the account with the Windows Security audit event.

## Telemetry and Alert Results

### Sysmon Process Creation

Sysmon Event ID 1 captured the command execution.

- Executable: `net1.exe`
- Parent executable: `net.exe`
- Command line: `net localgroup Administrators DarkLensTest /add`
- Existing Wazuh rule: `92031`
- Alert level: 3
- Existing description: `Discovery activity executed`

The command-line event established that the operation was invoked, but it did not independently prove that the group modification succeeded.

### Windows Security Audit Event

Windows Security Event ID 4732 recorded a successful addition to a security-enabled local group.

- Group: `Administrators`
- Group SID: `S-1-5-32-544`
- Actor: `DESKTOP-GGLJFDQ\Windowmon`
- Audit result: `AUDIT_SUCCESS`
- Existing Wazuh rule: `60154`
- Alert level: 12
- Existing description: `Administrators Group Changed`

The event's member SID was:

`S-1-5-21-1890898635-3973244862-1529490584-1003`

The endpoint's local account query confirmed that this SID belonged to `DarkLensTest`.

## Analysis

The correlated evidence establishes the test sequence:

1. Sysmon recorded the group-modification command.
2. Windows Security auditing recorded the successful group membership change.
3. The member SID matched the disposable test account.
4. Wazuh generated an alert for the Administrators group change.

Wazuh already provides detection coverage through rule `60154`. Therefore, a custom rule that simply alerts on every Event ID 4732 would duplicate existing functionality.

The observed Sysmon event was mapped by its Sysmon `RuleName` to T1018, Remote System Discovery, while Wazuh's rule 92031 mapped the alert to T1087, Account Discovery. These mappings describe existing rule metadata and should not be treated as proof that the group modification itself was discovery activity.

## Cleanup

After evidence collection, the disposable `DarkLensTest` account was removed from the local Administrators group and deleted.

The cleanup prevented the test account from retaining unnecessary administrative privileges.

## Evidence

Screenshots are stored in `evidences/detection-02/`:

1. `sysmon-command.png` — Sysmon process details and the group-modification command.
2. `security-event-4732.png` — Wazuh alerts showing Windows Security Event ID 4732.
3. `member-sid-verification.png` — Endpoint output showing the test account and its SID.

## Outcome

The lab successfully demonstrated collection and correlation of Sysmon process telemetry with Windows Security group-change auditing.

Existing Wazuh detection coverage was validated. No redundant custom rule was added.

## Next Steps

- Inspect the full details of the additional Event ID 4732 alert associated with rule `60170`.
- Assess whether existing alerts provide sufficient context for SOC triage.
- If a meaningful detection gap is identified, implement a targeted improvement and test it against both benign and suspicious scenarios.