import argparse

from dotenv import load_dotenv
from llama_index.core import Settings, VectorStoreIndex
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress
from rich.prompt import Confirm, Prompt

from daily_papers.engine.summarize import get_summary
from daily_papers.utils import (
    fetch_ids,
    fetch_papers,
    get_date,
    info_to_md_list,
    load_paper_as_context,
)

load_dotenv()


def drills_cli():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--model",
        help="Which model to use, one of openai, anthropic or some model from the huggingface hub",
        default="anthropic",
    )
    parser.add_argument(
        "--embedding_model",
        help="which embedding model to use",
        default="BAAI/bge-small-en-v1.5",
    )
    args = parser.parse_args()

    if args.model == "anthropic":
        from llama_index.llms.anthropic import Anthropic

        Settings.llm = Anthropic(temperature=0.0, model="claude-3-haiku-20240307")
    else:
        import warnings
        import torch
        warnings.filterwarnings("ignore", category=UserWarning)
        from llama_index.llms.huggingface import HuggingFaceLLM

        Settings.llm = HuggingFaceLLM(
            context_window=2048,
            tokenizer_name=args.model,
            model_name=args.model,
            device_map="auto",
            model_kwargs={"torch_dtype": torch.float16, "offload_folder": "artifacts/offload"},
        )

    Settings.embed_model = HuggingFaceEmbedding(model_name=args.embedding_model, trust_remote_code=True)

    console = Console()
    info = fetch_papers()
    ids = fetch_ids()

    console.print(Panel(info_to_md_list(info), title=get_date()))

    if Confirm.ask("Do you want the summary of any paper in particular?", default=True):
        paper_id = Prompt.ask("Enter the paper id", choices=ids)
        with Progress(transient=True) as progress:
            # Download and load paper
            load_docs_task = progress.add_task(
                "[cyan]downloading and loading the paper as context for LLM", total=1
            )
            context = load_paper_as_context(paper_id=paper_id)
            progress.update(load_docs_task, completed=True)

            # Generate Summaries
            generate_summaries_task = progress.add_task(
                "[cyan]generating summary", total=len(context)
            )
            summary = get_summary(
                context, rich_metadata=[progress, generate_summaries_task]
            )
            progress.console.print(Panel(summary, title=f"Summary for {paper_id}"))
    if Confirm.ask("Do you want to ask any questions about this paper?", default=True):
        index = VectorStoreIndex.from_documents(context)
        chat_engine = index.as_chat_engine()
        chat_engine.chat_repl()


if __name__ == "__main__":
    drills_cli()
