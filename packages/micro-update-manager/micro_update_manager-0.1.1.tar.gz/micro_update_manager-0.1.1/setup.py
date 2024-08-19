from setuptools import setup, find_packages

setup(
    name="micro-update-manager",
    use_scm_version=True,
    setup_requires=['setuptools_scm'],
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'flake8',
        'numpy',
        'requests',
        'pyyaml',
    ],
    entry_points={
        'console_scripts': [
            'micro-update-manager=micro_update_manager.micro_update_manager:main',
        ],
    },
    author="Aleksander Stanik (Olek)",
    author_email="aleksander.stanik@hammerheadsengineers.com",
    description="A Python package for monitoring and updating Python packages, managing and restarting dependent microservices.",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url="https://github.com/AleksanderStanikHE/micro-update-manager.git",
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.7',
)
