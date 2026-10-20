import importlib
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]

for directory in (ROOT, ROOT / "src"):
    if directory.is_dir() and str(directory) not in sys.path:
        sys.path.insert(0, str(directory))


@pytest.fixture(scope="session")
def module_prefix():
    candidates = [
        path.parent
        for path in ROOT.rglob("router.py")
        if (path.parent / "models.py").is_file()
        and not any(
            part.startswith(".") or part in {"venv", "env", "site-packages", "__pycache__"}
            for part in path.relative_to(ROOT).parts
        )
    ]

    if len(candidates) != 1:
        pytest.fail(f"Expected exactly one directory containing router.py and models.py; found {len(candidates)}.")

    package_dir = candidates[0]
    source_root = ROOT / "src"
    base = source_root if source_root in package_dir.parents else ROOT
    return ".".join(package_dir.relative_to(base).parts)


@pytest.fixture(scope="session")
def router_module(module_prefix):
    name = f"{module_prefix}.router" if module_prefix else "router"
    return importlib.import_module(name)


@pytest.fixture(scope="session")
def intent_type(module_prefix):
    name = f"{module_prefix}.models" if module_prefix else "models"
    return importlib.import_module(name).Intent


@pytest.fixture
def office_names():
    return {"phong dao tao", "student affairs"}


@pytest.fixture
def settings():
    from assistant_core.config import Settings

    return Settings(data_dir=ROOT / "data")


@pytest.fixture
def service(settings):
    from assistant_core.knowledge import Handbook, OfficeDirectory
    from assistant_core.responder import StubLLMResponder
    from assistant_core.service import AssistantService

    offices = OfficeDirectory.from_csv(settings.data_dir / "offices.csv")
    handbook = Handbook.from_json(settings.data_dir / "handbook.json")
    return AssistantService(settings, offices, handbook, StubLLMResponder())
