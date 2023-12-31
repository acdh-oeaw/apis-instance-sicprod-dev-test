from apis_acdhch_default_settings.settings import *
import re
import dj_database_url
import os


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
REDMINE_ID = 21704
APIS_LIST_VIEWS_ALLOWED = False
APIS_DETAIL_VIEWS_ALLOWED = False
FEATURED_COLLECTION_NAME = "FEATURED"
# MAIN_TEXT_NAME = "ÖBL Haupttext"
BIRTH_REL_NAME = "geboren in"
DEATH_REL_NAME = "verstorben in"
APIS_LOCATED_IN_ATTR = ["located in"]
APIS_BASE_URI = "https://sicprod.acdh.oeaw.ac.at/"
# APIS_OEBL_BIO_COLLECTION = "ÖBL Biographie"

APIS_SKOSMOS = {
    "url": os.environ.get("APIS_SKOSMOS", "https://vocabs.acdh-dev.oeaw.ac.at"),
    "vocabs-name": os.environ.get("APIS_SKOSMOS_THESAURUS", "apisthesaurus"),
    "description": "Thesaurus of the APIS project. Used to type entities and relations.",
}

APIS_BIBSONOMY = [{
   'type': 'zotero', #or zotero
   'url': 'https://api.zotero.org', #url of the bibsonomy instance or zotero.org
   'user': os.environ.get('APIS_BIBSONOMY_USER'), #for zotero use the user id number found in settings
   'API key': os.environ.get('APIS_BIBSONOMY_PASSWORD'),
   'group': '4853010'
}]
APIS_BIBSONOMY_FIELDS = ['self']
APIS_AUTOCOMPLETE_SETTINGS = "apis_ontology.settings.autocomplete_settings"

ALLOWED_HOSTS = re.sub(
    r"https?://",
    "",
    os.environ.get("ALLOWED_HOSTS", "localhost,127.0.0.1,sicprod.acdh-dev.oeaw.ac.at"),
).split(",")
# You need to allow '10.0.0.0/8' for service health checks.

ALLOWED_CIDR_NETS = ["10.0.0.0/8", "127.0.0.0/8"]

REST_FRAMEWORK["DEFAULT_PERMISSION_CLASSES"] = (
    # "rest_framework.permissions.DjangoModelPermissions",
    "rest_framework.permissions.IsAuthenticated",
    # "rest_framework.permissions.DjangoObjectPermissions",
    # use IsAuthenticated for every logged in user to have global edit rights
)

# HAYSTACK_DEFAULT_OPERATOR = "OR"

DEBUG = True
DEV_VERSION = False

SPECTACULAR_SETTINGS["COMPONENT_SPLIT_REQUEST"] = True
SPECTACULAR_SETTINGS["COMPONENT_NO_READ_ONLY_REQUIRED"] = True

DATABASES = {}

#DATABASES["default"] = dj_database_url.parse(os.environ['DATABASE_LOCAL'], conn_max_age=600)
DATABASES["default"] = dj_database_url.config(conn_max_age=600)

MAIN_TEXT_NAME = "ÖBL Haupttext"

LANGUAGE_CODE = "de"

INSTALLED_APPS += ["apis_bibsonomy"]
INSTALLED_APPS += ["webpage"]
INSTALLED_APPS += ["matomo"]
MATOMO_URL = "https://matomo.acdh.oeaw.ac.at/"
MATOMO_SITE_ID = 242

#STATICFILES_DIRS = [BASE_DIR + "/member_images"]

# APIS_COMPONENTS = ['deep learning']

# APIS_BLAZEGRAPH = ('https://blazegraph.herkules.arz.oeaw.ac.at/metaphactory-play/sparql', 'metaphactory-play', 'KQCsD24treDY')


APIS_RELATIONS_FILTER_EXCLUDE += ["annotation", "annotation_set_relation"]

from apis_ontology.filters import name_first_name_alternative_name_filter, name_alternative_name_filter, filter_empty_string, filter_status
#INSTALLED_APPS.append("apis_highlighter")
def salarychoices():
    from apis_ontology.models import Salary
    return Salary.TYP_CHOICES + (("empty", "Nicht gesetzt"),)

def placechoices():
    from apis_ontology.models import Place
    return Place.TYPE_CHOICES + (("empty", "Nicht gesetzt"),)

def genderchoices():
    from apis_ontology.models import Person
    return Person.GENDER_CHOICES + (("empty", "Nicht gesetzt"),)

detail_view_exclude = ["references", "notes", "published", "review"]

APIS_ENTITIES = {
    "Salary": {
        "relations_per_page": 100,
        "search": ["name"],
        "list_filters": {
            "typ": {"method": filter_empty_string, "extra": {"choices": salarychoices, "required": False }},
        },
        "detail_view_exclude": detail_view_exclude,

    },
    "Function": {
        "relations_per_page": 100,
        "search": ["name", "alternative_label"],
        "list_filters": {
            "name": {"method": name_alternative_name_filter, "label": "Name or alternative name"},
        },
        "table_fields": [
            "name",
            "alternative_label",
        ],
        "detail_view_exclude": detail_view_exclude,
    },
    "Court": {
        "relations_per_page": 100,
        "search": ["name", "alternative_label"],
        "detail_view_exclude": detail_view_exclude,
    },
    "Place": {
        "relations_per_page": 100,
        "merge": True,
        "search": ["name", "alternative_label"],
        "form_order": ["name", "kind", "lat", "lng", "status", "collection"],
        "table_fields": ["name"],
        "additional_cols": ["id", "lat", "lng", "part_of"],
        "list_filters": {
            "type": {"method": filter_empty_string, "extra": {"choices": placechoices, "required": False }},
        },
        "detail_view_exclude": detail_view_exclude,
    },
    "Person": {
        "relations_per_page": 100,
        "merge": True,
        "search": ["name", "first_name", "alternative_label"],
        "form_order": [
            "first_name",
            "name",
            "start_date_written",
            "end_date_written",
            "status",
            "collection",
        ],
        "table_fields": [
            "name",
            "first_name",
            "start_date_written",
            "end_date_written",
            "alternative_label",
            "status",
        ],
        "additional_cols": ["id", "gender"],
        "list_filters": {
            "name": {"method": name_first_name_alternative_name_filter, "label": "Name or first name or alternative name"},
            "gender": {"method": filter_empty_string, "extra": {"choices": genderchoices, "required": False}},
            "status": {"method": filter_status},
        },
        "detail_view_exclude": detail_view_exclude,
    },
    "Institution": {
        "relations_per_page": 100,
        "merge": True,
        "search": ["name", "alternative_label"],
        "form_order": [
            "name",
            "start_date_written",
            "end_date_written",
            "kind",
            "status",
            "collection",
        ],
        "additional_cols": [
            "id",
            "kind",
        ],
        "detail_view_exclude": detail_view_exclude,
    },
    "Work": {
        "relations_per_page": 100,
        "merge": True,
        "search": ["name"],
        "additional_cols": [
            "id",
            "kind",
        ],
        "detail_view_exclude": detail_view_exclude,
    },
    "Event": {
        "relations_per_page": 100,
        "merge": True,
        "search": ["name", "alternative_label"],
        "additional_cols": [
            "id",
        ],
        "detail_view_exclude": detail_view_exclude,
    },
}


# find out the path to the current settings file
# and use it to add a custom template path to
# the template backends
ONTOLOGY_DIR = os.path.dirname(os.path.dirname(__file__))
print(ONTOLOGY_DIR)
for template in TEMPLATES:
  template["DIRS"].append(os.path.join(ONTOLOGY_DIR, "templates"))
  template["OPTIONS"]["context_processors"].extend(
          ["webpage.webpage_content_processors.installed_apps",
          "webpage.webpage_content_processors.is_dev_version",
          "webpage.webpage_content_processors.get_db_name",
          "webpage.webpage_content_processors.title_img",
          "webpage.webpage_content_processors.logo_img",
          "webpage.webpage_content_processors.custom_css",
          "webpage.webpage_content_processors.shared_url",
          "webpage.webpage_content_processors.apis_app_name"])

BIBSONOMY_REFERENCE_SIMILARITY = ['bibs_url', 'pages_start', 'pages_end', 'folio']
ROOT_URLCONF="apis_ontology.urls"

def apis_view_passes_test(view) -> bool:
    if view.request.user.is_authenticated:
        return True
    obj = view.instance
    if hasattr(obj, 'collection'):
        return bool(obj.collection.filter(name="published"))
    return False

# we have to set this, otherwise there is an error
APIS_DETAIL_VIEWS_ALLOWED = True
APIS_VIEW_PASSES_TEST = apis_view_passes_test

def apis_list_view_object_filter(view, queryset):
    if view.request.user.is_authenticated:
        return queryset
    return queryset.filter(collection__name__contains="published")

APIS_LIST_VIEWS_ALLOWED = True
APIS_LIST_VIEW_OBJECT_FILTER = apis_list_view_object_filter

BASE_TEMPLATE = "webpage/base.html"
