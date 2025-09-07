from aws_cdk import (
    Stack,
    CfnOutput,
    aws_iam as iam,
    DefaultStackSynthesizer,
)
from constructs import Construct
import environments


# Create a Stack for GithubAccess for create a Roll en Differentes Enviroments
class GithubAccess(Stack):

    def __init__(
        self,
        scope: Construct,
        construct_id: str,
        github_org: str,
        repository_name: str,
        env_name: str,
        **kwargs
    ) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # DEV_ENV = environments.software_engineering["DEV"]
        # TESTING_ENV = environments.software_engineering["TESTING"]
        # PROD_ENV = environments.software_engineering["PROD"]

        # Parameters (passed directly from code)
        self.github_org = github_org
        self.repository_name = repository_name

        # Create OIDC Provider
        github_oidc = iam.CfnOIDCProvider(self, "GithubOidc",
            url="https://token.actions.githubusercontent.com",
            client_id_list=["sts.amazonaws.com"],
            thumbprint_list=["ffffffffffffffffffffffffffffffffffffffff"]
        )

        # Create IAM Role
        role = iam.Role(self, "GithubActionsRole",
            assumed_by=iam.FederatedPrincipal(
                federated=github_oidc.attr_arn,
                conditions={
                    "StringEquals": {"token.actions.githubusercontent.com:aud": "sts.amazonaws.com"},
                    "StringLike": {"token.actions.githubusercontent.com:sub": f"repo:{self.github_org}/{self.repository_name}:*"}
                },
                assume_role_action="sts:AssumeRoleWithWebIdentity"
            ),
            managed_policies=[iam.ManagedPolicy.from_aws_managed_policy_name("AdministratorAccess")]
        )

        # # Add cross-account assume role permissions ONLY FOR GLOBAL ACCOUNT
        # if env_name == "GLOBAL":
        #     for env in [DEV_ENV, TESTING_ENV, PROD_ENV]:
        #         for role_type in ["cfn-exec-role", "deploy-role", "file-publishing-role", "image-publishing-role", "lookup-role"]:
        #             resource_arn = f"arn:aws:iam::{env.account}:role/cdk-{DefaultStackSynthesizer.DEFAULT_QUALIFIER}-{role_type}-{env.account}-{env.region}"
        #             role.add_to_policy(
        #                 iam.PolicyStatement(
        #                     actions=["sts:AssumeRole"],
        #                     effect=iam.Effect.ALLOW,
        #                     resources=[resource_arn]
        #                 )
        #             )

        # Outputs
        CfnOutput(self, "RoleArn", value=role.role_arn)