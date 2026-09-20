
import json
from pathlib import Path
from src.exceptions import EmptyFileError,InvalidFileFormatError

class JobParser:
    #Ingests and normalizes job posting files across various formats.

    SUPPORTED_EXTENSIONS = {'.txt','.md','.json'}
    @classmethod
    def parse_file(cls, file_path : str | Path) -> str:
        path = Path(file_path)
        if not path.exists():
            raise FileNotFoundError(f'File not found: {path}')

        if path.suffix.lower() not in cls.SUPPORTED_EXTENSIONS:
         raise InvalidFileFormatError(
             f'Unsupported format {path.suffix}. Must be one of'
             f' {cls.SUPPORTED_EXTENSIONS}'
         )

        with open(path,'r',encoding = 'utf-8') as f:
         content = f.read().strip()

        if not content:
         raise EmptyFileError(f'File is empty: {path}')


        if path.suffix.lower() == '.json':
            data = json.loads(content)
            # Extract common job fields: description, requirements, or body
            return ' '.join([
                str(v)
                for k ,v in data.items()
                if k.lower() in('desciption','requirements','summary','body') 
            ])

            return content   


import urllib.parse
import httpx

class RemoteJobParser:
    """Fetches job posting from remote URLs or public APIs."""

    @staticmethod
    def fetch_from_url(url:str,timeout:float=10.0) -> str:
        # Basic validation
        parsed = urllib.parse.urlparse(url)
        if not parsed.scheme or not parsed.netloc:
            raise ValueError(f"Invalid URL:{url}")

        try:
            with httpx.Client(timeout=timeout) as client:
                response = client.get(url)
                response.raise_for_status()
                return response.text
        except httpx.HTTPError as e:
            raise ConnectionError(f"Failed to fetch job posting from {url} :{e}")
        

