from drf_yasg.generators import OpenAPISchemaGenerator
from drf_yasg.inspectors import SwaggerAutoSchema


class CustomAutoSchema(SwaggerAutoSchema):
    def get_tags(self, operation_keys=None):
        tags = self.overrides.get('tags', None) or getattr(self.view,
                                                           'swagger_tags', [])
        if not tags:
            tags = [operation_keys[0]]

        return tags


class CustomOpenAPISchemaGenerator(OpenAPISchemaGenerator):
    def get_schema(self, request=None, public=False):
        swagger = super().get_schema(request=request, public=public)
        swagger.tags = [
            {
                "name": "App",
            },
            {
                "name": "Plan",
            },
            {
                "name": "Subscription",
            },
        ]

        return swagger
