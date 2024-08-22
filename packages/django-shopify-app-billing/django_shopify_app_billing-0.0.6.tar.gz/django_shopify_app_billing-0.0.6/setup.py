from setuptools import find_packages, setup

setup(
    name="django_shopify_app_billing",
    version="0.0.6",
    author="Santiago Fernandez",
    author_email="",
    packages=find_packages(),
    scripts=[],
    url="http://pypi.python.org/pypi/django_shopify_app_billing/",
    license="MIT",
    description="A django app to help you manage the django-shopify-app package billing",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    package_data={"shopify_app_billing": ["templates/shopify_app_billing/*.html"]},
    install_requires=[
        "Django >= 4.0.0",
        "pytest",
        "django-shopify-app",
    ],
)
