# pylint: disable
# flake8: noqa
from __future__ import annotations
from enum import Enum
from typing import Annotated, List, Optional, Union

from pydantic import BaseModel, Field

from llamazure.azrest.models import AzList, ReadOnly, Req, default_list, default_dict



class UserAssignedIdentities(BaseModel):
	"""The set of user assigned identities associated with the resource. The userAssignedIdentities dictionary keys will be ARM resource ids in the form: '/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.ManagedIdentity/userAssignedIdentities/{identityName}. The dictionary values can be empty objects ({}) in requests."""



	def __eq__(self, o) -> bool:
		return (
			isinstance(o, self.__class__)
		)



class UserAssignedIdentity(BaseModel):
	"""User assigned identity properties"""

	principalId: ReadOnly[str] = None
	clientId: ReadOnly[str] = None

	def __eq__(self, o) -> bool:
		return (
			isinstance(o, self.__class__)
		)



class ManagedServiceIdentity(BaseModel):
	"""Managed service identity (system assigned and/or user assigned identities)"""

	principalId: ReadOnly[str] = None
	tenantId: ReadOnly[str] = None
	type: Optional[str] = None
	userAssignedIdentities: Optional[UserAssignedIdentities] = None

	def __eq__(self, o) -> bool:
		return (
			isinstance(o, self.__class__)
			and self.type == o.type
			and self.userAssignedIdentities == o.userAssignedIdentities
		)



class SystemAssignedServiceIdentity(BaseModel):
	"""Managed service identity (either system assigned, or none)"""

	principalId: ReadOnly[str] = None
	tenantId: ReadOnly[str] = None
	type: Optional[str] = None

	def __eq__(self, o) -> bool:
		return (
			isinstance(o, self.__class__)
			and self.type == o.type
		)



UserAssignedIdentities.model_rebuild()

UserAssignedIdentity.model_rebuild()

ManagedServiceIdentity.model_rebuild()

SystemAssignedServiceIdentity.model_rebuild()


