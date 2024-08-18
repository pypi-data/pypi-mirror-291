from setuptools import setup,find_packages

setup(
    name ='AtharvaTech-STT',
    version='0.1',
    author='Atharva Shinde',
    author_email='atharvathehero07@gmail.com',
    description='This is Speech-To-Text Package created by Atharva Shinde'
)
packages = find_packages(),
install_requirement = [
    'selenium',
    'webdriver_manager'
]
