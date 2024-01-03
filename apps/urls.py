from django.contrib import admin
from django.urls import path, include
from graphene_django.views import GraphQLView

from apps.workspaces.urls import workspace_router

# custom_urlpatterns = [
#     path('', include(workspace_router.urls)),
# ]

urlpatterns = [
    # path('api/', include(custom_urlpatterns)),
    path('admin/', admin.site.urls),
    path("graphql/", GraphQLView.as_view(graphiql=True)),
]
