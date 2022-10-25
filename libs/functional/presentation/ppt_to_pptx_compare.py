# -*- coding: utf-8 -*-
from config import version
from framework.power_point import PowerPoint
from libs.helpers.compare_image import CompareImage
from management import *
from data.StaticData import StaticData


class PptPptxCompareImg(PowerPoint):
    def run_compare(self, list_of_files):
        logger.info(f'The {self.doc_helper.source_extension} to {self.doc_helper.converted_extension} '
                    f'comparison on version: {version} is running.')
        for self.doc_helper.converted_file in list_of_files:
            if not self.doc_helper.converted_file.endswith((".pptx", ".PPTX")):
                continue
            self.doc_helper.preparing_files_for_compare_test()
            print(f'[bold green]In test[/] {self.doc_helper.converted_file}')
            if not self.get_slide_count():
                continue
            self.open_presentation_with_cmd(self.doc_helper.tmp_converted_file)
            if not self.errors_handler_when_opening():
                self.close_presentation_with_hotkey()
                continue
            self.get_screenshot(StaticData.TMP_DIR_CONVERTED_IMG)
            self.close_presentation_with_hotkey()

            print(f'[bold green]In test[/] {self.doc_helper.source_file}')
            self.open_presentation_with_cmd(self.doc_helper.tmp_source_file)
            self.get_screenshot(StaticData.TMP_DIR_SOURCE_IMG)
            self.close_presentation_with_hotkey()

            CompareImage(self.doc_helper)
            self.doc_helper.tmp_cleaner()
