from setuptools import setup


setup(
    name='brynq_sdk_shiftbase',
    version='1.0.0',
    description='Shiftbase wrapper from BrynqQ',
    long_description='Shiftbase wrapper from BrynQ',
    author='D&A BrynQ',
    author_email='support@brynq.com',
    packages=["brynq_sdk.shiftbase"],
    license='BrynQ License',
    install_requires=[
        'brynq_sdk_brynq>=1',
        'pandas>=1,<=3',
        'requests>=2,<=3'
    ],
    zip_safe=False,
)