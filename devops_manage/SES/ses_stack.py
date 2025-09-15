from aws_cdk import (
	Stack,
	aws_ses as ses,
	aws_route53 as route53,
)
from constructs import Construct


class SesStack(Stack):
	"""Stack para crear una identidad de SES de tipo Email Address.

	Al desplegar, AWS SES enviará un correo a la dirección para verificación.
	"""

	def __init__(self, scope: Construct, construct_id: str, *, domain_name: str, **kwargs) -> None:  # type: ignore[override]
		super().__init__(scope, construct_id, **kwargs)

		# # Creación de la identidad de correo electrónico
		# ses.EmailIdentity(
		# 	self,
		# 	"EmailIdentity",
		# 	identity=ses.Identity.email(email),
		# )

		#    Si ya la tienes (compraste el dominio en Route 53), usa from_lookup:
		hosted_zone = route53.HostedZone.from_lookup(
			self,
			"HostedZone",
			domain_name=domain_name,
		)
	
		# 4) SES: identidad de dominio (para enviar desde *@estcharls.com)
		ses.EmailIdentity(
			self,
			"SesDomainIdentity",
			identity=ses.Identity.public_hosted_zone(hosted_zone),
		)