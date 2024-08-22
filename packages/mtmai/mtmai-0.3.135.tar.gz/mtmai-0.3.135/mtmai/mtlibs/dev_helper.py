import asyncio
import logging
from pathlib import Path

from mtmai.core import coreutils
from mtmai.core.config import settings
from mtmai.mtlibs import mtutils
from mtmai.mtlibs.github import git_commit_push
from mtmai.mtlibs.mtutils import is_in_gitpod
from mtmai.mtlibs.process_helper import bash, command_exists
from mtmai.mtlibs.temboio import run_tmpbo_instance1

from . import huggingface

logger = logging.getLogger()


def init_project():
    if not coreutils.is_in_gitpod():
        return

    huggingface.hf_trans1_clone()


def hf_trans1_commit():
    target_dir = (
        Path(settings.storage_dir)
        .joinpath(settings.gitsrc_dir)
        .joinpath(settings.HUGGINGFACEHUB_DEFAULT_WORKSPACE)
    )
    rnd_str = mtutils.gen_orm_id_key()
    Path(target_dir).joinpath("Dockerfile").write_text(f"""
# {rnd_str}
FROM docker.io/gitgit188/tmpboai
ENV DATABASE_URL={settings.DATABASE_URL}
ENV LOKI_USER={settings.LOKI_USER}
ENV GRAFANA_TOKEN={settings.GRAFANA_TOKEN}
ENV LOKI_ENDPOINT={settings.LOKI_ENDPOINT}


RUN sudo apt update

""")
    Path(target_dir).joinpath("README.md").write_text(f"""---
title: Trans1
emoji: 🏢
colorFrom: red
colorTo: gray
sdk: docker
pinned: false
license: other
app_port:  {settings.FRONT_PORT}
---""")
    bash(f"cd {target_dir} && git commit -am abccommit && git push")
    return {"ok": True}


def run_clean():
    bun_cache_dir = Path.home().joinpath(".bun/install/cache")
    bash(f"rm -rdf {bun_cache_dir}")

    if command_exists("pip"):
        logging.info("正在清理 pip 缓存")
        bash("pip cache dir && pip cache purge")
    if command_exists("docker"):
        logging.info("正在清理 docker 缓存")
        bash("docker system prune -f")
    if is_in_gitpod():
        logger.info("删除 ~/.rustup")
        bash("rm -rdf ~/.rustup")
        logger.info("删除 ~/.rvm")
        bash("rm -rdf ~/.rvm")


def run_release():
    logger.info("🚀 testing")
    bash("poetry run poe test")
    logger.info("✅ testing ok!")
    logger.info("🚀 build node packages")
    bash("bun run turbo build")
    asyncio.run(run_tmpbo_instance1())
    logger.info("✅ tembo io pushed")

    hf_trans1_commit()
    logger.info("✅ hf_trans1_commit")
    git_commit_push()
    mtutils.pyproject_patch_version()
    logger.info("✅ version patch new version!")
