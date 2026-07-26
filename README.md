# Unity Project Generative AI PR Descriptor

[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

This Github Action creates a comprehensive PR description using generative AI. This action saves developer
time by automatically pulling in the commits in the repo, and generating the summary for the developer.

Need some back story? See [back story](docs/backstory.md).

## Usage

Add this as a step in your Github Workflow:

```yaml
steps:
    - name: Summarize PR
        if: (github.event_name == 'pull_request') && (github.event.pull_request.merged == false)
        uses: The-Unity-Project-LLC/pull-request-automation@v0.1.0
        with:
            github_token: ${{ secrets.GH_TOKEN }}
            gemini_api_token: ${{ secrets.GEMINI_GITHUB_REPORT_API_KEY }}
```
