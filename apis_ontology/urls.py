from apis.urls import urlpatterns
from django.urls import path
from .views import CustomReferenceDetailView, TempTripleAutocomplete, TempEntityClassAutocomplete, CustomReferenceDeleteView
from django.contrib.auth.decorators import login_required

from django_versions.urls import urlpatterns as django_version_urlpatterns
urlpatterns = django_version_urlpatterns + urlpatterns

customurlpatterns = [
    path("bibsonomy/references/<int:pk>", login_required(CustomReferenceDetailView.as_view()), name='referencedetail'),
    path('bibsonomy/tempentityclass-autocomplete/', TempEntityClassAutocomplete.as_view(), name="tempentityclass-autocomplete",),
    path('bibsonomy/temptriple-autocomplete/', TempTripleAutocomplete.as_view(), name="temptriple-autocomplete",),
    path('bibsonomy/references/<int:pk>/delete', login_required(CustomReferenceDeleteView.as_view()), name='referencedelete'),
]
urlpatterns = customurlpatterns + urlpatterns
