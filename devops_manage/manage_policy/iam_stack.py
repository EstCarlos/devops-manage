from aws_cdk import (
    Stack,
    aws_iam as iam,
)
from constructs import Construct
import json

def policy_reader(filename: str):
    with open(f"devops_manage/manage_policy/policy_definitions/{filename}", "r") as f:
        return json.load(f)

class SEIamPolicyStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Políticas customer-managed que usará el Permission Set SE_DEV
        iam.CfnManagedPolicy(
            self,
            "CICDFullAccess",
            policy_document=policy_reader("SE_CICDFullAccess.json"),
            managed_policy_name="SE_CICDFullAccess",
            description="Full access to CI/CD services",
        )
        iam.CfnManagedPolicy(
            self,
            "DBFullAccess",
            policy_document=policy_reader("SE_DBFullAccess.json"),
            managed_policy_name="SE_DBFullAccess",
            description="Full access to DB and storage services",
        )
        iam.CfnManagedPolicy(
            self,
            "DevFullAccess",
            policy_document=policy_reader("SE_DevFullAccess.json"),
            managed_policy_name="SE_DevFullAccess",
            description="Full access to dev services",
        )
        iam.CfnManagedPolicy(
            self,
            "DenyIAMRiskyActions",
            policy_document=policy_reader("SE_DenyIAMRiskyActions.json"),
            managed_policy_name="SE_DenyIAMRiskyActions",
            description="Deny risky IAM actions and editing SE_* policies",
        )
        iam.CfnManagedPolicy(
            self,
            "SECustomDEV",
            policy_document=policy_reader("SE_CUSTOM_DEV.json"),
            managed_policy_name="SE_CUSTOM_DEV",
            description="Custom permissions for DEV account",
        )

        # # region SE CUSTOM POLICY FOR EACH ORGANIZATION UNIT
        # for environment_name in environments.software_engineering:
        #     # Skip ROOT account
        #     if environment_name in ['ROOT']: continue
        #     # Conditionally create a custom policy for each environment
        #     if self.account == environments.software_engineering[environment_name].account:
        #         custom_policy = iam.CfnManagedPolicy(
        #             self,
        #             f"CUSTOM_{environment_name}",
        #             policy_document=policy_reader(f'SE_CUSTOM_{environment_name}.json'),
        #             description=f"Special and carefully designed policies for the SE {environment_name} Organization Unit",
        #             managed_policy_name=f"SE_CUSTOM_{environment_name}",
        #         )

        # # endregion