import argparse
import configparser
import os
import sys
from pathlib import Path

import anthropic


def summarize(context: str) -> str | None:
    """This function returns the summary from the Anthropic Claude agent.

    Args:
        context(str): The context of the PR's commits that the summary is to be generated for.

    Returns:
        str: The text return summary of the PRs.
    """

    # Send to Claude
    try:
        prompt = (
            f"Analyze the following git diff and provide a PR description in github flavored Markdown, so the hashtags are marking the titles, and the bullets points are just bullet points. Dont add ```markdown``` to the response.\n\n"
            f"### PR Summary\n"
            f"(Limit to {_config['ai_bot']['no_of_sentences']} sentences max). Provide a concise overview of the purpose of these changes.\n\n"
            f"## Technical Changes\n"
            f"### Code Modifications\n"
            f"Use **bold** for key files or functions.\n"
            f"• List specific technical shifts (e.g., refactoring logic, adding endpoints).\n\n"
            f"## Executive Summary\n"
            f"### Strategic Overview\n"
            f"• High-level summary of the 'Why' behind this PR.\n"
            f"• Focus on the problem being solved rather than the code syntax.\n\n"
            f"## Business Impact\n"
            f"### User & Operational Value\n"
            f"• Explain how this affects the end-user (e.g., performance, bug fixes).\n"
            f"• Note any reduction in technical debt or security improvements.\n\n"
            f"**Commits to analyze:**\n{context}"
        )

        response = client.messages.create(
            model=_config["ai_bot"]["model"],
            max_tokens=2048,
            messages=[{"role": "user", "content": prompt}],
        )
        response_text = response.content[0].text
    except Exception as e:
        print(f"AI Generation Error: {e}")
        exit(1)

    return response_text if response_text else None


if __name__ == "__main__":
    current_file = Path(__file__).resolve()
    current_dir = current_file.parent
    _config = configparser.ConfigParser()
    _config.read(os.path.join(current_dir, "config.ini"))
    _number_of_sentences = _config["ai_bot"]["no_of_sentences"]
    _model = _config["ai_bot"]["model"]

    # Configure Anthropic client
    client = anthropic.Anthropic(
        api_key=os.getenv("CLAUDE_API_KEY"),
    )

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--file", help="The file with the PR commit data.", required=True
    )
    parser.add_argument(
        "--debug",
        action="store_true",
        default=False,
        help="Sets debug mode, will print out available models.",
        required=False,
    )
    args = parser.parse_args()

    # Let's error if the user doesn't input a value for the user argument
    if args.file == "" or args.file is None:
        print(
            "[ERROR] - The file argument cannot be empty. Please provide a valid file containing the current PR commit data.",
            file=sys.stderr,
        )
        exit(1)

    try:
        with open(args.file, "r") as f:
            context = f.read()
    except FileNotFoundError:
        print(f"Error: The file '{args.file}' was not found.")
        exit(1)

    if args.debug:
        print(f"Number of sentences: {_number_of_sentences}")
        print(f"Model: {_model}")

    response_text = summarize(context=context)

    if response_text is not None:
        with open("summary.md", "w") as f:
            f.write(response_text)
    else:
        print(
            "[ERROR] - Could not retrieve the report data from Anthropic Claude...",
            file=sys.stderr,
        )
        exit(1)
