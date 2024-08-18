import os
import sys

import openai
import typer
from rich.console import Console
from youtube_transcript_api import TranscriptsDisabled

# from .config import load_config, Config
from chat_gpt.commands.chat import chat
from chat_gpt.commands.youtube import chat_with_yt_video

app = typer.Typer()

console = Console()

openai.api_key = os.environ.get("OPENAI_API_KEY")

if openai.api_key is None:
    console.print("[red]Please set the OPENAI_API_KEY environment variable.")
    exit(1)


@app.command("chat")
def start(
    model_name: str = "gpt-4o", markdown: bool = False, file_path: str | None = None
):
    """
    Start conversation with our assistant
    """
    try:
        chat(model_name, markdown=markdown, file_path=file_path)
    except KeyboardInterrupt:
        try:
            sys.exit(130)
        except SystemExit:
            os._exit(130)


@app.command()
def youtube(url: str, language: str = "en"):
    """
    Start conversation with our assistant using a youtube video transcript
    """

    try:
        chat_with_yt_video(url, language)
    except TranscriptsDisabled as e:
        console.print(
            "\n[red]Transcripts are disabled for this video or the video you're trying to extract doesn't exist."
        )
        console.print(e)
    except KeyboardInterrupt:
        try:
            sys.exit(130)
        except SystemExit:
            os._exit(130)


#
#
# @app.command()
# def show_config():
#     config: Config = load_config()
#
#     for key, value in config.model_dump().items():
#         typer.echo(f"{key}: {value}")
#
#
# @app.command()
# def rag():
#     import questionary
#
#     p = questionary.path(
#         "Enter the path to the RAG model file:", only_directories=True
#     ).ask()
#     print(p)
#     print("type", type(p))
#
#     action = questionary.rawselect(
#         "Choose an action:",
#         choices=["Chat", "RAG", "Image", "STOP"],
#     ).ask()
#
#     match action:
#         case "Chat":
#             start()
#         case "RAG":
#             typer.echo("RAG")
#         case "Image":
#             typer.echo("Image")
#             image_action = questionary.rawselect(
#                 "Choose an action:", choices=["Last screenshot", "From file path"]
#             )
#
#             match image_action:
#                 case "Last screenshot":
#                     typer.echo("Last screenshot")
#                 case "From file path":
#                     typer.echo("From file path")
#                     file_path = questionary.path(
#                         "Enter the path to the image file:", only_files=True
#                     ).ask()
#         case "STOP":
#             typer.echo("STOP")
#             sys.exit(0)
