import subprocess as sb

from tqdm import tqdm

from config import *
from libs.functional.documents.doc_to_docx_image_compare import WordCompareImg

if __name__ == "__main__":
    for i in tqdm(range(1)):
        WordCompareImg(list_of_file_names)
        sb.call(f'powershell.exe kill -Name WINWORD', shell=False)
