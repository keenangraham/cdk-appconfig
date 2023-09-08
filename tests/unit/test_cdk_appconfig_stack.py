import aws_cdk as core
import aws_cdk.assertions as assertions

from cdk_appconfig.cdk_appconfig_stack import CdkAppconfigStack

# example tests. To run these tests, uncomment this file along with the example
# resource in cdk_appconfig/cdk_appconfig_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = CdkAppconfigStack(app, "cdk-appconfig")
    template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })
