# coding: utf-8

"""
    GraphScope FLEX HTTP SERVICE API

    This is a specification for GraphScope FLEX HTTP service based on the OpenAPI 3.0 specification. You can find out more details about specification at [doc](https://swagger.io/specification/v3/).  Some useful links: - [GraphScope Repository](https://github.com/alibaba/GraphScope) - [The Source API definition for GraphScope Interactive](https://github.com/GraphScope/portal/tree/main/httpservice)

    The version of the OpenAPI document: 1.0.0
    Contact: graphscope@alibaba-inc.com
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


from __future__ import annotations
import pprint
import re  # noqa: F401
import json

from pydantic import BaseModel, StrictStr, field_validator
from typing import Any, ClassVar, Dict, List, Optional
from typing import Optional, Set
from typing_extensions import Self

class BaseEdgeTypeVertexTypePairRelationsInnerXCsrParams(BaseModel):
    """
    Used for storage optimization
    """ # noqa: E501
    edge_storage_strategy: Optional[StrictStr] = None
    __properties: ClassVar[List[str]] = ["edge_storage_strategy"]

    @field_validator('edge_storage_strategy')
    def edge_storage_strategy_validate_enum(cls, value):
        """Validates the enum"""
        if value is None:
            return value

        if value not in set(['ONLY_IN', 'ONLY_OUT', 'BOTH_OUT_IN']):
            raise ValueError("must be one of enum values ('ONLY_IN', 'ONLY_OUT', 'BOTH_OUT_IN')")
        return value

    model_config = {
        "populate_by_name": True,
        "validate_assignment": True,
        "protected_namespaces": (),
    }


    def to_str(self) -> str:
        """Returns the string representation of the model using alias"""
        return pprint.pformat(self.model_dump(by_alias=True))

    def to_json(self) -> str:
        """Returns the JSON representation of the model using alias"""
        # TODO: pydantic v2: use .model_dump_json(by_alias=True, exclude_unset=True) instead
        return json.dumps(self.to_dict())

    @classmethod
    def from_json(cls, json_str: str) -> Optional[Self]:
        """Create an instance of BaseEdgeTypeVertexTypePairRelationsInnerXCsrParams from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self) -> Dict[str, Any]:
        """Return the dictionary representation of the model using alias.

        This has the following differences from calling pydantic's
        `self.model_dump(by_alias=True)`:

        * `None` is only added to the output dict for nullable fields that
          were set at model initialization. Other fields with value `None`
          are ignored.
        """
        excluded_fields: Set[str] = set([
        ])

        _dict = self.model_dump(
            by_alias=True,
            exclude=excluded_fields,
            exclude_none=True,
        )
        return _dict

    @classmethod
    def from_dict(cls, obj: Optional[Dict[str, Any]]) -> Optional[Self]:
        """Create an instance of BaseEdgeTypeVertexTypePairRelationsInnerXCsrParams from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate({
            "edge_storage_strategy": obj.get("edge_storage_strategy")
        })
        return _obj


