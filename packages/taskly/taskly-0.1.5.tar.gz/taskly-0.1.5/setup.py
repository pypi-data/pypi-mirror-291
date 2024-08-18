from setuptools import setup

if __name__ == "__main__":
    try:
        setup(
            version='0.1.5',
            use_scm_version={"version_scheme": "no-guess-dev"},
            # packages=find_packages(where='src'),
            # package_dir={'': 'src'},
            package_data={'': ['scripts/reset.py']},
        )
    except Exception as e:
        print(
            "\n\nAn error occurred while building the project:\n",
            str(e),
            "\n\nPlease ensure you have the most updated version of setuptools, "
            "setuptools_scm, and wheel with:\n"
            "   pip install -U setuptools setuptools_scm wheel\n\n"
        )
        raise
