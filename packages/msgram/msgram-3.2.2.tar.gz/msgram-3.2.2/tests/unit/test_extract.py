import sys
import pytest
import tempfile
import shutil
import os
import copy

from io import StringIO
from pathlib import Path

from src.cli.commands.cmd_extract import get_infos_from_name, command_extract

EXTRACT_ARGS = {
    "output_origin": "sonarqube",
    "extracted_path": Path(""),
    "data_path": Path(""),
    "language_extension": "py",
}


def test_get_file_infos():
    file_path = "tests/unit/data/fga-eps-mds-2022-2-MeasureSoftGram-CLI-01-11-2023-21-59-03-develop.json"

    file_name = get_infos_from_name(file_path)
    assert (
        "fga-eps-mds-2022-2-MeasureSoftGram-CLI-01-11-2023-21-59-03-develop-extracted.msgram"
        in file_name
    )


def test_not_get_file_infos_wrong_name():
    filename = "metrics/wrong-name.json"

    with pytest.raises(SystemExit) as e:
        _ = get_infos_from_name(filename)

    assert e.value.code == 1


def test_command_extract_should_succeed():
    config_dirpath = tempfile.mkdtemp()
    extract_dirpath = tempfile.mkdtemp()

    shutil.copy("tests/unit/data/msgram.json", f"{config_dirpath}/msgram.json")

    shutil.copy(
        "tests/unit/data/fga-eps-mds-2022-2-MeasureSoftGram-CLI-01-11-2023-21-59-03-develop.json",
        f"{extract_dirpath}/fga-eps-mds-2022-2-MeasureSoftGram-CLI-01-11-2023-21-59-03-develop.json",
    )

    args = {
        "output_origin": "sonarqube",
        "extracted_path": Path(config_dirpath),
        "data_path": Path(extract_dirpath),
        "language_extension": "py",
    }

    captured_output = StringIO()
    sys.stdout = captured_output

    command_extract(args)

    sys.stdout = sys.__stdout__

    assert "Metrics successfully extracted" in captured_output.getvalue()
    assert os.path.isfile(
        f"{config_dirpath}/fga-eps-mds-2022-2-MeasureSoftGram-"
        "CLI-01-11-2023-21-59-03-develop-extracted.msgram"
    )

    shutil.rmtree(config_dirpath)
    shutil.rmtree(extract_dirpath)


@pytest.mark.parametrize(
    "extract_arg",
    ["output_origin", "extracted_path", "language_extension"],
)
def test_extract_invalid_args(extract_arg):
    captured_output = StringIO()
    sys.stdout = captured_output

    args = copy.deepcopy(EXTRACT_ARGS)
    del args[extract_arg]

    with pytest.raises(SystemExit):
        command_extract(args)

    sys.stdout = sys.__stdout__
    assert (
        f"KeyError: args['{extract_arg}'] - non-existent parameters"
        in captured_output.getvalue()
    )


def test_extract_fail_no_dp_or_rep():
    extract_dirpath = tempfile.mkdtemp()
    args = {
        "output_origin": "sonarqube",
        "language_extension": "py",
        "extracted_path": Path(extract_dirpath),
    }

    captured_output = StringIO()
    sys.stdout = captured_output
    with pytest.raises(SystemExit):
        command_extract(args)

    sys.stdout = sys.__stdout__

    assert (
        "It is necessary to pass the data_path or repository_path parameters"
        in captured_output.getvalue()
    )


def test_extract_fail_sonarqube_wf():
    extract_dirpath = tempfile.mkdtemp()
    args = {
        "output_origin": "sonarqube",
        "language_extension": "py",
        "extracted_path": Path(extract_dirpath),
        "repository_path": "fga-eps-mds/2023-1-MeasureSoftGram-DOC",
        "workflows": "pages build and deployment",
    }

    captured_output = StringIO()
    sys.stdout = captured_output
    with pytest.raises(SystemExit):
        command_extract(args)

    sys.stdout = sys.__stdout__

    assert (
        'Error: The parameter "-wf" must accompany a github repository output'
        in captured_output.getvalue()
    )


def test_extract_fail_sonarqube_lb():
    extract_dirpath = tempfile.mkdtemp()
    args = {
        "output_origin": "sonarqube",
        "language_extension": "py",
        "extracted_path": Path(extract_dirpath),
        "repository_path": "fga-eps-mds/2023-1-MeasureSoftGram-DOC",
        "label": "US",
    }

    captured_output = StringIO()
    sys.stdout = captured_output
    with pytest.raises(SystemExit):
        command_extract(args)

    sys.stdout = sys.__stdout__

    assert (
        'Error: The parameter "-lb" must accompany a github repository output'
        in captured_output.getvalue()
    )


def test_extract_fail_sonarqube_fd():
    extract_dirpath = tempfile.mkdtemp()
    args = {
        "output_origin": "sonarqube",
        "language_extension": "py",
        "extracted_path": Path(extract_dirpath),
        "repository_path": "fga-eps-mds/2023-1-MeasureSoftGram-DOC",
        "filter_date": "20/06/2023-15/07/2023",
    }

    captured_output = StringIO()
    sys.stdout = captured_output
    with pytest.raises(SystemExit):
        command_extract(args)

    sys.stdout = sys.__stdout__

    assert (
        'Error: The parameter "-fd" must accompany a github repository output'
        in captured_output.getvalue()
    )


def test_extract_fail_date_format():
    extract_dirpath = tempfile.mkdtemp()
    args = {
        "output_origin": "github",
        "language_extension": "py",
        "extracted_path": Path(extract_dirpath),
        "repository_path": "fga-eps-mds/2023-1-MeasureSoftGram-DOC",
        "filter_date": "20/06/2023-15/07/2021",
    }

    captured_output = StringIO()
    sys.stdout = captured_output
    with pytest.raises(SystemExit):
        command_extract(args)

    sys.stdout = sys.__stdout__

    assert (
        "Error: Range of dates for filter must be in format 'dd/mm/yyyy-dd/mm/yyyy'"
        in captured_output.getvalue()
    )


def test_extract_directory_not_exist():
    args = {
        "output_origin": "sonarqube",
        "language_extension": "py",
        "extracted_path": Path("tests/directory_not_exist"),
        "data_path": Path("tests/directory_not_exist"),
    }

    captured_output = StringIO()
    sys.stdout = captured_output
    with pytest.raises(SystemExit):
        command_extract(args)

    sys.stdout = sys.__stdout__

    assert "FileNotFoundError: extract directory" in captured_output.getvalue()
