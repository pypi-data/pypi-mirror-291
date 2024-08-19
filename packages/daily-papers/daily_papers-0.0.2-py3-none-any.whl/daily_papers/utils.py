import os
from datetime import datetime, timedelta
from typing import Dict, List, Optional

import requests
from llama_index.core import Document, SimpleDirectoryReader

ARXIV_PDF_URL: str = "https://arxiv.org/pdf/"
DAILY_PAPERS_ENDPOINT: str = "https://huggingface.co/api/daily_papers"


def info_to_md_list(id_title_dict_list: List[Dict[str, str]]) -> str:
    txt = ""
    for index, item in enumerate(id_title_dict_list, start=1):
        txt += f"{index}. {item['id']} | {item['name']}\n"
    return txt


def get_date() -> str:
    now = datetime.now()

    if now.hour >= 9:
        date_to_check = now
    else:
        date_to_check = now - timedelta(days=1)

    # Adjust for weekends
    if date_to_check.weekday() == 5:
        date_to_check -= timedelta(days=1)
    elif date_to_check.weekday() == 6:
        date_to_check -= timedelta(days=2)

    return date_to_check.strftime("%Y-%m-%d")


def fetch_ids() -> List[str]:
    ids = []
    params: Dict[str, str] = {"date": get_date()}
    response = requests.get(url=DAILY_PAPERS_ENDPOINT, params=params)

    # collect paper ids
    for element in response.json():
        _id = element["paper"]["id"]
        ids.append(_id)

    return ids


def fetch_papers() -> List[Dict[str, str]]:
    info = []
    params: Dict[str, str] = {"date": get_date()}
    response = requests.get(url=DAILY_PAPERS_ENDPOINT, params=params)

    for element in response.json():
        _id = element["paper"]["id"]
        name = element["paper"]["title"]
        info.append({"id": _id, "name": name})

    return info


def download_papers(paper_id: Optional[str] = None) -> None:
    ids = fetch_ids()
    if paper_id is not None:
        assert paper_id in ids

    path = f"artifacts/{get_date()}"
    os.makedirs(path, exist_ok=True)

    if paper_id:
        _url = ARXIV_PDF_URL + paper_id
        response = requests.get(_url)
        if response.status_code == 200:
            with open(f"{path}/{paper_id}.pdf", "wb") as f:
                f.write(response.content)
        else:
            raise ValueError(
                f"download for paper id {paper_id} failed with error code {response.status_code}"
            )
    else:
        for paper_id in ids:
            download_papers(paper_id)


def load_paper_as_context(paper_id: str, verbose: bool = False) -> List[Document]:
    download_papers(paper_id=paper_id)
    reader = SimpleDirectoryReader(
        input_dir=f"artifacts/{get_date()}",
        input_files=[f"artifacts/{get_date()}/{paper_id}.pdf"],
    )
    context = reader.load_data(show_progress=verbose)

    return context
