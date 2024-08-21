# pylint: disable
# flake8: noqa
from __future__ import annotations
from enum import Enum
from typing import Annotated, List, Optional, Union

from pydantic import BaseModel, Field

from llamazure.azrest.models import AzList, ReadOnly, Req, default_list, default_dict



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



class Principal(BaseModel):
	"""The name of the entity last modified it"""

	rid: Optional[str] = Field(alias="id", default=None)
	displayName: Optional[str] = None
	type: Optional[str] = None
	email: Optional[str] = None

	def __eq__(self, o) -> bool:
		return (
			isinstance(o, self.__class__)
			and self.rid == o.rid
			and self.displayName == o.displayName
			and self.type == o.type
			and self.email == o.email
		)



class RoleManagementPolicyRule(BaseModel):
	"""The role management policy rule."""

	rid: Optional[str] = Field(alias="id", default=None)
	ruleType: Optional[str] = None
	target: Optional[RoleManagementPolicyRuleTarget] = None

	def __eq__(self, o) -> bool:
		return (
			isinstance(o, self.__class__)
			and self.rid == o.rid
			and self.ruleType == o.ruleType
			and self.target == o.target
		)



class RoleManagementPolicyApprovalRule(BaseModel):
	"""The role management policy approval rule."""

	setting: Optional[ApprovalSettings] = None
	rid: Optional[str] = Field(alias="id", default=None)
	ruleType: Optional[str] = None
	target: Optional[RoleManagementPolicyRuleTarget] = None

	def __eq__(self, o) -> bool:
		return (
			isinstance(o, self.__class__)
			and self.setting == o.setting
			and self.rid == o.rid
			and self.ruleType == o.ruleType
			and self.target == o.target
		)



class ApprovalSettings(BaseModel):
	"""The approval settings."""

	isApprovalRequired: Optional[bool] = None
	isApprovalRequiredForExtension: Optional[bool] = None
	isRequestorJustificationRequired: Optional[bool] = None
	approvalMode: Optional[str] = None
	approvalStages: Annotated[List[ApprovalStage],default_list] = []

	def __eq__(self, o) -> bool:
		return (
			isinstance(o, self.__class__)
			and self.isApprovalRequired == o.isApprovalRequired
			and self.isApprovalRequiredForExtension == o.isApprovalRequiredForExtension
			and self.isRequestorJustificationRequired == o.isRequestorJustificationRequired
			and self.approvalMode == o.approvalMode
			and self.approvalStages == o.approvalStages
		)



class ApprovalStage(BaseModel):
	"""The approval stage."""

	approvalStageTimeOutInDays: Optional[int] = None
	isApproverJustificationRequired: Optional[bool] = None
	escalationTimeInMinutes: Optional[int] = None
	primaryApprovers: Annotated[List[UserSet],default_list] = []
	isEscalationEnabled: Optional[bool] = None
	escalationApprovers: Annotated[List[UserSet],default_list] = []

	def __eq__(self, o) -> bool:
		return (
			isinstance(o, self.__class__)
			and self.approvalStageTimeOutInDays == o.approvalStageTimeOutInDays
			and self.isApproverJustificationRequired == o.isApproverJustificationRequired
			and self.escalationTimeInMinutes == o.escalationTimeInMinutes
			and self.primaryApprovers == o.primaryApprovers
			and self.isEscalationEnabled == o.isEscalationEnabled
			and self.escalationApprovers == o.escalationApprovers
		)



class UserSet(BaseModel):
	"""The detail of a user."""

	userType: Optional[str] = None
	isBackup: Optional[bool] = None
	rid: Optional[str] = Field(alias="id", default=None)
	description: Optional[str] = None

	def __eq__(self, o) -> bool:
		return (
			isinstance(o, self.__class__)
			and self.userType == o.userType
			and self.isBackup == o.isBackup
			and self.rid == o.rid
			and self.description == o.description
		)



class RoleManagementPolicyAuthenticationContextRule(BaseModel):
	"""The role management policy authentication context rule."""

	isEnabled: Optional[bool] = None
	claimValue: Optional[str] = None
	rid: Optional[str] = Field(alias="id", default=None)
	ruleType: Optional[str] = None
	target: Optional[RoleManagementPolicyRuleTarget] = None

	def __eq__(self, o) -> bool:
		return (
			isinstance(o, self.__class__)
			and self.isEnabled == o.isEnabled
			and self.claimValue == o.claimValue
			and self.rid == o.rid
			and self.ruleType == o.ruleType
			and self.target == o.target
		)



class RoleManagementPolicyEnablementRule(BaseModel):
	"""The role management policy enablement rule."""

	enabledRules: Annotated[List[str],default_list] = []
	rid: Optional[str] = Field(alias="id", default=None)
	ruleType: Optional[str] = None
	target: Optional[RoleManagementPolicyRuleTarget] = None

	def __eq__(self, o) -> bool:
		return (
			isinstance(o, self.__class__)
			and self.enabledRules == o.enabledRules
			and self.rid == o.rid
			and self.ruleType == o.ruleType
			and self.target == o.target
		)



class RoleManagementPolicyExpirationRule(BaseModel):
	"""The role management policy expiration rule."""

	isExpirationRequired: Optional[bool] = None
	maximumDuration: Optional[str] = None
	rid: Optional[str] = Field(alias="id", default=None)
	ruleType: Optional[str] = None
	target: Optional[RoleManagementPolicyRuleTarget] = None

	def __eq__(self, o) -> bool:
		return (
			isinstance(o, self.__class__)
			and self.isExpirationRequired == o.isExpirationRequired
			and self.maximumDuration == o.maximumDuration
			and self.rid == o.rid
			and self.ruleType == o.ruleType
			and self.target == o.target
		)



class RoleManagementPolicyNotificationRule(BaseModel):
	"""The role management policy notification rule."""

	notificationType: Optional[str] = None
	notificationLevel: Optional[str] = None
	recipientType: Optional[str] = None
	notificationRecipients: Annotated[List[str],default_list] = []
	isDefaultRecipientsEnabled: Optional[bool] = None
	rid: Optional[str] = Field(alias="id", default=None)
	ruleType: Optional[str] = None
	target: Optional[RoleManagementPolicyRuleTarget] = None

	def __eq__(self, o) -> bool:
		return (
			isinstance(o, self.__class__)
			and self.notificationType == o.notificationType
			and self.notificationLevel == o.notificationLevel
			and self.recipientType == o.recipientType
			and self.notificationRecipients == o.notificationRecipients
			and self.isDefaultRecipientsEnabled == o.isDefaultRecipientsEnabled
			and self.rid == o.rid
			and self.ruleType == o.ruleType
			and self.target == o.target
		)



class RoleManagementPolicyRuleTarget(BaseModel):
	"""The role management policy rule target."""

	caller: Optional[str] = None
	operations: Annotated[List[str],default_list] = []
	level: Optional[str] = None
	targetObjects: Annotated[List[str],default_list] = []
	inheritableSettings: Annotated[List[str],default_list] = []
	enforcedSettings: Annotated[List[str],default_list] = []

	def __eq__(self, o) -> bool:
		return (
			isinstance(o, self.__class__)
			and self.caller == o.caller
			and self.operations == o.operations
			and self.level == o.level
			and self.targetObjects == o.targetObjects
			and self.inheritableSettings == o.inheritableSettings
			and self.enforcedSettings == o.enforcedSettings
		)



Permission.model_rebuild()

Principal.model_rebuild()

RoleManagementPolicyRule.model_rebuild()

RoleManagementPolicyApprovalRule.model_rebuild()

ApprovalSettings.model_rebuild()

ApprovalStage.model_rebuild()

UserSet.model_rebuild()

RoleManagementPolicyAuthenticationContextRule.model_rebuild()

RoleManagementPolicyEnablementRule.model_rebuild()

RoleManagementPolicyExpirationRule.model_rebuild()

RoleManagementPolicyNotificationRule.model_rebuild()

RoleManagementPolicyRuleTarget.model_rebuild()


