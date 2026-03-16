"""Integration tests for serialization and loading."""

import json
from hold import Hold
from storage.serializer import HoldSerializer
from storage.exporter import HoldExporter
from storage.loader import HoldLoader


class TestSerializationWorkflow:
    def make_hold(self):
        hold = Hold()
        hold.create_bay("A")
        hold.create_bay("B", "overflow")
        hold.move("A", "B", 100, "test")
        hold.move("A", "B", 200, "test2")
        return hold

    def test_serialize_and_load(self):
        hold = self.make_hold()
        serializer = HoldSerializer()
        data = serializer.serialize_hold(hold)
        loader = HoldLoader()
        restored = loader.from_dict(data)
        assert len(restored.bays()) == 2
        assert restored.get_bay("A").load == 300
        assert restored.get_bay("B").load == -300

    def test_json_roundtrip(self):
        hold = self.make_hold()
        serializer = HoldSerializer()
        json_str = serializer.to_json(hold)
        loader = HoldLoader()
        restored = loader.from_json(json_str)
        assert len(restored.log_entries()) == 2

    def test_export_csv(self):
        hold = self.make_hold()
        exporter = HoldExporter(hold)
        csv_str = exporter.to_csv_string()
        assert "A" in csv_str
        assert "B" in csv_str

    def test_export_text(self):
        hold = self.make_hold()
        exporter = HoldExporter(hold)
        text = exporter.to_text_report()
        assert "CARGO HOLD" in text

    def test_snapshot(self):
        hold = self.make_hold()
        serializer = HoldSerializer()
        snap = serializer.snapshot(hold)
        assert snap["bays"]["A"] == 300
        assert snap["log_size"] == 2
