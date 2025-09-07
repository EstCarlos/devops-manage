```

self.lambda_layer = lambda_.LayerVersion(
            self,
            "lambda-layers",
            # Run local-build.sh to see this folder
            code=lambda_.Code.from_asset("dependencies"),
        )

        
self.lambda_function = lambda_.Function(
    layers=[self.lambda_layer]
)

```