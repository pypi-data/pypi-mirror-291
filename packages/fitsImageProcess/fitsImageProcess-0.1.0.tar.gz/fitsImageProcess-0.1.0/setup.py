from setuptools import setup, find_packages

setup(
    name='fitsImageProcess',  # This should be a unique name for your package
    version='0.1.0',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    install_requires=[
        # List your package dependencies here
        # e.g., 'numpy', 'pandas', etc.
        'numpy','astropy','matplotlib','photutils','sep','astroquery','collections','numba','reproject','scipy','setuptools','opencv-python','cmastro','skimage','os','time'
    ],
    entry_points={
        'console_scripts': [
            # Define any command-line scripts here
        ],
    },
    # url='https://github.com/yourusername/fitsImageProcess',  # Update this with your repository URL
    license='MIT',
    author='Matthieu Musy',
    author_email='matthieu.musy@ensta-bretagne.org',
    description='A package for processing FITS images',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
)
