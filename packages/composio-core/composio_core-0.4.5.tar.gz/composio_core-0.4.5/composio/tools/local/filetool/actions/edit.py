from pydantic import Field

from composio.tools.env.filemanager.manager import FileManager
from composio.tools.local.filetool.actions.base_action import (
    BaseFileAction,
    BaseFileRequest,
    BaseFileResponse,
)


class EditFileRequest(BaseFileRequest):
    """Request to edit a file."""

    file_path: str = Field(
        default=None,
        description=(
            "The path to the file that will be edited. If not provided, "
            "THE CURRENTLY OPEN FILE will be edited. If provided, the "
            "file at the provided path will be OPENED and edited, changing "
            "the opened file."
        ),
    )
    text: str = Field(
        ...,
        description="The text that will replace the specified line range in the file.",
    )
    start_line: int = Field(
        ...,
        description="The line number at which the file edit will start (REQUIRED). Inclusive - the start line will be included in the edit.",
    )
    end_line: int = Field(
        ...,
        description="The line number at which the file edit will end (REQUIRED). Exclusive - the end line will NOT be included in the edit.",
    )


class EditFileResponse(BaseFileResponse):
    """Response to edit a file."""

    old_text: str = Field(
        default=None,
        description=(
            "The updated changes. If the file was not edited, the original file "
            "will be returned."
        ),
    )
    error: str = Field(
        default=None,
        description="Error message if any",
    )
    updated_text: str = Field(
        default=None,
        description="The updated text. If the file was not edited, this will be empty.",
    )


class EditFile(BaseFileAction):
    """
    Use this tools to edit a file.
    THE EDIT COMMAND REQUIRES INDENTATION.

    If you'd like to add the line '        print(x)' you must fully write
    that out, with all those spaces before the code!

    If a lint error occurs, the edit will not be applied.
    Review the error message, adjust your edit accordingly.

    If start line and end line are the same,
    the new text will be added at the start line &
    text at end line will be still in the new edited file.

    Examples A - Start line == End line
    Start line: 1
    End line: 1
    Text: "print(x)"
    Result: As Start line == End line, print(x) will be added as first line in the file. Rest of the file will be unchanged.

    Examples B - Start line != End line
    Start line: 1
    End line: 3
    Text: "print(x)"
    Result: print(x) will be replaced in the file as first line.
    First and Second line will be removed as end line = 3
    Rest of the file will be unchanged.

    This action edits a specific part of the file, if you want to rewrite the
    complete file, use `write` tool instead."""

    _display_name = "Edit a file"
    _request_schema = EditFileRequest
    _response_schema = EditFileResponse

    def execute_on_file_manager(
        self,
        file_manager: FileManager,
        request_data: EditFileRequest,  # type: ignore
    ) -> EditFileResponse:
        try:
            file = (
                file_manager.recent
                if request_data.file_path is None
                else file_manager.open(
                    path=request_data.file_path,
                )
            )

            if file is None:
                raise FileNotFoundError(f"File not found: {request_data.file_path}")

            response = file.write_and_run_lint(
                text=request_data.text,
                start=request_data.start_line,
                end=request_data.end_line,
            )
            if response.get("error") and len(response["error"]) > 0:
                return EditFileResponse(
                    error="No Update, found error: " + response["error"]
                )
            return EditFileResponse(
                old_text=response["replaced_text"],
                updated_text=response["replaced_with"],
            )
        except FileNotFoundError as e:
            return EditFileResponse(error=f"File not found: {str(e)}")
        except PermissionError as e:
            return EditFileResponse(error=f"Permission denied: {str(e)}")
        except OSError as e:
            return EditFileResponse(error=f"OS error occurred: {str(e)}")
