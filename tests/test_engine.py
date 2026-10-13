
import json

import pytest

from tools.investigator.engine import (
    investigate,
    load_events,
    write_reports,
)


@pytest.fixture
def sample_events():
    return [
        {
            "timestamp": "2026-10-13T11:06:36.370Z",
            "rule": {"id": "92021", "level": 3},
            "data": {
                "win": {
                    "system": {"eventID": "1"},
                    "eventdata": {
                        "processGuid": "{process-123}",
                        "processId": "4612",
                        "image": r"C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe",
                        "commandLine": "powershell secedit /export",
                    },
                }
            },
        },
        {
            "timestamp": "2026-10-13T11:06:38.814Z",
            "data": {
                "win": {
                    "system": {"eventID": "11"},
                    "eventdata": {
                        "processGuid": "{process-123}",
                        "processId": "4612",
                        "targetFilename": r"C:\Windows\Temp\secpol.cfg",
                    },
                }
            },
        },
    ]


def test_correlates_events_by_process_guid(sample_events):
    result = investigate(sample_events)

    assert result["input_event_count"] == 2
    assert len(result["process_correlations"]) == 1
    assert result["process_correlations"][0]["process_guid"] == "{process-123}"
    assert result["process_correlations"][0]["event_count"] == 2


def test_timeline_is_chronological(sample_events):
    result = investigate(sample_events)

    assert result["timeline"][0]["event_id"] == "1"
    assert result["timeline"][1]["event_id"] == "11"


def test_does_not_correlate_events_without_process_guid():
    events = [
        {"timestamp": "2026-10-13T11:00:00Z"},
        {"timestamp": "2026-10-13T11:00:01Z"},
    ]

    result = investigate(events)

    assert result["process_correlations"] == []


def test_loads_json_file(tmp_path, sample_events):
    file_path = tmp_path / "events.json"
    file_path.write_text(json.dumps(sample_events), encoding="utf-8")

    loaded = load_events([file_path])

    assert len(loaded) == 2


def test_rejects_malformed_json(tmp_path):
    file_path = tmp_path / "broken.json"
    file_path.write_text('{"timestamp": invalid}', encoding="utf-8")

    with pytest.raises(ValueError, match="Invalid JSON"):
        load_events([file_path])


def test_writes_json_and_markdown_reports(tmp_path, sample_events):
    result = investigate(sample_events)

    json_path, markdown_path = write_reports(result, tmp_path / "reports")

    assert json_path.exists()
    assert markdown_path.exists()
    assert json.loads(json_path.read_text(encoding="utf-8"))["input_event_count"] == 2
    assert "DarkLens Investigation Report" in markdown_path.read_text(encoding="utf-8")
def test_reports_process_file_relationship_and_evidence_gaps(sample_events):
    result = investigate(sample_events)

    assert len(result["findings"]) == 1

    finding = result["findings"][0]
    assert finding["type"] == "process_file_creation_correlation"
    assert finding["process_guid"] == "{process-123}"
    assert finding["files_created"] == [
        r"C:\Windows\Temp\secpol.cfg"
    ]
    assert any(
        "malicious intent" in finding["interpretation"]
        for _ in [0]
    )
    assert any(
        "deletion" in gap.lower()
        for gap in finding["evidence_gaps"]
    )

def test_loads_native_wazuh_search_result(tmp_path):
    wrapper = {
        "_index": "wazuh-archives-test",
        "_id": "example-id",
        "_source": {
            "timestamp": "2026-10-13T11:06:48.451+0000",
            "agent": {"name": "Windowmon", "id": "001"},
            "data": {
                "win": {
                    "system": {"eventID": "11"},
                    "eventdata": {
                        "utcTime": "2026-10-13 11:06:36.928",
                        "processGuid": "{real-guid}",
                        "processId": "4612",
                        "targetFilename": r"C:\Windows\Temp\test.ps1",
                    },
                }
            },
        },
    }
    file_path = tmp_path / "wazuh-search.json"
    file_path.write_text(json.dumps(wrapper), encoding="utf-8")

    loaded = load_events([file_path])

    assert len(loaded) == 1
    assert loaded[0]["agent"]["name"] == "Windowmon"
    assert loaded[0]["data"]["win"]["eventdata"]["processGuid"] == "{real-guid}"


def test_prefers_sysmon_event_time_over_ingestion_time():
    event = {
        "timestamp": "2026-10-13T11:06:48.451+0000",
        "@timestamp": "2026-10-13T11:06:48.451Z",
        "data": {
            "win": {
                "system": {"eventID": "11"},
                "eventdata": {"utcTime": "2026-10-13 11:06:36.928"},
            }
        },
    }

    result = investigate([event])
    timeline_event = result["timeline"][0]

    assert timeline_event["timestamp"] == "2026-10-13T11:06:36.928000+00:00"
    assert timeline_event["timestamp_source"] == "Sysmon event time"


def test_does_not_treat_pid_only_match_as_process_correlation():
    events = [
        {
            "timestamp": "2026-10-13T11:00:00Z",
            "agent": {"name": "Windowmon", "id": "001"},
            "data": {
                "win": {
                    "system": {"eventID": "1"},
                    "eventdata": {"processId": "4612"},
                }
            },
        },
        {
            "timestamp": "2026-10-13T11:00:01Z",
            "agent": {"name": "Windowmon", "id": "001"},
            "data": {
                "win": {
                    "system": {"eventID": "11"},
                    "eventdata": {
                        "processId": "4612",
                        "targetFilename": r"C:\Windows\Temp\test.ps1",
                    },
                }
            },
        },
    ]

    result = investigate(events)

    assert result["process_correlations"] == []
    assert result["findings"] == []
    assert len(result["pid_match_candidates"]) == 1
