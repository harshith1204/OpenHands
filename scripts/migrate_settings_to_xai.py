#!/usr/bin/env python3
"""One-time migration of ~/.openhands/settings.json to Simpo xAI defaults.

Applies the same rules as FileSettingsStore load-time migration. Useful when
a Docker volume has stale settings before redeploy.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path

_REPO_ROOT = Path(__file__).resolve().parents[1]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from openhands.app_server.settings.simpo_settings_migration import (
    migrate_settings_kwargs_for_simpo_xai,
)
from openhands.app_server.utils.simpo_llm_config import is_simpo_xai_only_mode


def _default_settings_path() -> Path:
    file_store_path = os.getenv('FILE_STORE_PATH', '').strip()
    if file_store_path:
        return Path(file_store_path) / 'settings.json'
    return Path.home() / '.openhands' / 'settings.json'


def _diff_summary(before: dict, after: dict) -> list[str]:
    lines: list[str] = []
    before_model = (before.get('agent_settings') or {}).get('llm', {}).get('model')
    after_model = (after.get('agent_settings') or {}).get('llm', {}).get('model')
    if before_model != after_model:
        lines.append(f'  agent_settings.llm.model: {before_model!r} -> {after_model!r}')

    before_effort = (before.get('agent_settings') or {}).get('llm', {}).get(
        'reasoning_effort'
    )
    after_effort = (after.get('agent_settings') or {}).get('llm', {}).get(
        'reasoning_effort'
    )
    if before_effort != after_effort:
        lines.append(
            f'  agent_settings.llm.reasoning_effort: {before_effort!r} -> {after_effort!r}'
        )

    before_profiles = (before.get('llm_profiles') or {}).get('profiles')
    after_profiles = (after.get('llm_profiles') or {}).get('profiles')
    if before_profiles != after_profiles:
        lines.append(f'  llm_profiles.profiles: {before_profiles!r} -> {after_profiles!r}')

    before_active = (before.get('llm_profiles') or {}).get('active')
    after_active = (after.get('llm_profiles') or {}).get('active')
    if before_active != after_active:
        lines.append(f'  llm_profiles.active: {before_active!r} -> {after_active!r}')

    if before.get('llm_model') != after.get('llm_model'):
        lines.append(
            f'  llm_model: {before.get("llm_model")!r} -> {after.get("llm_model")!r}'
        )

    return lines


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        '--path',
        type=Path,
        default=None,
        help='Path to settings.json (default: ~/.openhands/settings.json)',
    )
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Print changes without writing the file',
    )
    args = parser.parse_args(argv)

    if not is_simpo_xai_only_mode():
        print(
            'OH_LLM_PROVIDER_ALLOWLIST must be set to "xai" for migration.',
            file=sys.stderr,
        )
        return 1

    path = args.path or _default_settings_path()
    if not path.exists():
        print(f'No settings file at {path}', file=sys.stderr)
        return 1

    raw = path.read_text(encoding='utf-8')
    before = json.loads(raw)
    after, migrated = migrate_settings_kwargs_for_simpo_xai(before)

    if not migrated:
        print(f'No migration needed for {path}')
        return 0

    print(f'Migration changes for {path}:')
    for line in _diff_summary(before, after):
        print(line)

    if args.dry_run:
        print('(dry run — file not written)')
        return 0

    path.write_text(json.dumps(after, indent=2) + '\n', encoding='utf-8')
    print(f'Wrote migrated settings to {path}')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
