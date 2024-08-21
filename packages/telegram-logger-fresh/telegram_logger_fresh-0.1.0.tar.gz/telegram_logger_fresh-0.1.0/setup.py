from setuptools import setup, find_packages

setup(
    name="telegram_logger_fresh",
    version="0.1.0",
    description="A simple library to send messages to Telegram using a bot",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author="Danya",
    author_email="danyanaro@gmail.com",
    # url="https://github.com/ваш_github/telegram_logger_fresh",  # Ссылка на репозиторий
    packages=find_packages(),
    install_requires=[
        "requests>=2.20.0"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
