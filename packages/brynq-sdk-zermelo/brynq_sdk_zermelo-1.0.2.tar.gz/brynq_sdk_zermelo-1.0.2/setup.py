from setuptools import setup


setup(
    name='brynq_sdk_zermelo',
    version='1.0.2',
    description='Zermelo wrapper from BrynQ',
    long_description='Zermelo wrapper from BrynQ',
    author='BrynQ',
    author_email='support@brynq.com',
    packages=["brynq_sdk.zermelo"],
    license='BrynQ License',
    install_requires=[
        'brynq-sdk-brynq>=1',
        'pandas>=1,<3',
        'requests>=2,<=3'
    ],
    zip_safe=False,
)