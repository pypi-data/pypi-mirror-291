# pylint: disable
# flake8: noqa
from __future__ import annotations
from enum import Enum
from typing import Annotated, List, Optional, Union

from pydantic import BaseModel, Field

from llamazure.azrest.models import AzList, ReadOnly, Req, default_list, default_dict


from llamazure.tools.migrate.c.r.v3.managedidentity import ManagedServiceIdentity, UserAssignedIdentities
from llamazure.tools.migrate.c.r.v1.types import SystemData
class WorkbookResource(BaseModel):
	"""An azure resource object"""

	identity: Optional[ManagedServiceIdentity] = None
	kind: Optional[str] = None
	etag: Optional[str] = None
	tags: Optional[dict] = None
	location: str
	rid: ReadOnly[str] = Field(alias="id", default=None)
	name: ReadOnly[str] = None
	type: ReadOnly[str] = None

	def __eq__(self, o) -> bool:
		return (
			isinstance(o, self.__class__)
			and self.identity == o.identity
			and self.kind == o.kind
			and self.etag == o.etag
			and self.tags == o.tags
			and self.location == o.location
		)



class Workbook(BaseModel):
	"""A workbook definition."""
	class Properties(BaseModel):
		"""Properties that contain a workbook."""

		displayName: str
		serializedData: str
		version: Optional[str] = None
		timeModified: ReadOnly[str] = None
		category: str
		tags: Annotated[List[str],default_list] = []
		userId: ReadOnly[str] = None
		sourceId: Optional[str] = None
		storageUri: Optional[str] = None
		description: Optional[str] = None
		revision: ReadOnly[str] = None

		def __eq__(self, o) -> bool:
			return (
				isinstance(o, self.__class__)
				and self.displayName == o.displayName
				and self.serializedData == o.serializedData
				and self.version == o.version
				and self.category == o.category
				and self.tags == o.tags
				and self.sourceId == o.sourceId
				and self.storageUri == o.storageUri
				and self.description == o.description
			)


	properties: Properties
	systemData: Optional[SystemData] = None
	identity: Optional[ManagedServiceIdentity] = None
	kind: Optional[str] = None
	etag: Optional[str] = None
	tags: Optional[dict] = None
	location: str
	rid: ReadOnly[str] = Field(alias="id", default=None)
	name: ReadOnly[str] = None
	type: ReadOnly[str] = None

	def __eq__(self, o) -> bool:
		return (
			isinstance(o, self.__class__)
			and self.properties == o.properties
			and self.systemData == o.systemData
			and self.identity == o.identity
			and self.kind == o.kind
			and self.etag == o.etag
			and self.tags == o.tags
			and self.location == o.location
		)



class WorkbookUpdateParameters(BaseModel):
	"""The parameters that can be provided when updating workbook properties properties."""
	class Properties(BaseModel):
		"""Properties that contain a workbook for PATCH operation."""

		displayName: Optional[str] = None
		serializedData: Optional[str] = None
		category: Optional[str] = None
		tags: Annotated[List[str],default_list] = []
		description: Optional[str] = None
		revision: Optional[str] = None

		def __eq__(self, o) -> bool:
			return (
				isinstance(o, self.__class__)
				and self.displayName == o.displayName
				and self.serializedData == o.serializedData
				and self.category == o.category
				and self.tags == o.tags
				and self.description == o.description
				and self.revision == o.revision
			)


	kind: Optional[str] = None
	tags: Optional[dict] = None
	properties: Properties

	def __eq__(self, o) -> bool:
		return (
			isinstance(o, self.__class__)
			and self.kind == o.kind
			and self.tags == o.tags
			and self.properties == o.properties
		)



class WorkbookError(BaseModel):
	"""Error response."""

	error: Optional[WorkbookErrorDefinition] = None

	def __eq__(self, o) -> bool:
		return (
			isinstance(o, self.__class__)
			and self.error == o.error
		)



class WorkbookErrorDefinition(BaseModel):
	"""Error definition."""

	code: ReadOnly[str] = None
	message: ReadOnly[str] = None
	innererror: Optional[WorkbookInnerErrorTrace] = None

	def __eq__(self, o) -> bool:
		return (
			isinstance(o, self.__class__)
			and self.innererror == o.innererror
		)



class WorkbookInnerErrorTrace(BaseModel):
	"""Error details"""

	trace: Annotated[List[str],default_list] = []

	def __eq__(self, o) -> bool:
		return (
			isinstance(o, self.__class__)
			and self.trace == o.trace
		)



WorkbooksListResult = AzList[Workbook]

WorkbookResource.model_rebuild()

Workbook.model_rebuild()

WorkbookUpdateParameters.model_rebuild()

WorkbookError.model_rebuild()

WorkbookErrorDefinition.model_rebuild()

WorkbookInnerErrorTrace.model_rebuild()

WorkbooksListResult.model_rebuild()


class AzWorkbooks:
	apiv = "2023-06-01"
	@staticmethod
	def ListBySubscription(subscriptionId: str, category: str, tags: Optional[List[str]] = None, canFetchContent: Optional[bool] = None) -> Req[WorkbooksListResult]:
		"""Get all Workbooks defined within a specified subscription and category."""
		r = Req.get(
			name="Workbooks.ListBySubscription",
			path=f"/subscriptions/{subscriptionId}/providers/Microsoft.Insights/workbooks",
			apiv="2023-06-01",
			ret_t=WorkbooksListResult
		)
		if category is not None:
			r = r.add_param("category", str(category))
		if tags is not None:
			r = r.add_param("tags", str(tags))
		if canFetchContent is not None:
			r = r.add_param("canFetchContent", str(canFetchContent))

		return r

	@staticmethod
	def ListByResourceGroup(subscriptionId: str, resourceGroupName: str, category: str, tags: Optional[List[str]] = None, sourceId: Optional[str] = None, canFetchContent: Optional[bool] = None) -> Req[WorkbooksListResult]:
		"""Get all Workbooks defined within a specified resource group and category."""
		r = Req.get(
			name="Workbooks.ListByResourceGroup",
			path=f"/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.Insights/workbooks",
			apiv="2023-06-01",
			ret_t=WorkbooksListResult
		)
		if category is not None:
			r = r.add_param("category", str(category))
		if tags is not None:
			r = r.add_param("tags", str(tags))
		if sourceId is not None:
			r = r.add_param("sourceId", str(sourceId))
		if canFetchContent is not None:
			r = r.add_param("canFetchContent", str(canFetchContent))

		return r

	@staticmethod
	def Get(subscriptionId: str, resourceGroupName: str, resourceName: str, canFetchContent: Optional[bool] = None) -> Req[Workbook]:
		"""Get a single workbook by its resourceName."""
		r = Req.get(
			name="Workbooks.Get",
			path=f"/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.Insights/workbooks/{resourceName}",
			apiv="2023-06-01",
			ret_t=Workbook
		)
		if canFetchContent is not None:
			r = r.add_param("canFetchContent", str(canFetchContent))

		return r

	@staticmethod
	def CreateOrUpdate(subscriptionId: str, resourceGroupName: str, resourceName: str, workbookProperties: Workbook, sourceId: Optional[str] = None) -> Req[Workbook]:
		"""Create a new workbook."""
		r = Req.put(
			name="Workbooks.CreateOrUpdate",
			path=f"/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.Insights/workbooks/{resourceName}",
			apiv="2023-06-01",
			body=workbookProperties,
			ret_t=Workbook
		)
		if sourceId is not None:
			r = r.add_param("sourceId", str(sourceId))

		return r

	@staticmethod
	def Delete(subscriptionId: str, resourceGroupName: str, resourceName: str) -> Req[None]:
		"""Delete a workbook."""
		r = Req.delete(
			name="Workbooks.Delete",
			path=f"/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.Insights/workbooks/{resourceName}",
			apiv="2023-06-01",
			ret_t=None
		)

		return r

	@staticmethod
	def Update(subscriptionId: str, resourceGroupName: str, resourceName: str, WorkbookUpdateParameters: WorkbookUpdateParameters, sourceId: Optional[str] = None) -> Req[Workbook]:
		"""Updates a workbook that has already been added."""
		r = Req.patch(
			name="Workbooks.Update",
			path=f"/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.Insights/workbooks/{resourceName}",
			apiv="2023-06-01",
			body=WorkbookUpdateParameters,
			ret_t=Workbook
		)
		if sourceId is not None:
			r = r.add_param("sourceId", str(sourceId))

		return r

	@staticmethod
	def RevisionsList(subscriptionId: str, resourceGroupName: str, resourceName: str) -> Req[WorkbooksListResult]:
		"""Get the revisions for the workbook defined by its resourceName."""
		r = Req.get(
			name="Workbooks.RevisionsList",
			path=f"/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.Insights/workbooks/{resourceName}/revisions",
			apiv="2023-06-01",
			ret_t=WorkbooksListResult
		)

		return r

	@staticmethod
	def RevisionGet(subscriptionId: str, resourceGroupName: str, resourceName: str, revisionId: str) -> Req[Workbook]:
		"""Get a single workbook revision defined by its revisionId."""
		r = Req.get(
			name="Workbooks.RevisionGet",
			path=f"/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.Insights/workbooks/{resourceName}/revisions/{revisionId}",
			apiv="2023-06-01",
			ret_t=Workbook
		)

		return r

