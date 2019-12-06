"""A setuptools based setup module."""

from setuptools import setup, find_packages

setup(
    name="todoist2org",
    version="0.0.1",
    description="Create TODO org-file from todoist",
    author="Katsuki Kobayashi",
    author_email="rare@tirasweel.org",
    entry_points={"console_scripts": ["todoist2org=todoist2org:main"]},
)
