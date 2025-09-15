#!/usr/bin/env python3
import os
import aws_cdk as cdk
from devops_manage.devops_manage_stack import DevopsManageStack
from devops_manage.SES.ses_stack import SesStack
from devops_manage.manage_policy.persmission_sets_stack import SEPermissionSetStack
from devops_manage.manage_policy.iam_stack import SEIamPolicyStack
from devops_manage.Github.github_access_stack import GithubAccess
from devops_manage.network.single_account_networking_stack import SingleAccountNetworkingStack
import environments
from dotenv import load_dotenv
load_dotenv(override=True)
'''
Cómo obtener el SSO Instance ARN (ROOT)

aws sso-admin list-instances --profile root
'''

app = cdk.App()

domain = os.getenv("SE_SERVICES_DOMAIN") 
api_subdomain = os.getenv("API_SUBDOMAIN")

# Stack de SES para identidad de email
SesStack(
    app,
    "SesEmailIdentityStack",
    domain_name=domain,
    env=environments.software_engineering["DEV"],
)

#region Iam Permissions
# SSO Instance ARN desde contexto o variable de entorno
sso_instance_arn = os.getenv("SSO_INSTANCE_ARN")
if not sso_instance_arn:
    raise ValueError("Provide ssoInstanceArn in cdk.json context or SSO_INSTANCE_ARN env var")

# 1) Políticas IAM en la cuenta DEV
SEIamPolicyStack(
    app,
    "se-iam-dev",
    env=environments.software_engineering["DEV"],
)

# 2) Permission Sets en la cuenta ROOT
SEPermissionSetStack(
    app,
    "se-permission-sets-root",
    sso_instance_arn=sso_instance_arn,
    env=environments.software_engineering["ROOT"],
)
#endregion

# region CREATE CONNECTION GITHUB <> AWS
for env_name, environment in environments.software_engineering.items():
    # Skip creation of networking stacks in ROOT and GLOBAL accounts
    if env_name in ["ROOT"]:
        continue
    GithubAccess(
        app,
        f"GithubAccess-{env_name}",
        env=environment,
        stack_name=f"GithubAccess-{env_name}",
        description="This stack contains the connection between Github and AWS.",
        # This stack cannot be deleted by the CDK CLI or CloudFormation, but can be deleted manually.
        termination_protection=True,
        github_org="EstCarlos",
        repository_name="*",
        env_name=env_name 
    )

# endregion 


#region NETWORKING
SingleAccountNetworkingStack(
    app,
    "se-account-networking",
    domain_name=domain,
    api_subdomain=api_subdomain,
    env=environments.software_engineering["DEV"]
)
#endregion
app.synth()
