import os
import subprocess
from .common import get_logger, write_above_or_end
import tomli


def sphinx_workflow(conf_path, docs_path, project_path, index_fname, logger=None, readme=None, title=""):
    if not logger:
        logger = get_logger(__name__)

    if not os.path.exists(conf_path):
        logger.error(f"{conf_path} is not found.")
        return

    meta_data = meta_from_conf(conf_path=conf_path)
    build_sphinx(meta_data=meta_data, docs_path=docs_path, logger=logger)
    fix_sphinx_conf(project_path=project_path, sphinx_conf_path=os.path.join(docs_path, "conf.py"))
    gen_project_docs(project_path=project_path, docs_path=docs_path, logger=logger)
    mod_name = meta_data.get("name", "")
    cleanup_index(docs_path=docs_path, index_fname=index_fname, title=title)
    if mod_name:
        toc_fname = f"""{mod_name}.rst"""
        append_module_to_index(toc_fname=toc_fname, docs_path=docs_path, index_fname=index_fname, logger=logger)
    if readme:
        append_readme_to_index(readme_path=readme, docs_path=docs_path, index_fname=index_fname, logger=logger)


def fix_sphinx_conf(project_path, sphinx_conf_path):

    pp = os.path.join(os.path.pardir, project_path)
    # fix python path
    pp = f"""
import sys
import os
sys.path.insert(0, os.path.abspath('{pp}'))
"""
    doc_gen = """
extensions += [
    'sphinx.ext.napoleon',
    'sphinx.ext.autodoc',
    'sphinx.ext.viewcode',
    'sphinx.ext.autosummary',
    'sphinx_mdinclude',
]

autosummary_generate = True

"""
    with open(sphinx_conf_path, "r") as f:
        content = f.read()

    new_content = content
    if "import sys" not in content:
        new_content = pp + content

    if "autosummary_generate" not in content:
        new_content += doc_gen

    with open(sphinx_conf_path, "w") as f:
        f.write(new_content)


def run_command(comm, logger):
    logger.debug(comm)
    p = subprocess.Popen(comm, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    for line in p.stdout.readlines():
        logger.debug(line.decode())


def gen_html(docs_path, logger):
    comm = f"cd {docs_path}; make html"
    run_command(comm, logger)


def gen_project_docs(project_path, docs_path, logger):
    """
    Generate the docs of a given directory
    :param project_path:
    :param docs_path:
    :param logger:
    :return:
    """
    comm = f"sphinx-apidoc -o {docs_path} {project_path}"
    run_command(comm, logger)


def meta_from_conf(conf_path):
    """
    Parse the configuration file
    :param conf_path: str. The configuration path.
    :return:
    """
    with open(conf_path, "rb") as f:
        toml_dict = tomli.load(f)
    return toml_dict["project"]


def meta_authors(meta_data, sep=", "):
    """
    Return the authors from the given meta dict
    :param meta_data: dict
    :param sep: str
    :return:
    """
    authors = []
    if "authors" in meta_data:
        for auth in meta_data["authors"]:
            if "name" in auth:
                authors.append(auth["name"])
    return sep.join(authors)


def meta_release(meta_data):
    """
    Get the release from the given meta dict
    :param meta_data: dict
    :param sep: str
    :return:
    """
    release = meta_data.get("version", "")
    return release


def build_sphinx(meta_data, docs_path, logger):
    """
    Build sphinx dpcs

    :param meta_data:
    :param docs_path:
    :param logger:
    :return:
    """
    project_name = meta_data["name"]
    authors = meta_authors(meta_data)
    release = meta_release(meta_data)
    comm = f"sphinx-quickstart {docs_path} -q "
    if project_name:
        comm += f""" --project "{project_name}" """
    if authors:
        comm += f""" --author "{authors}" """
    if release:
        comm += f""" --release "{release}" """

    run_command(comm, logger)


def append_indices(rst_fpath, logger):
    rst = """
Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
"""
    with open(rst_fpath, "r") as f:
        content = f.read()
    if "Indices and tables" not in content:
        logger.info("Adding Indices and tables section")
        with open(rst_fpath, "a") as f:
            f.write(rst)


def append_module_to_index(toc_fname, docs_path, index_fname, logger):
    """
    Include the examples or any other module into the index
    :param toc_fname:
    :param docs_path:
    :param index_fname:
    :return:
    """
    index_path = os.path.join(docs_path, index_fname)
    toc_name = toc_fname[:-4]
    line = f"   {toc_name}\n"
    with open(index_path, "r") as f:
        content = f.read()
    if line not in content:
        logger.info(f"Adding module {toc_name} to {index_fname}")
        write_above_or_end(index_path, target="Indices and tables", content_to_write=line)
    with open(index_path, "r") as f:
        content = f.read()
        logger.debug(f"index content after appending module {toc_name}: \n{content}\n\n\n")


def append_readme_to_index(readme_path, docs_path, index_fname, logger):
    """
    Include the readme to the index
    :param toc_fname:
    :param docs_path:
    :param index_fname:
    :return:
    """
    index_path = os.path.join(docs_path, index_fname)
    if not os.path.isabs(readme_path):
        readme_path = os.path.join(os.path.pardir, readme_path)
    line = f".. mdinclude:: {readme_path}\n"
    with open(index_path, "r") as f:
        content = f.read()
    if line not in content:
        logger.info(f"Adding readme {readme_path} to {index_fname}")
        write_above_or_end(index_path, target=".. toctree::", content_to_write=line)
    with open(index_path, "r") as f:
        content = f.read()
        logger.debug(f"index content after appending readme: \n{content}\n\n\n")


def cleanup_index(docs_path, index_fname, title=""):
    index_path = os.path.join(docs_path, index_fname)
    with open(index_path) as f:
        content = f.read()
    lines = content.split('\n')
    cutoff = 0
    for i, line in enumerate(lines):
        if ".. toctree::" in line:
            cutoff = i
            break

    new_content = "\n".join(lines[cutoff:])
    if title:
        under = "=" * len(title)
        title = title + f"\n{under}\n"
    new_content = title + new_content
    with open(index_path, "w") as f:
        f.write(new_content)

