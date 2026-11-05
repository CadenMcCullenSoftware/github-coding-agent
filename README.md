# GitHub Actions AI Coding Agent Starter

A lightweight **AI coding agent for GitHub Actions**. Trusted repository collaborators can comment `/agent <task>` on an issue or pull request to request a small code change. The agent sends bounded repository context to an OpenAI-compatible model, validates the returned unified diff, and opens a separate pull request for human review. It does not commit to the default branch or auto-merge.

Use this starter when you want a self-hosted-in-your-repository workflow for AI-assisted coding tasks without giving the model direct shell access. It is a prototype: generated changes can still be incorrect or unsafe, and every pull request needs human review.

## Highlights

- **Reviewable pull requests:** changes are proposed on a new branch; nothing is merged automatically.
- **Trusted-collaborator trigger:** only new `/agent ` comments from owners, members, and collaborators start a run.
- **Bounded context:** the agent reads a limited set of tracked text files and skips excluded directories and likely secrets.
- **Patch validation:** malformed patches, protected paths, oversized changes, binaries, and symlinks are rejected.
- **Provider flexibility:** configure any model service that supports the OpenAI-compatible `POST /chat/completions` interface.
- **Minimal implementation:** the agent uses Python's standard library and GitHub Actions.

## Quick start

1. Copy both [`agent.py`](agent.py) and the [coding-agent workflow](.github/workflows/coding-agent.yml) into the target repository, preserving the workflow path.
2. Add a repository Actions secret named `MODEL_API_KEY` with your model provider's API key. Never commit provider credentials.
3. Optionally add repository Actions variables:
   - `MODEL_BASE_URL`: API root. Defaults to `https://api.openai.com/v1`.
   - `MODEL_NAME`: model identifier. Defaults to `gpt-4.1-mini`.
4. In **Settings → Actions → General**, allow GitHub Actions to create pull requests. The workflow requests `contents: write`, `pull-requests: write`, and `issues: read` for its job.
5. Enable GitHub Actions. A repository owner, member, or collaborator can request a change by commenting, for example:

   ```text
   /agent Add input validation to the parser
   ```

6. Review the generated pull request, inspect the complete diff, and run the project's checks before merging.

The workflow checks out the target repository's default branch, not code from an issue author or pull request head. It creates a new branch and targets the default branch. For additional protection, enable branch protection and require human review and status checks.

## What the agent does—and does not do

The model receives a task and a bounded text snapshot of eligible tracked files, then returns a unified diff. The workflow validates and applies that diff before opening a pull request. Model output is treated as data; it is not run as a shell command.

The starter does **not** install dependencies, run project tests, deploy software, access private external services, or merge pull requests. It blocks changes under `.github/`, environment files, private-key files, and common credential or secret filenames. File extensions, context size, patch size, and number of changed files are limited in [`agent.py`](agent.py).

These controls reduce risk; they do not make generated code trustworthy by default. The workflow uses write-scoped credentials to open a branch and pull request. Keep the trusted-author gate enabled, review model-generated changes, and do not broaden permissions or invocation access without understanding the consequences.

## Configuration

`MODEL_API_KEY` is required. `MODEL_BASE_URL` and `MODEL_NAME` are optional repository Actions variables. The model endpoint must implement the OpenAI-compatible `POST /chat/completions` interface. Store credentials in GitHub Actions secrets, not in source files, issue comments, or pull requests.

The workflow runs only for newly created comments that begin with `/agent ` and whose GitHub `author_association` is `OWNER`, `MEMBER`, or `COLLABORATOR`. Fork contributors without one of these associations cannot invoke it. Review the workflow permissions and repository settings before enabling it.

## Local checks

The implementation uses only Python's standard library:

```bash
python -m unittest discover -s tests -v
python -m py_compile agent.py
```

## Contributing

Bug reports and focused improvements are welcome. Include steps to reproduce issues and expected behavior, and avoid posting credentials or private repository data in public issues.

## License

MIT. See [LICENSE](LICENSE).
