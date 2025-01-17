from setuptools import setup, find_packages
##

setup(
  name = 'swarms',
  packages = find_packages(exclude=[]),
  version = '1.1.3',
  license='MIT',
  description = 'Swarms - Pytorch',
  author = 'Kye Gomez',
  author_email = 'kye@apac.ai',
  long_description_content_type = 'text/markdown',
  url = 'https://github.com/kyegomez/swarms',
  keywords = [
    'artificial intelligence',
    'deep learning',
    'optimizers',
    "Prompt Engineering"
  ],
  install_requires=[
        'transformers',
        'openai',
        'langchain',
        'torch',
        'torchvision',
        'torchaudio',
        'asyncio',
        'nest_asyncio',
        'bs4',
        'pegasusx',
        'oceandb',
        'playwright',
        'duckduckgo_search',
        'faiss-cpu',
        'wget==3.2',
        'accelerate',
        'sphinx_rtd_theme',
        'addict',
        'albumentations',
        'basicsr',
        'controlnet-aux',
        'diffusers',
        'einops',
        'gradio',
        'imageio',
        'imageio-ffmpeg',
        'kornia',
        'numpy',
        'omegaconf',
        'open_clip_torch',
        'opencv-python',
        'prettytable',
        'safetensors',
        'streamlit',
        'test-tube',
        'timm',
        'torchmetrics',
        'webdataset',
        'yapf',
        'wolframalpha',
        'wikipedia==1.4.0',
        'httpx',
        'ggl',
        'gradio_tools',
        'arxiv',
        'google-api-python-client',
        'google-auth-httplib2',
        'beautifulsoup4==4.11.2',
        'O365',
        'pytube',
        'pydub',
        'llama-index',
        'fastapi==0.94.1',
        'pydantic==1.10.6',
        'tenacity==8.2.2',
        'python-dotenv',
        'boto3',
        'uvicorn==0.21.1',
        'jinja2==3.1.2',
        'python-multipart==0.0.6',
        'celery==5.3.1',
        'redis==4.6.0',
        'sentencepiece',
        'bitsandbytes==0.41.0',
        'psycopg2-binary==2.9.5',
        'google-search-results==2.4.2',
        'black==23.7.0',
        'Pillow',
        'selenium',
        'diffusers',
        'controlnet_aux',
        'tiktoken',
        'espnet==202301',
        'espnet_model_zoo==0.1.7',
        'flask==2.2.3',
        'flask_cors==3.0.10',
        'waitress==2.1.2',
        'asteroid',
        'speechbrain',
        'timm',
        'typeguard',
        'pytesseract',
        'huggingface_hub',
        'fastapi-cache',
        'fastapi-limiter',
    ],
  classifiers=[
    'Development Status :: 4 - Beta',
    'Intended Audience :: Developers',
    'Topic :: Scientific/Engineering :: Artificial Intelligence',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3.6',
  ],
)