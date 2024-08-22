import os
import re
import base64
import itertools
import json
import re
from pathlib import Path
import requests
from langchain_core.pydantic_v1 import BaseModel, Field, PrivateAttr
from typing import Optional, Dict, Any, Union, List, Type
from metalm_tools.code_interpreter.codeinterpreter_session import CodeinterpreterSession
from langchain_community.tools import BaseTool, Tool
from langchain_community.tools.e2b_data_analysis.unparse import Unparser
from langchain_community.tools import BearlyInterpreterTool

def strip_markdown_code(md_string: str) -> str:
    """Strip markdown code from a string."""
    stripped_string = re.sub(r"^`{1,3}.*?\n", "", md_string, flags=re.DOTALL)
    stripped_string = re.sub(r"`{1,3}$", "", stripped_string)
    return stripped_string

   
class MetaLMInterpreterToolArguments(BaseModel):
    """Arguments for the MetaLMInterpreterTool."""

    python_code: str = Field(
        ...,
        example="print('Hello World')",
        description=(
            "The pure python script to be evaluated. "
            "The contents will be in main.py. "
            "It should not be in markdown format."
        ),
    )

base_description = """Evaluates python code in a sandbox environment. \
You must send the whole script every time and print your outputs. \
Script should be pure python code that can be evaluated. \
It should be in python format NOT markdown. \
The code should NOT be wrapped in backticks. \
All python packages including requests, matplotlib, scipy, numpy, pandas, \
etc are available. \
If you have any files outputted write them to "output/" relative to the execution \
path. Output can only be read from the directory, stdout, and stdin. \
Do not use things like plot.show() as it will \
not work instead write them out `output/` and a link to the file will be returned. \
print() any output and results so you can capture the output."""

base_description_zh = """在沙箱环境中运行python代码。\
每次都必须发送整个脚本并打印输出。\
脚本应该是可以求值的纯python代码。\
它应该是python格式,而不是markdown。\
代码不应该用反引号括起来。\
所有python包包括requests, matplotlib, scipy, numpy, pandas, \
等等都可用。\
如果有任何文件输出，将它们相对于执行路径写入 "output/"。\
只能从目录、标准输出和标准输入中读取输出。\
不要使用plot.show()之类的东西，因为它不起作用，而是将它们写出来' output/ '，并返回到文件的链接。\
print() 任何输出和结果，以便您可以捕获输出。"""


class UploadedFile(BaseModel):
    """Description of the uploaded path with its remote path."""

    name: str
    remote_path: str
    description: str

class MetaLMInterpreterTool(BaseTool):
    """Tool for evaluating python code in a sandbox environment."""

    name = "metalm_interpreter"
    session: Any
    args_schema: Type[BaseModel] = MetaLMInterpreterToolArguments
    description: str
    _uploaded_files: List[UploadedFile] = PrivateAttr(default_factory=list)
    
    def __init__(
        self,
        url: Optional[str] = None,
        api_key: Optional[str] = None,
        **kwargs: Any,
    ):
        super().__init__(description=base_description, **kwargs)
        self.session = CodeinterpreterSession(url,api_key)
        
    def close(self) -> None:
        """Close the cloud sandbox."""
        self._uploaded_files = []
        self.session.close()
    
    def __del__(self):
        self.close()
        
    @property
    def uploaded_files_description(self) -> str:
        if len(self._uploaded_files) == 0:
            return ""
        lines = ["The following files available in the sandbox:"]

        for f in self._uploaded_files:
            if f.description == "":
                lines.append(f"- path: `{f.remote_path}`")
            else:
                lines.append(
                    f"- path: `{f.remote_path}` \n description: `{f.description}`"
                )
        return "\n".join(lines)

    def _run(self, python_code: str) -> dict:
        script = strip_markdown_code(python_code)
        return self.session.run_code(script)
    
    async def _arun(
        self,
        python_code: str,
    ) -> str:
        raise NotImplementedError("does not support async")

    def install_python_packages(self, package_names: Union[str, List[str]]) -> None:
        """Install python packages in the sandbox."""
        if isinstance(package_names, str):
            package_names = [package_names]
        self.session.install(package_names)
        
    def download_files(self, remote_paths: Union[str, List[str]]) -> bytes:
        """Download file from the sandbox."""
        if isinstance(remote_paths, str):
            remote_paths = [remote_paths]
        return self.session.download_files(remote_paths)
    
    def upload_files(self, filenames: List[str], descriptions: List[str]) -> UploadedFile:
        """Upload file to the sandbox.

        The file is uploaded to the '/codebox/<filename>' path."""
        remote_paths = self.session.upload_files(filenames)
        for idx in range(len(filenames)):
            f = UploadedFile(
                name=os.path.basename(filenames[idx]),
                remote_path=remote_paths[idx],
                description=descriptions[idx],
            )
            self._uploaded_files.append(f)
        self.description = self.description + "\n" + self.uploaded_files_description
        return self._uploaded_files
    
    def as_tool(self) -> Tool:  # type: ignore[override]
        return Tool.from_function(
            func=self._run,
            name=self.name,
            description=self.description,
            args_schema=self.args_schema,
        )
