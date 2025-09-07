from aws_cdk import (
	Stack,
	aws_ses as ses,
)
from constructs import Construct


class SesStack(Stack):
	"""Stack para crear una identidad de SES de tipo Email Address.

	Al desplegar, AWS SES enviará un correo a la dirección para verificación.
	"""

	def __init__(self, scope: Construct, construct_id: str, *, email: str, **kwargs) -> None:  # type: ignore[override]
		super().__init__(scope, construct_id, **kwargs)

		# Creación de la identidad de correo electrónico
		ses.EmailIdentity(
			self,
			"EmailIdentity",
			identity=ses.Identity.email(email),
		)
