from django.conf.urls import url, include

from rest_framework.routers import DefaultRouter
from rest_framework_jwt.views import obtain_jwt_token

from bag_transfer.api.views import AccessionViewSet, OrganizationViewSet, ArchivesViewSet, BAGLogViewSet, BagItProfileViewSet, UserViewSet

router = DefaultRouter()
router.register(r'accessions', AccessionViewSet, 'accession')
router.register(r'bagit_profiles', BagItProfileViewSet)
router.register(r'events', BAGLogViewSet)
router.register(r'orgs', OrganizationViewSet)
router.register(r'transfers', ArchivesViewSet, 'archives')
router.register(r'users', UserViewSet)

urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^get-token/', obtain_jwt_token),
]
