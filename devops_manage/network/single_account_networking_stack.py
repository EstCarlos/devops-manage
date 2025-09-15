from aws_cdk import (
    Stack,
    CfnOutput,
    aws_route53 as route53,
    aws_route53_targets as targets,
    aws_certificatemanager as acm,
    aws_apigateway as apigateway,
    aws_ses as ses,
)
from constructs import Construct

class SingleAccountNetworkingStack(Stack):
    def __init__(
        self,
        scope: Construct,
        construct_id: str,
        domain_name: str,
        api_subdomain: str = "api",
        **kwargs
    ) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # 1) Hosted Zone pública del dominio (debe existir en Route 53)
        #    Si ya la tienes (compraste el dominio en Route 53), usa from_lookup:
        hosted_zone = route53.HostedZone.from_lookup(
            self,
            "HostedZone",
            domain_name=domain_name,
        )

        # 2) Certificado para el subdominio del API (Regional → cert en la misma región del API)
        api_fqdn = f"{api_subdomain}.{domain_name}"
        certificate = acm.Certificate(
            self,
            "ApiCertificate",
            domain_name=api_fqdn,
            validation=acm.CertificateValidation.from_dns(hosted_zone),
        )
        CfnOutput(self, "ApiCertificateArn", value=certificate.certificate_arn)

        # 3) API Gateway + Custom Domain
        api = apigateway.RestApi(
            self,
            "PublicApi",
            rest_api_name="PublicApi",
            description=f"Public API for {api_fqdn}",
            endpoint_types=[apigateway.EndpointType.REGIONAL],
            disable_execute_api_endpoint=True,  # solo por custom domain
        )

        # Add a minimal health endpoint so the API has at least one method
        health = api.root.add_resource("health")
        health.add_method(
            "GET",
            apigateway.MockIntegration(
                integration_responses=[
                    {
                        "statusCode": "200",
                        "responseTemplates": {"application/json": '{"status":"ok"}'}
                    }
                ],
                request_templates={"application/json": '{"status":"ok"}'}
            ),
            method_responses=[apigateway.MethodResponse(status_code="200")],
        )

        custom_domain = apigateway.DomainName(
            self,
            "ApiCustomDomain",
            domain_name=api_fqdn,
            certificate=certificate,
            endpoint_type=apigateway.EndpointType.REGIONAL,
        )

        apigateway.BasePathMapping(
            self,
            "ApiBasePathMapping",
            domain_name=custom_domain,
            rest_api=api,
        )

        # DNS A-ALIAS hacia el dominio del API
        route53.ARecord(
            self,
            "ApiAliasRecord",
            zone=hosted_zone,
            record_name=api_fqdn,
            target=route53.RecordTarget.from_alias(
                targets.ApiGatewayDomain(custom_domain)
            ),
        )

        CfnOutput(self, "ApiInvokeUrl", value=f"https://{api_fqdn}/")

        # # 4) SES: identidad de dominio (para enviar desde *@estcharls.com)
        # ses.EmailIdentity(
        #     self,
        #     "SesDomainIdentity",
        #     identity=ses.Identity.public_hosted_zone(hosted_zone),
        # )