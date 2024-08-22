from setuptools import setup, find_packages

setup(
    name='tts-stt-tools',
    version='0.1.02',
    packages=find_packages(),
    install_requires=[],  # List your dependencies here
    tests_require=['unittest'],
    test_suite='tests',
    python_requires='>=3.9',
    entry_points={
        'console_scripts': [
            'tts-stt-tools=tts_stt_tools.main:generate_audio',
        ],
    },
)
