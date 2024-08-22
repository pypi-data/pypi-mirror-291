import re
import setuptools


# function to read the version wrote down in the project_name.__init__ file
def get_property(prop, project):
    result = re.search(r'{}\s*=\s*[\'"]([^\'"]*)[\'"]'.format(prop), open(project + '/__init__.py').read())
    return result.group(1)


project_name = 'crackpy'

setuptools.setup(
    name='crackpy',
    version=get_property('__version__', project_name),
    packages=setuptools.find_packages(
        exclude=['test_scripts*',
                 'crackpy.tests*,'
                 'example_images']
    ),
    description='Crack Analysis Tool in Python - CrackPy',
    author='DLR',
    license='MIT',
    include_package_data=True,
    install_requires=[
        'matplotlib>=3.5.3',
        'numpy>=1.23.2',
        'opencv_python>=4.5.4.60',
        'pandas>=1.4.3',
        'pyvista>=0.37.0',
        'scikit_image>=0.19.3',
        'scikit_learn>=1.1.2',
        'scipy>=1.9.0',
        'torch>=1.13.1',
        'torchvision>=0.13.1',
        'rich>=12.5.1'
    ]
)
