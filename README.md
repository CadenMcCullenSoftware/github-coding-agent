# GitHub Coding Agent

A minimal GitHub Action that lets **trusted repository collaborators** request coding help by commenting `/agent <task>` on an issue or pull request. It reads a bounded set of tracked text files, asks a configurable OpenAI-compatible model for a unified diff, validates the patch, and opens a **reviewable pull request**. It never commits to the default branch or auto-merges.

## Quick start

1. Add `.github/workflows/coding-agent.yml` from this repository to your repository.
2. Add a repository Actions secret named `MODEL_API_KEY` for your model provider.
3. Optionally set repository Actions variables:
   - `MODEL_BASE_URL`: API root, default `https://api.openai.com/v1`.
   - `MODEL_NAME`: model identifier, default `gpt-4.1-mini`.
4. Enable Actions. In repository **Settings → Actions → General**, allow GitHub Actions to create pull requests. The workflow requests only `contents: write`, `pull-requests: write`, and `issues: read`.
5. A repository owner, member, or collaborator comments `/agent Add input validation to the parser` on an issue or PR conversation.
6. Review the generated PR before merging. Nothing is auto-merged.

The workflow checks out the repository's default branch, not code supplied by an issue author or a PR head. It creates a new branch and a PR against the default branch. For stronger protection, configure branch protection and require human review/status checks.

## What it can and cannot do

- It proposes code edits as a unified diff. Model output is never executed as a shell command.
- It considers only tracked text files with a supported source/documentation extension, with per-file and total context limits.
- It blocks patches to `.github/`, environment files, private-key files, and common credential/secret filenames; it also rejects malformed patches and whitespace errors.
- The patch size is capped. The generated branch is separate from the default branch.
- It does not install dependencies, run project tests, deploy software, access private external services, or merge PRs.
- This starter is a prototype, not a substitute for code review or security controls. Model-generated changes can be incorrect or unsafe.

## Configuration

`MODEL_API_KEY` is required. `MODEL_BASE_URL` and `MODEL_NAME` are optional repository Actions variables. The endpoint must implement the OpenAI-compatible `POST /chat/completions` interface. Keep provider credentials in GitHub Actions secrets; never commit them to the repository.

The event workflow runs only for newly created comments that begin with `/agent ` and whose GitHub `author_association` is `OWNER`, `MEMBER`, or `COLLABORATOR`. Fork contributors without one of those trusted associations cannot invoke it. Do not broaden this gate without understanding the risk of exposing write-scoped workflow credentials.

## Local checks

The implementation uses only Python's standard library:

```bash
python -m unittest discover -s tests -v
python -m py_compile agent.py
```

## License

MIT. See [LICENSE](LICENSE).
