from setuptools import setup, find_packages

setup(
    name = "django-allmedia",
    url = "http://github.com/suselrd/django-allmedia/",
    author = "Susel Ruiz Duran",
    author_email = "suselrd@gmail.com",
    version = "0.2.0",
    packages = find_packages(),
    include_package_data=True,
    zip_safe=False,
    description = "All Media for Django (Images, Videos, Attachments)",
    install_requires=['django>=1.6.1',
                      'pytz==2013d',
                      'billiard==3.3.0.17',
                      'amqp==1.4.5',
                      'anyjson==0.3.3',
                      'kombu==3.0.15',
                      'celery==3.1.4',
                      'Pillow'],
    classifiers = [
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.3",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Libraries",
        "Topic :: Utilities",
        "Environment :: Web Environment",
        "Framework :: Django",
    ],

)
