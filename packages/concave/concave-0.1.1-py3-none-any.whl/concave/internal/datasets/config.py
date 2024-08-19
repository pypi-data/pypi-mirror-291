from concave.internal.datasets.swe_bench.constants import MAP_REPO_VERSION_TO_SPECS
from concave.internal.workspace.config import Config


def get_config_from_swe_bench(name: str, repo: str, version: str, base_commit: str):
    SPCE_MAPS = MAP_REPO_VERSION_TO_SPECS[repo]
    spec = SPCE_MAPS[version]
    setup = []
    if "pre_install" in spec:
        setup.extend(spec["pre_install"])

    if "pip_packages" in spec:
        setup.append('pip install {}'.format(
            " ".join(spec["pip_packages"])
        ))

    setup.append(spec["install"])

    return Config(
        name=name,
        language='python',
        version=f'{spec["python"]}',
        codebase=f'github.com/{repo}/commit/{base_commit}',
        project_setup=setup
    )
