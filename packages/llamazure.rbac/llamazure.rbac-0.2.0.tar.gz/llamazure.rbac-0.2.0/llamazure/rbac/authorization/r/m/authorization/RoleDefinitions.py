# pylint: disable
# flake8: noqa
from __future__ import annotations
from enum import Enum
from typing import Annotated, List, Optional, Union

from pydantic import BaseModel, Field

from llamazure.azrest.models import AzList, ReadOnly, Req, default_list, default_dict



class RoleDefinitionFilter(BaseModel):
	"""Role Definitions filter"""

	roleName: Optional[str] = None
	type: Optional[str] = None

	def __eq__(self, o) -> bool:
		return (
			isinstance(o, self.__class__)
			and self.roleName == o.roleName
			and self.type == o.type
		)



class RoleDefinition(BaseModel):
	"""Role definition."""
	class Properties(BaseModel):
		"""Role definition properties."""

		roleName: Optional[str] = None
		description: Optional[str] = None
		type: Optional[str] = None
		permissions: Annotated[List[Permission],default_list] = []
		assignableScopes: Annotated[List[str],default_list] = []
		createdOn: ReadOnly[str] = None
		updatedOn: ReadOnly[str] = None
		createdBy: ReadOnly[str] = None
		updatedBy: ReadOnly[str] = None

		def __eq__(self, o) -> bool:
			return (
				isinstance(o, self.__class__)
				and self.roleName == o.roleName
				and self.description == o.description
				and self.type == o.type
				and self.permissions == o.permissions
				and self.assignableScopes == o.assignableScopes
			)


	rid: ReadOnly[str] = Field(alias="id", default=None)
	name: ReadOnly[str] = None
	type: ReadOnly[str] = None
	properties: Properties

	def __eq__(self, o) -> bool:
		return (
			isinstance(o, self.__class__)
			and self.properties == o.properties
		)



class Permission(BaseModel):
	"""Role definition permissions."""

	actions: Annotated[List[str],default_list] = []
	notActions: Annotated[List[str],default_list] = []
	dataActions: Annotated[List[str],default_list] = []
	notDataActions: Annotated[List[str],default_list] = []

	def __eq__(self, o) -> bool:
		return (
			isinstance(o, self.__class__)
			and self.actions == o.actions
			and self.notActions == o.notActions
			and self.dataActions == o.dataActions
			and self.notDataActions == o.notDataActions
		)



RoleDefinitionListResult = AzList[RoleDefinition]

PermissionGetResult = AzList[Permission]

RoleDefinitionFilter.model_rebuild()

RoleDefinition.model_rebuild()

Permission.model_rebuild()

RoleDefinitionListResult.model_rebuild()

PermissionGetResult.model_rebuild()


class AzPermissions:
	apiv = "2022-04-01"
	@staticmethod
	def ListForResourceGroup(resourceGroupName: str, subscriptionId: str) -> Req[PermissionGetResult]:
		"""Gets all permissions the caller has for a resource group."""
		r = Req.get(
			name="Permissions.ListForResourceGroup",
			path=f"/subscriptions/{subscriptionId}/resourcegroups/{resourceGroupName}/providers/Microsoft.Authorization/permissions",
			apiv="2022-04-01",
			ret_t=PermissionGetResult
		)

		return r

	@staticmethod
	def ListForResource(resourceGroupName: str, resourceProviderNamespace: str, parentResourcePath: str, resourceType: str, resourceName: str, subscriptionId: str) -> Req[PermissionGetResult]:
		"""Gets all permissions the caller has for a resource."""
		r = Req.get(
			name="Permissions.ListForResource",
			path=f"/subscriptions/{subscriptionId}/resourcegroups/{resourceGroupName}/providers/{resourceProviderNamespace}/{parentResourcePath}/{resourceType}/{resourceName}/providers/Microsoft.Authorization/permissions",
			apiv="2022-04-01",
			ret_t=PermissionGetResult
		)

		return r



class AzRoleDefinitions:
	apiv = "2022-04-01"
	@staticmethod
	def Get(scope: str, roleDefinitionId: str) -> Req[RoleDefinition]:
		"""Get role definition by name (GUID)."""
		r = Req.get(
			name="RoleDefinitions.Get",
			path=f"/{scope}/providers/Microsoft.Authorization/roleDefinitions/{roleDefinitionId}",
			apiv="2022-04-01",
			ret_t=RoleDefinition
		)

		return r

	@staticmethod
	def CreateOrUpdate(scope: str, roleDefinitionId: str, roleDefinition: RoleDefinition) -> Req[RoleDefinition]:
		"""Creates or updates a role definition."""
		r = Req.put(
			name="RoleDefinitions.CreateOrUpdate",
			path=f"/{scope}/providers/Microsoft.Authorization/roleDefinitions/{roleDefinitionId}",
			apiv="2022-04-01",
			body=roleDefinition,
			ret_t=RoleDefinition
		)

		return r

	@staticmethod
	def Delete(scope: str, roleDefinitionId: str) -> Req[Optional[RoleDefinition]]:
		"""Deletes a role definition."""
		r = Req.delete(
			name="RoleDefinitions.Delete",
			path=f"/{scope}/providers/Microsoft.Authorization/roleDefinitions/{roleDefinitionId}",
			apiv="2022-04-01",
			ret_t=Optional[RoleDefinition]
		)

		return r

	@staticmethod
	def List(scope: str, filter: Optional[str] = None) -> Req[RoleDefinitionListResult]:
		"""Get all role definitions that are applicable at scope and above."""
		r = Req.get(
			name="RoleDefinitions.List",
			path=f"/{scope}/providers/Microsoft.Authorization/roleDefinitions",
			apiv="2022-04-01",
			ret_t=RoleDefinitionListResult
		)
		if filter is not None:
			r = r.add_param("$filter", str(filter))

		return r

	@staticmethod
	def GetById(roleId: str) -> Req[RoleDefinition]:
		"""Gets a role definition by ID."""
		r = Req.get(
			name="RoleDefinitions.GetById",
			path=f"/{roleId}?disambiguation_dummy",
			apiv="2022-04-01",
			ret_t=RoleDefinition
		)

		return r

