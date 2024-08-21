# pylint: disable
# flake8: noqa
from __future__ import annotations
from enum import Enum
from typing import Annotated, List, Optional, Union

from pydantic import BaseModel, Field

from llamazure.azrest.models import AzList, ReadOnly, Req, default_list, default_dict


from llamazure.tools.migrate.c.r.v5.types import OperationListResult, SystemData, Operation
class Dashboard(BaseModel):
	"""The shared dashboard resource definition."""
	class Properties(BaseModel):
		"""Dashboard Properties with Provisioning state"""

		lenses: Annotated[List[DashboardLens],default_list] = []
		metadata: Optional[dict] = None
		provisioningState: Optional[str] = None

		def __eq__(self, o) -> bool:
			return (
				isinstance(o, self.__class__)
				and self.lenses == o.lenses
				and self.metadata == o.metadata
				and self.provisioningState == o.provisioningState
			)


	properties: Properties
	tags: Optional[dict] = None
	location: str
	rid: ReadOnly[str] = Field(alias="id", default=None)
	name: ReadOnly[str] = None
	type: ReadOnly[str] = None
	systemData: Optional[SystemData] = None

	def __eq__(self, o) -> bool:
		return (
			isinstance(o, self.__class__)
			and self.properties == o.properties
			and self.tags == o.tags
			and self.location == o.location
			and self.systemData == o.systemData
		)



class DashboardLens(BaseModel):
	"""A dashboard lens."""

	order: int
	parts: Annotated[List[DashboardParts],default_list] = []
	metadata: Optional[dict] = None

	def __eq__(self, o) -> bool:
		return (
			isinstance(o, self.__class__)
			and self.order == o.order
			and self.parts == o.parts
			and self.metadata == o.metadata
		)



class DashboardPartMetadata(BaseModel):
	"""A dashboard part metadata."""

	type: Optional[str] = None

	def __eq__(self, o) -> bool:
		return (
			isinstance(o, self.__class__)
			and self.type == o.type
		)



class DashboardParts(BaseModel):
	"""A dashboard part."""

	position: Optional[DashboardPartsPosition] = None
	metadata: Optional[DashboardPartMetadata] = None

	def __eq__(self, o) -> bool:
		return (
			isinstance(o, self.__class__)
			and self.position == o.position
			and self.metadata == o.metadata
		)



class DashboardPartsPosition(BaseModel):
	"""The dashboard's part position."""

	x: int
	y: int
	rowSpan: int
	colSpan: int
	metadata: Optional[dict] = None

	def __eq__(self, o) -> bool:
		return (
			isinstance(o, self.__class__)
			and self.x == o.x
			and self.y == o.y
			and self.rowSpan == o.rowSpan
			and self.colSpan == o.colSpan
			and self.metadata == o.metadata
		)



class MarkdownPartMetadata(BaseModel):
	"""Markdown part metadata."""

	inputs: Annotated[List[dict],default_list] = []
	settings: Optional[MarkdownPartMetadataSettings] = None
	type: Optional[str] = None

	def __eq__(self, o) -> bool:
		return (
			isinstance(o, self.__class__)
			and self.inputs == o.inputs
			and self.settings == o.settings
			and self.type == o.type
		)



class MarkdownPartMetadataSettings(BaseModel):
	"""Markdown part settings."""

	content: Optional[MarkdownPartMetadataSettingsContent] = None

	def __eq__(self, o) -> bool:
		return (
			isinstance(o, self.__class__)
			and self.content == o.content
		)



class MarkdownPartMetadataSettingsContent(BaseModel):
	"""The content of markdown part."""

	settings: Optional[MarkdownPartMetadataSettingsContentSettings] = None

	def __eq__(self, o) -> bool:
		return (
			isinstance(o, self.__class__)
			and self.settings == o.settings
		)



class MarkdownPartMetadataSettingsContentSettings(BaseModel):
	"""The setting of the content of markdown part."""

	content: Optional[str] = None
	title: Optional[str] = None
	subtitle: Optional[str] = None
	markdownSource: Optional[int] = None
	markdownUri: Optional[str] = None

	def __eq__(self, o) -> bool:
		return (
			isinstance(o, self.__class__)
			and self.content == o.content
			and self.title == o.title
			and self.subtitle == o.subtitle
			and self.markdownSource == o.markdownSource
			and self.markdownUri == o.markdownUri
		)



class PatchableDashboard(BaseModel):
	"""The shared dashboard resource definition."""
	class Properties(BaseModel):
		"""The shared dashboard properties."""

		lenses: Annotated[List[DashboardLens],default_list] = []
		metadata: Optional[dict] = None

		def __eq__(self, o) -> bool:
			return (
				isinstance(o, self.__class__)
				and self.lenses == o.lenses
				and self.metadata == o.metadata
			)


	properties: Properties
	tags: Optional[dict] = None

	def __eq__(self, o) -> bool:
		return (
			isinstance(o, self.__class__)
			and self.properties == o.properties
			and self.tags == o.tags
		)



DashboardListResult = AzList[Dashboard]

Dashboard.model_rebuild()

DashboardLens.model_rebuild()

DashboardPartMetadata.model_rebuild()

DashboardParts.model_rebuild()

DashboardPartsPosition.model_rebuild()

MarkdownPartMetadata.model_rebuild()

MarkdownPartMetadataSettings.model_rebuild()

MarkdownPartMetadataSettingsContent.model_rebuild()

MarkdownPartMetadataSettingsContentSettings.model_rebuild()

PatchableDashboard.model_rebuild()

DashboardListResult.model_rebuild()


class AzOperations:
	apiv = "2020-09-01-preview"
	@staticmethod
	def List() -> Req[OperationListResult]:
		"""List the operations for the provider"""
		r = Req.get(
			name="Operations.List",
			path=f"/providers/Microsoft.Portal/operations",
			apiv="2020-09-01-preview",
			ret_t=OperationListResult
		)

		return r



class AzDashboards:
	apiv = "2020-09-01-preview"
	@staticmethod
	def ListBySubscription(subscriptionId: str) -> Req[DashboardListResult]:
		"""Gets all the dashboards within a subscription."""
		r = Req.get(
			name="Dashboards.ListBySubscription",
			path=f"/subscriptions/{subscriptionId}/providers/Microsoft.Portal/dashboards",
			apiv="2020-09-01-preview",
			ret_t=DashboardListResult
		)

		return r

	@staticmethod
	def ListByResourceGroup(subscriptionId: str, resourceGroupName: str) -> Req[DashboardListResult]:
		"""Gets all the Dashboards within a resource group."""
		r = Req.get(
			name="Dashboards.ListByResourceGroup",
			path=f"/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.Portal/dashboards",
			apiv="2020-09-01-preview",
			ret_t=DashboardListResult
		)

		return r

	@staticmethod
	def Get(subscriptionId: str, resourceGroupName: str, dashboardName: str) -> Req[Dashboard]:
		"""Gets the Dashboard."""
		r = Req.get(
			name="Dashboards.Get",
			path=f"/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.Portal/dashboards/{dashboardName}",
			apiv="2020-09-01-preview",
			ret_t=Dashboard
		)

		return r

	@staticmethod
	def CreateOrUpdate(subscriptionId: str, resourceGroupName: str, dashboardName: str, dashboard: Dashboard) -> Req[Dashboard]:
		"""Creates or updates a Dashboard."""
		r = Req.put(
			name="Dashboards.CreateOrUpdate",
			path=f"/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.Portal/dashboards/{dashboardName}",
			apiv="2020-09-01-preview",
			body=dashboard,
			ret_t=Dashboard
		)

		return r

	@staticmethod
	def Delete(subscriptionId: str, resourceGroupName: str, dashboardName: str) -> Req[None]:
		"""Deletes the Dashboard."""
		r = Req.delete(
			name="Dashboards.Delete",
			path=f"/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.Portal/dashboards/{dashboardName}",
			apiv="2020-09-01-preview",
			ret_t=None
		)

		return r

	@staticmethod
	def Update(subscriptionId: str, resourceGroupName: str, dashboardName: str, dashboard: PatchableDashboard) -> Req[Dashboard]:
		"""Updates an existing Dashboard."""
		r = Req.patch(
			name="Dashboards.Update",
			path=f"/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.Portal/dashboards/{dashboardName}",
			apiv="2020-09-01-preview",
			body=dashboard,
			ret_t=Dashboard
		)

		return r

