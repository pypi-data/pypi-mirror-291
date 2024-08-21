from pydantic.v1 import BaseModel, Extra, Field, root_validator
from typing import Sequence, Literal
from .tomato import Tomato
from .sample import Sample
from .method import Method

from pathlib import Path
import yaml
import json


class Payload(BaseModel, extra=Extra.forbid):
    version: Literal["0.2"]
    tomato: Tomato = Field(default_factory=Tomato)
    """Additional configuration options for tomato."""

    sample: Sample
    """Specification of the experimental sample."""

    method: Sequence[Method]
    """A sequence of the experimental methods."""

    @root_validator(pre=True)
    def extract_samplefile(cls, values):  # pylint: disable=E0213
        """
        If ``samplefile`` is provided in ``values``, parse the file as ``sample``.
        """
        if "samplefile" in values:
            sf = Path(values.pop("samplefile"))
            assert sf.exists()
            with sf.open() as f:
                if sf.suffix in {".yml", ".yaml"}:
                    sample = yaml.safe_load(f)
                elif sf.suffix in {".json"}:
                    sample = json.load(f)
                else:
                    raise ValueError(f"Incorrect suffix of samplefile: '{sf}'")
            assert "sample" in sample
            values["sample"] = sample["sample"]
        return values

    @root_validator(pre=True)
    def extract_methodfile(cls, values):  # pylint: disable=E0213
        """
        If ``methodfile`` is provided in ``values``, parse the file as ``method``.
        """
        if "methodfile" in values:
            mf = Path(values.pop("methodfile"))
            assert mf.exists()
            with mf.open() as f:
                if mf.suffix in {".yml", ".yaml"}:
                    method = yaml.safe_load(f)
                elif mf.suffix in {".json"}:
                    method = json.load(f)
                else:
                    raise ValueError(f"Incorrect suffix of methodfile: '{mf}'")
            assert "method" in method
            values["method"] = method["method"]
        return values
