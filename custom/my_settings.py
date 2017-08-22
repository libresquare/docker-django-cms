## Prerequisites
# pip install aldryn-boilerplates aldryn-bootstrap3 aldryn-newsblog django-cms-articles Markdown django-markwhat cmsplugin-markdown djangocms-history djangocms-timed djangocms-light-gallery djangocms-page-meta djangocms-maps
# python manage.py syncdb
# python manage.py migrate
# python manage.py makemigrations
# python manage.py collectstatic

## Expected files
# /home/django/custom/my_settings.py
# /home/django/custom/templates/flexible.html

## Expected Environment Variables
# LANGUAGE_CODE      (E.g. "en")
# TIME_ZONE          (E.g. "Asia/Hong_Kong")
# LANGUAGES          (E.g. "en:English;zh-hant:Traditional Chinese")
# DATABASE_ENGINE    (E.g. "django.db.backends.postgresql_psycopg2")
# DATABASE_HOST      (E.g. "djangocmsdb")
# DATABASE_PORT
# DATABASE_NAME
# DATABASE_USER
# DATABASE_PASSWORD

## Launch Demo
# python manage.py runserver --pythonpath /home/django/custom --settings my_settings 0.0.0.0:8000

import os, io, csv
from mysite.settings import *

CUSTOM_SETTINGS_DIR = '/home/django/custom'

thumbnail_precessors_list = list(THUMBNAIL_PROCESSORS)
installed_apps_list = list(INSTALLED_APPS)

DEBUG = False
ALLOWED_HOSTS = ['*']

if 'LANGUAGE_CODE' in os.environ:    
    LANGUAGE_CODE = os.environ['LANGUAGE_CODE']

if 'TIME_ZONE' in os.environ:
    TIME_ZONE = os.environ['TIME_ZONE']

if 'LANGUAGES' in os.environ:
    LANGUAGES = ()
    CMS_LANGUAGES[1] = []
    
    language_list = list(csv.reader(io.StringIO(os.environ['LANGUAGES']), delimiter=';'))[0]
    for language in language_list:
        language_param = list(csv.reader(io.StringIO(language), delimiter=':'))[0]
        language_code = language_param[0]
        language_name = language_param[1]
        LANGUAGES += ((language_code, gettext(language_name)),)
        CMS_LANGUAGES[1] += [{
            'code': language_code,
            'name': gettext(language_name),
            'public': True,
            'redirect_on_fallback': True,
            'hide_untranslated': False,
        }]

TEMPLATES[0]['DIRS'] = [os.path.join(CUSTOM_SETTINGS_DIR, 'templates'),]

CMS_TEMPLATES = (
    ('flexible.html', 'Flexible'),
)

if 'DATABASE_ENGINE' in os.environ:
    DATABASES['default']['ENGINE'] = os.environ['DATABASE_ENGINE']
    
if 'DATABASE_HOST' in os.environ:
    DATABASES['default']['HOST'] = os.environ['DATABASE_HOST']

if 'DATABASE_PORT' in os.environ:
    DATABASES['default']['PORT'] = os.environ['DATABASE_PORT']
    
if 'DATABASE_NAME' in os.environ:
    DATABASES['default']['NAME'] = os.environ['DATABASE_NAME']
    
if 'DATABASE_USER' in os.environ:
    DATABASES['default']['USER'] = os.environ['DATABASE_USER']
    
if 'DATABASE_PASSWORD' in os.environ:
    DATABASES['default']['PASSWORD'] = os.environ['DATABASE_PASSWORD']

## aldryn_boilerplates
installed_apps_list += ['aldryn_boilerplates']

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'aldryn_boilerplates.staticfile_finders.AppDirectoriesFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)
TEMPLATES[0]['OPTIONS']['context_processors'] += ['aldryn_boilerplates.context_processors.boilerplate']
TEMPLATES[0]['OPTIONS']['loaders'].insert(TEMPLATES[0]['OPTIONS']['loaders'].index('django.template.loaders.app_directories.Loader'), 'aldryn_boilerplates.template_loaders.AppDirectoriesLoader')

ALDRYN_BOILERPLATE_NAME = 'bootstrap3'

## aldryn-bootstrap3
installed_apps_list += ['aldryn_bootstrap3']

## aldryn-newsblog
installed_apps_list += [
    'aldryn_apphooks_config',
    'aldryn_categories',
    'aldryn_common',
    'aldryn_newsblog',
    'aldryn_people',
    'aldryn_reversion',
    'aldryn_translation_tools',
    'parler',
    'sortedm2m',
    'taggit'
]

if 'easy_thumbnails.processors.scale_and_crop' in thumbnail_precessors_list:
    thumbnail_precessors_list.insert(thumbnail_precessors_list.index('easy_thumbnails.processors.scale_and_crop'), 'filer.thumbnail_processors.scale_and_crop_with_subject_location')
    thumbnail_precessors_list.remove('easy_thumbnails.processors.scale_and_crop')

## cmsplugin-markdown
installed_apps_list += [
    'django_markwhat',
    'cmsplugin_markdown'
]

## djangocms-history
installed_apps_list += ['djangocms_history']

## djangocms-timed
installed_apps_list += ['djangocms_timed']

## djangocms-light-gallery
installed_apps_list += ['light_gallery']

## djangocms-page-meta
installed_apps_list += [
    'filer',
    'meta',
    'easy_thumbnails',
    'djangocms_page_meta'
]

## djangocms-maps
installed_apps_list += ['djangocms_maps']

THUMBNAIL_PROCESSORS = tuple(thumbnail_precessors_list)
INSTALLED_APPS = tuple(list(INSTALLED_APPS) + list(set(installed_apps_list) - set(INSTALLED_APPS)))