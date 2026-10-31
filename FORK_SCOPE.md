# Scope of this fork

Upstream: [ImagingDataCommons/IDC-Tutorials](https://github.com/ImagingDataCommons/IDC-Tutorials). Original authorship and license
remain with upstream; upstream performance/clinical claims are not personal
portfolio results.

Learning reference for the upstream NCI Imaging Data Commons tutorials. It is not a personal medical ML platform or an independently validated dataset.

## Audited snapshot and limits

Portfolio audit base: `ca36d16db3208db28295b4d19035e6d65b11d5ee` (2026-10-28, rechecked 2026-10-29).

Cloud queries/downloads, credentials, object licensing and notebook runtime costs have not been qualified by the portfolio remediation. A new tutorial execution needs its own object versions/licenses, environment and acceptance record.

The historical audit above did not run the new checks described below. These bounded checks do not certify the full upstream system.

## Offline fork qualification (2026-10-30)

The current fork checks notebook integrity without cloud credentials or model/data downloads. On Python 3.13:

```sh
python -m pip install --require-hashes -r requirements-ci.lock
python -m pip check
python -m pip_audit --no-deps --disable-pip --strict -r requirements-ci.lock
python .ci/validate_notebooks.py
python test/src/check_notebook_standards.py
```

The first validator checks all 47 notebook schemas and transforms/parses 501 code cells in active Python notebooks. The R notebook and 14 already deprecated notebooks receive schema checks only. The upstream standards script checks its 33 selected notebooks. These checks do not execute tutorial cells, cloud queries, downloads or biomedical analyses. Existing missing-cell-ID warnings remain visible. CI checks out notebook text and validator files only, excluding ONNX/H5 model assets. No notebook results were rewritten.

`requirements-ci.in` describes validation tooling, not every tutorial runtime. Regenerate the hash lock with `uv pip compile requirements-ci.in --python-version 3.13 --generate-hashes -o requirements-ci.lock`. The workflow runs on pushes, pull requests and manual dispatch. Hosted Actions results remain separate from these local checks.

## Upstream infrastructure applicability

The Colab-image maintenance job in `.github/workflows/test_colab.yml` belongs to
`ImagingDataCommons/IDC-Tutorials`: it authenticates with the upstream Google Cloud
service account, can publish `imagingdatacommons/idc-testing-colab` to Docker Hub,
executes cloud tutorials and opens an image-metadata update pull request. The
scheduled job in `.github/workflows/keep-alive.yml` maintains the upstream
`keep-alive` branch. Both jobs now require that exact upstream repository
identity. Their existing steps, assertions and secret references are preserved.
They are not part of this fork's offline learning-reference qualification.

On this fork those two jobs are **configured to skip as not applicable**. Earlier failures
from missing cloud authorization and blocked keepalive-action repository access
remain historical failures; skipping an inapplicable job does not prove that its
cloud workflow passed. No upstream credentials, publishing authority, biomedical
execution results or clinical qualification are claimed.

The independent `fork-integrity.yml` checks continue on every push, pull request
and manual dispatch. The ordinary `check_notebook_standards.yml` workflow and its
notebook-path triggers remain unchanged. Notebook schemas, Python code-cell
parsing and notebook standards remain the applicable validation gates; no cloud
or notebook assertions were weakened to make those gates pass.
