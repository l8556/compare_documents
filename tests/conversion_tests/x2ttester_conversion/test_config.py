# -*- coding: utf-8 -*-
from os.path import dirname
from tempfile import gettempdir

from host_tools import File
from host_tools.utils import Dir
from pydantic import BaseModel, Field, model_validator
from typing import Optional

import config
from frameworks.StaticData import StaticData
from frameworks.editors.onlyoffice import VersionHandler, X2t



class TestConfig(BaseModel):
    core_dir: Optional[str] = None
    reports_dir: Optional[str] = None
    input_dir: Optional[str] = None
    result_dir: Optional[str] = None
    cores: Optional[int] = None
    timeout: Optional[int] = None
    delete: Optional[bool] = None
    direction: Optional[str] = Field(default=None, description="Conversion direction, e.g., 'docx-pdf'")
    version: Optional[str] = None
    trough_conversion: bool = False
    environment_off: bool = False
    tmp_dir: Optional[str] = None
    output_dir: Optional[str] = Field(init=False, default=None)
    report_path: Optional[str] = Field(init=False, default=None)
    timestamp: bool = Field(init=False, default=False)
    fonts_dir: Optional[str] = Field(init=False, default=None)
    errors_only: bool = Field(init=False)
    x2t_version: Optional[str] = Field(init=False, default=None)

    @model_validator(mode="after")
    def set_computed_fields(self):
        self.x2t_version = VersionHandler(self.version or X2t.version(self.core_dir)).version
        self.tmp_dir = File.unique_name(self.tmp_dir or gettempdir())
        self.report_path = self.get_tmp_report_path(self.tmp_dir)
        self.cores = self.cores or config.cores
        self.timeout = self.timeout or config.timeout
        self.timestamp = config.timestamp
        self.delete = self.delete if self.delete is not None else config.delete
        self.errors_only = config.errors_only
        self.output_dir = self.output_dir or self.tmp_dir
        self.result_dir = self.result_dir or StaticData.result_dir()
        self.input_dir = self.input_dir or StaticData.documents_dir()
        self.fonts_dir = StaticData.fonts_dir()
        return self

    @staticmethod
    def get_tmp_report_path(tmp_dir: str) -> str:
        tmp_report = File.unique_name(File.unique_name(tmp_dir), 'csv')
        Dir.create(dirname(tmp_report), stdout=False)
        return tmp_report
