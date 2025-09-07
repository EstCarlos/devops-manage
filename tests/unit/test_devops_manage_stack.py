import aws_cdk as core
import aws_cdk.assertions as assertions

from devops_manage.devops_manage_stack import DevopsManageStack
from devops_manage.SES.ses_stack import SesStack

# example tests. To run these tests, uncomment this file along with the example
# resource in devops_manage/devops_manage_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = DevopsManageStack(app, "devops-manage")
    template = assertions.Template.from_stack(stack)
# Test para verificar que la identidad de SES se crea
def test_ses_email_identity_created():
    app = core.App()
    ses_stack = SesStack(app, "TestSesStack", email="example@test.com")
    template = assertions.Template.from_stack(ses_stack)
    template.resource_count_is("AWS::SES::EmailIdentity", 1)


#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })
