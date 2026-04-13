"""Tests for JobConfig.base_out_dir and jobs_dir fields."""

from pathlib import Path

import pytest

from rock.sdk.agent.constants import USER_DEFINED_LOGS
from rock.sdk.agent.models.job.config import JobConfig


EXPERIMENT_ID = "exp-base-out-dir"


class TestBaseOutDirDefault:
    def test_default_base_out_dir(self):
        """base_out_dir defaults to USER_DEFINED_LOGS."""
        cfg = JobConfig(experiment_id=EXPERIMENT_ID)
        assert cfg.base_out_dir == Path(USER_DEFINED_LOGS)

    def test_default_jobs_dir_is_none(self):
        """jobs_dir defaults to None; caller sets it to base_out_dir / 'jobs' when needed."""
        cfg = JobConfig(experiment_id=EXPERIMENT_ID)
        assert cfg.jobs_dir is None


class TestBaseOutDirCustom:
    def test_custom_base_out_dir(self):
        """Custom base_out_dir is stored as-is."""
        cfg = JobConfig(experiment_id=EXPERIMENT_ID, base_out_dir=Path("/my/output"))
        assert cfg.base_out_dir == Path("/my/output")

    def test_explicit_jobs_dir(self):
        """Explicitly set jobs_dir is stored as-is."""
        cfg = JobConfig(
            experiment_id=EXPERIMENT_ID,
            base_out_dir=Path("/my/output"),
            jobs_dir=Path("/custom/jobs"),
        )
        assert cfg.jobs_dir == Path("/custom/jobs")

    def test_jobs_dir_independent_of_base_out_dir(self):
        """jobs_dir can be set independently of base_out_dir."""
        cfg = JobConfig(
            experiment_id=EXPERIMENT_ID,
            jobs_dir=Path("/standalone/jobs"),
        )
        assert cfg.jobs_dir == Path("/standalone/jobs")
        assert cfg.base_out_dir == Path(USER_DEFINED_LOGS)
