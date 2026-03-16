"""Integration tests for manifest building and formatting."""

import json
from hold import Hold
from manifests.builder import ManifestBuilder
from manifests.formatter import ManifestFormatter
from manifests.validator import ManifestValidator


class TestManifestWorkflow:
    def make_hold(self):
        hold = Hold()
        hold.create_bay("A")
        hold.create_bay("B", "overflow")
        hold.move("A", "B", 100, "test")
        return hold

    def test_build_and_format(self):
        hold = self.make_hold()
        builder = ManifestBuilder(hold)
        manifest = builder.build_full_manifest()
        formatter = ManifestFormatter()
        text = formatter.format_text(manifest)
        assert "CARGO MANIFEST" in text
        assert "100" in text

    def test_build_and_validate(self):
        hold = self.make_hold()
        builder = ManifestBuilder(hold)
        manifest = builder.build_full_manifest()
        validator = ManifestValidator(hold)
        assert validator.validate_full_manifest(manifest)

    def test_json_roundtrip(self):
        hold = self.make_hold()
        builder = ManifestBuilder(hold)
        manifest = builder.build_full_manifest()
        formatter = ManifestFormatter()
        json_str = formatter.format_json(manifest)
        parsed = json.loads(json_str)
        assert parsed["total_load"] == manifest["total_load"]

    def test_log_manifest(self):
        hold = self.make_hold()
        builder = ManifestBuilder(hold)
        manifest = builder.build_log_manifest()
        assert manifest["entry_count"] == 1
        validator = ManifestValidator()
        assert validator.validate_log_manifest(manifest)
