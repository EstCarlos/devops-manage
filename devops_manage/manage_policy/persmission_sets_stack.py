from aws_cdk import (
    Stack,
    aws_iam as iam,
    aws_sso as sso,
)
from constructs import Construct

# AWS managed
readonly_policy = iam.ManagedPolicy.from_aws_managed_policy_name("ReadOnlyAccess")
readbilling_policy = iam.ManagedPolicy.from_aws_managed_policy_name("AWSBillingReadOnlyAccess")
admin_full_policy = iam.ManagedPolicy.from_aws_managed_policy_name("AdministratorAccess")

class SEPermissionSetStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, sso_instance_arn: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Permission Set para la cuenta DEV
        sso.CfnPermissionSet(
            self,
            "DEV_PERMISSION_SET",
            name="SE_DEV",
            description="Grants full-access to core AWS services. Intended for DEV account.",
            instance_arn=sso_instance_arn,
            customer_managed_policy_references=[
                {"name": "SE_CICDFullAccess"},
                {"name": "SE_DBFullAccess"},
                {"name": "SE_DevFullAccess"},
                {"name": "SE_DenyIAMRiskyActions"},
                {"name": "SE_CUSTOM_DEV"},
            ],
            managed_policies=[
                readonly_policy.managed_policy_arn,
                readbilling_policy.managed_policy_arn,
            ],
            session_duration="PT8H",
        )

        SE_DEVOPS = sso.CfnPermissionSet(
            self,
            'SE_DEVOPS_PERMISSION_SET',
            name='SE_DEVOPS',
            description='Grants full-access to core CI/CD services. Intended for a DevOps person.',
            instance_arn=sso_instance_arn,
            customer_managed_policy_references=[
                {"name": "SE_CICDFullAccess"},
            ],
            managed_policies=[
                readonly_policy.managed_policy_arn,
                readbilling_policy.managed_policy_arn
            ],
            session_duration='PT8H',
        )

        # Permission Set con permisos Full (Administrator) + Billing read-only
        sso.CfnPermissionSet(
            self,
            'SE_FULL_PERMISSION_SET',
            name='SE_FULL',
            description='Full administrative access to the account plus billing read access.',
            instance_arn=sso_instance_arn,
            managed_policies=[
                admin_full_policy.managed_policy_arn,
                readbilling_policy.managed_policy_arn,
            ],
            session_duration='PT8H',
        )