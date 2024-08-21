# pylint: disable
# flake8: noqa
from __future__ import annotations
from enum import Enum
from typing import Annotated, List, Optional, Union

from pydantic import BaseModel, Field

from llamazure.azrest.models import AzList, ReadOnly, Req, default_list, default_dict



class ValidationResponseErrorInfo(BaseModel):
	"""Failed validation result details"""

	code: ReadOnly[str] = None
	message: ReadOnly[str] = None

	def __eq__(self, o) -> bool:
		return (
			isinstance(o, self.__class__)
		)



class ValidationResponse(BaseModel):
	"""Validation response"""

	isValid: ReadOnly[bool] = None
	errorInfo: Optional[ValidationResponseErrorInfo] = None

	def __eq__(self, o) -> bool:
		return (
			isinstance(o, self.__class__)
			and self.errorInfo == o.errorInfo
		)



class RoleAssignmentFilter(BaseModel):
	"""Role Assignments filter"""

	principalId: Optional[str] = None

	def __eq__(self, o) -> bool:
		return (
			isinstance(o, self.__class__)
			and self.principalId == o.principalId
		)



class RoleAssignment(BaseModel):
	"""Role Assignments"""
	class Properties(BaseModel):
		"""Role assignment properties."""

		scope: ReadOnly[str] = None
		roleDefinitionId: str
		principalId: str
		principalType: Optional[str] = None
		description: Optional[str] = None
		condition: Optional[str] = None
		conditionVersion: Optional[str] = None
		createdOn: ReadOnly[str] = None
		updatedOn: ReadOnly[str] = None
		createdBy: ReadOnly[str] = None
		updatedBy: ReadOnly[str] = None
		delegatedManagedIdentityResourceId: Optional[str] = None

		def __eq__(self, o) -> bool:
			return (
				isinstance(o, self.__class__)
				and self.roleDefinitionId == o.roleDefinitionId
				and self.principalId == o.principalId
				and self.principalType == o.principalType
				and self.description == o.description
				and self.condition == o.condition
				and self.conditionVersion == o.conditionVersion
				and self.delegatedManagedIdentityResourceId == o.delegatedManagedIdentityResourceId
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



class RoleAssignmentCreateParameters(BaseModel):
	"""Role assignment create parameters."""
	class Properties(BaseModel):
		"""Role assignment properties."""

		scope: ReadOnly[str] = None
		roleDefinitionId: str
		principalId: str
		principalType: Optional[str] = None
		description: Optional[str] = None
		condition: Optional[str] = None
		conditionVersion: Optional[str] = None
		createdOn: ReadOnly[str] = None
		updatedOn: ReadOnly[str] = None
		createdBy: ReadOnly[str] = None
		updatedBy: ReadOnly[str] = None
		delegatedManagedIdentityResourceId: Optional[str] = None

		def __eq__(self, o) -> bool:
			return (
				isinstance(o, self.__class__)
				and self.roleDefinitionId == o.roleDefinitionId
				and self.principalId == o.principalId
				and self.principalType == o.principalType
				and self.description == o.description
				and self.condition == o.condition
				and self.conditionVersion == o.conditionVersion
				and self.delegatedManagedIdentityResourceId == o.delegatedManagedIdentityResourceId
			)


	properties: Properties

	def __eq__(self, o) -> bool:
		return (
			isinstance(o, self.__class__)
			and self.properties == o.properties
		)



RoleAssignmentListResult = AzList[RoleAssignment]

ValidationResponseErrorInfo.model_rebuild()

ValidationResponse.model_rebuild()

RoleAssignmentFilter.model_rebuild()

RoleAssignment.model_rebuild()

RoleAssignmentCreateParameters.model_rebuild()

RoleAssignmentListResult.model_rebuild()


class AzRoleAssignments:
	apiv = "2022-04-01"
	@staticmethod
	def ListForSubscription(subscriptionId: str, filter: Optional[str] = None, tenantId: Optional[str] = None) -> Req[RoleAssignmentListResult]:
		"""List all role assignments that apply to a subscription."""
		r = Req.get(
			name="RoleAssignments.ListForSubscription",
			path=f"/subscriptions/{subscriptionId}/providers/Microsoft.Authorization/roleAssignments",
			apiv="2022-04-01",
			ret_t=RoleAssignmentListResult
		)
		if filter is not None:
			r = r.add_param("$filter", str(filter))
		if tenantId is not None:
			r = r.add_param("tenantId", str(tenantId))

		return r

	@staticmethod
	def ListForResourceGroup(subscriptionId: str, resourceGroupName: str, filter: Optional[str] = None, tenantId: Optional[str] = None) -> Req[RoleAssignmentListResult]:
		"""List all role assignments that apply to a resource group."""
		r = Req.get(
			name="RoleAssignments.ListForResourceGroup",
			path=f"/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.Authorization/roleAssignments",
			apiv="2022-04-01",
			ret_t=RoleAssignmentListResult
		)
		if filter is not None:
			r = r.add_param("$filter", str(filter))
		if tenantId is not None:
			r = r.add_param("tenantId", str(tenantId))

		return r

	@staticmethod
	def ListForResource(subscriptionId: str, resourceGroupName: str, resourceProviderNamespace: str, resourceType: str, resourceName: str, filter: Optional[str] = None, tenantId: Optional[str] = None) -> Req[RoleAssignmentListResult]:
		"""List all role assignments that apply to a resource."""
		r = Req.get(
			name="RoleAssignments.ListForResource",
			path=f"/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/{resourceProviderNamespace}/{resourceType}/{resourceName}/providers/Microsoft.Authorization/roleAssignments",
			apiv="2022-04-01",
			ret_t=RoleAssignmentListResult
		)
		if filter is not None:
			r = r.add_param("$filter", str(filter))
		if tenantId is not None:
			r = r.add_param("tenantId", str(tenantId))

		return r

	@staticmethod
	def Get(scope: str, roleAssignmentName: str, tenantId: Optional[str] = None) -> Req[RoleAssignment]:
		"""Get a role assignment by scope and name."""
		r = Req.get(
			name="RoleAssignments.Get",
			path=f"/{scope}/providers/Microsoft.Authorization/roleAssignments/{roleAssignmentName}",
			apiv="2022-04-01",
			ret_t=RoleAssignment
		)
		if tenantId is not None:
			r = r.add_param("tenantId", str(tenantId))

		return r

	@staticmethod
	def Create(scope: str, roleAssignmentName: str, parameters: RoleAssignmentCreateParameters) -> Req[RoleAssignment]:
		"""Create or update a role assignment by scope and name."""
		r = Req.put(
			name="RoleAssignments.Create",
			path=f"/{scope}/providers/Microsoft.Authorization/roleAssignments/{roleAssignmentName}",
			apiv="2022-04-01",
			body=parameters,
			ret_t=RoleAssignment
		)

		return r

	@staticmethod
	def Delete(scope: str, roleAssignmentName: str, tenantId: Optional[str] = None) -> Req[Optional[RoleAssignment]]:
		"""Delete a role assignment by scope and name."""
		r = Req.delete(
			name="RoleAssignments.Delete",
			path=f"/{scope}/providers/Microsoft.Authorization/roleAssignments/{roleAssignmentName}",
			apiv="2022-04-01",
			ret_t=Optional[RoleAssignment]
		)
		if tenantId is not None:
			r = r.add_param("tenantId", str(tenantId))

		return r

	@staticmethod
	def ListForScope(scope: str, filter: Optional[str] = None, tenantId: Optional[str] = None, skipToken: Optional[str] = None) -> Req[RoleAssignmentListResult]:
		"""List all role assignments that apply to a scope."""
		r = Req.get(
			name="RoleAssignments.ListForScope",
			path=f"/{scope}/providers/Microsoft.Authorization/roleAssignments",
			apiv="2022-04-01",
			ret_t=RoleAssignmentListResult
		)
		if filter is not None:
			r = r.add_param("$filter", str(filter))
		if tenantId is not None:
			r = r.add_param("tenantId", str(tenantId))
		if skipToken is not None:
			r = r.add_param("$skipToken", str(skipToken))

		return r

	@staticmethod
	def GetById(roleAssignmentId: str, tenantId: Optional[str] = None) -> Req[RoleAssignment]:
		"""Get a role assignment by ID."""
		r = Req.get(
			name="RoleAssignments.GetById",
			path=f"/{roleAssignmentId}",
			apiv="2022-04-01",
			ret_t=RoleAssignment
		)
		if tenantId is not None:
			r = r.add_param("tenantId", str(tenantId))

		return r

	@staticmethod
	def CreateById(roleAssignmentId: str, parameters: RoleAssignmentCreateParameters) -> Req[RoleAssignment]:
		"""Create or update a role assignment by ID."""
		r = Req.put(
			name="RoleAssignments.CreateById",
			path=f"/{roleAssignmentId}",
			apiv="2022-04-01",
			body=parameters,
			ret_t=RoleAssignment
		)

		return r

	@staticmethod
	def DeleteById(roleAssignmentId: str, tenantId: Optional[str] = None) -> Req[Optional[RoleAssignment]]:
		"""Delete a role assignment by ID."""
		r = Req.delete(
			name="RoleAssignments.DeleteById",
			path=f"/{roleAssignmentId}",
			apiv="2022-04-01",
			ret_t=Optional[RoleAssignment]
		)
		if tenantId is not None:
			r = r.add_param("tenantId", str(tenantId))

		return r

