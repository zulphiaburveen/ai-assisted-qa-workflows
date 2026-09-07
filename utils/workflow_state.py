from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class WorkflowState:
    """
    Shared workflow state.
    Every module reads from and writes to this object.
    """

    artifacts: dict = field(default_factory=dict)

    def add_artifact(self, key: str, value):
        self.artifacts[key] = value

        Path("artifacts").mkdir(exist_ok=True)

        extension = "md"

        if key.endswith("_json"):
            extension = "json"

        elif key.endswith("_ts"):
            extension = "ts"

        with open(
            f"artifacts/{key}.{extension}",
            "w",
            encoding="utf-8",
        ) as file:
            file.write(str(value))

    def get_artifact(self, key: str):
        return self.artifacts.get(key)