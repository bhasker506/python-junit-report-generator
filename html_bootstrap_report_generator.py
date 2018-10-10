'''
@author : breddy
@author : usharma
'''
import html_template as template
from apitestlib.tools.html_report_generator.results_parser import TestResultsParser


class ReportGenerator(object):
    def __init__(self):
        self.summary_table = list()
        self.all_tests_table = list()
        self.failed_tests_table = list()
        self.error_tests_table = list()
        self.skipped_tests_table = list()
        self.passed_with_bugid_tests_table = list()
        self.tests_without_bugid_table = list()
        self.headers = list()
        self.all_tests_table.append(template.ALL_TESTS_TABLE_HEADER_TMPL)
        self.summary_table.append(template.SUMMARY_TABLE_HEADER_TMPL)
        self.failed_tests_table.append(template.FAILED_TESTS_TABLE_HEADER_TMPL % dict(id_refrence='failed_tests'))
        self.error_tests_table.append(template.FAILED_TESTS_TABLE_HEADER_TMPL % dict(id_refrence='error_tests'))
        self.passed_with_bugid_tests_table.append(template.FAILED_TESTS_TABLE_HEADER_TMPL % dict(
            id_refrence='passed_with_bugid'))
        self.tests_without_bugid_table.append(template.SKIPPED_TESTS_TABLE_HEADER % dict(id_refrence='with_out_bug'))
        self.skipped_tests_table.append(template.SKIPPED_TESTS_TABLE_HEADER % dict(id_refrence='skipped_tests'))
        self.Total_cases_count = 0
        self.Total_failed_count = 0
        self.Total_error_count = 0
        self.Total_skip_count = 0
        self.Total_without_bug_id_count = 0
        self.Total_passed_with_bug_id_count = 0

    def get_results(self, xml_location):
        obj = TestResultsParser()
        test_result_files = obj.get_xmls(xml_location)
        return obj.get_test_results(test_result_files)

    def generate_report(self, results, report_title='Test Report', build_no=1, **kwargs):
        kwargs['report_tile'] = report_title
        kwargs['build_no'] = build_no
        report_title = report_title.replace("_", " ")
        jenkins_details = self.get_build_details(**kwargs)
        self.headers.append(template.HTML_HEAD_TMPL % dict(report_title=report_title.upper(),
                                                           build_details=jenkins_details))
        for suite_name, suite_info in results.iteritems():
            tmp = suite_name.split(".")
            class_name = tmp[len(tmp) - 2] + "." + tmp[len(tmp) - 1]
            self._create_summary_table(class_name, suite_info)
            self._create_all_tests_table(class_name, suite_info)
            self._create_failed_tests_table(class_name, suite_info)
            self._create_error_tests_table(class_name, suite_info)
            self._create_passed_with_bugid_tests_table(class_name, suite_info)
            self._create_skipped_table(class_name, suite_info)

        html_output = self.headers + [template.SUMMARY_VIEW] + self._create_summary_count_table(len(results)) + [
            template.TABLE_FOOTER_TMPL] + \
                      self.summary_table + [template.TABLE_FOOTER_TMPL] + (
                      [template.NO_DATA_FOUND] if len(results) == 0 else [""]) + [template.CLOSE_DIV] + \
                      self.all_tests_table + [template.TABLE_FOOTER_TMPL] + (
                      [template.NO_DATA_FOUND] if self.Total_cases_count == 0 else [""]) + [template.CLOSE_DIV] + \
                      self.failed_tests_table + [template.TABLE_FOOTER_TMPL] + (
                      [template.NO_DATA_FOUND] if self.Total_failed_count == 0 else [""]) + [template.CLOSE_DIV] + \
                      self.error_tests_table + [template.TABLE_FOOTER_TMPL] + (
                      [template.NO_DATA_FOUND] if self.Total_error_count == 0 else [""]) + [template.CLOSE_DIV] + \
                      self.skipped_tests_table + [template.TABLE_FOOTER_TMPL] + (
                      [template.NO_DATA_FOUND] if self.Total_skip_count == 0 else [""]) + [template.CLOSE_DIV] + \
                      self.tests_without_bugid_table + [template.TABLE_FOOTER_TMPL] + (
                      [template.NO_DATA_FOUND] if self.Total_without_bug_id_count == 0 else [""]) + [
                          template.CLOSE_DIV] + \
                      self.passed_with_bugid_tests_table + [template.TABLE_FOOTER_TMPL] + (
                      [template.NO_DATA_FOUND] if self.Total_passed_with_bug_id_count == 0 else [""]) + [
                          template.CLOSE_DIV] + \
                      [template.ERROR_POPUP] + [template.HTML_END_TMPL]

        return "".join(html_output)

    def get_build_details(self, **kwargs):
        jenkins_details = list()
        if "build_no" in kwargs:
            jenkins_details.append(template.BUILD_DETAIL_TMPL % dict(key="BUILD NO", value=str(kwargs["build_no"])))
        if "build_url" in kwargs:
            url = '<a href="'+str(kwargs["build_url"])+'">'+str(kwargs["build_url"])+'</a>'
            jenkins_details.append(template.BUILD_DETAIL_TMPL % dict(key="BUILD URL", value=url))
        if "git_branch" in kwargs:
            jenkins_details.append(template.BUILD_DETAIL_TMPL % dict(key="GIT BRANCH", value=str(kwargs["git_branch"])))
        return "\n".join(jenkins_details)

    def _create_summary_table(self, class_name, suite_info):
        tr_class = "danger" if suite_info.failed_count + suite_info.error_count > 0 else "success"
        row = template.SUMMARY_TABLE_ROW_TMPL % dict(test_class=class_name, total=suite_info.total_count,
                                                     passed=suite_info.passed_count, failed=suite_info.failed_count,
                                                     error=suite_info.error_count, skipped=suite_info.skipped_count,
                                                     tr_class=tr_class, bug_list=", ".join(suite_info.bugs))
        self.summary_table.append(row)

    def get_color_status(self, case):
        if str(case.status).lower() in ['failed', 'error']:
            return "danger", template.ALL_FAILED_TESTS_TABLE_BODY_TMPL, template.BUGS_ROW
        elif str(case.status).lower() == 'passed':
            return "success", template.ALL_PASSED_TESTS_TABLE_BODY_TMPL, template.PASSED_TEST_CASE_COL
        elif str(case.status).lower() == 'skipped':
            return "warning", template.ALL_PASSED_TESTS_TABLE_BODY_TMPL, template.PASSED_TEST_CASE_COL

    def _create_all_tests_table(self, class_name, suite_info):
        tests_len = len(suite_info.test_case_info)
        self.all_tests_table.append(template.TEST_CLASS_ROW % dict(test_case_count=suite_info.suite_bug_count,
                                                                   test_class=class_name))
        for i, case in enumerate(suite_info.test_case_info):

            color_status, row_to_append, test_case_col = self.get_color_status(case)

            self.Total_cases_count += 1
            error_msg = str(case.error_msg).replace('"', '`').replace('\'', '`').replace('\n', '<br>')
            row = test_case_col % dict(bug_error=error_msg, test_case=case.test_case_name,
                                       bug_count=len(case.bug_details), col_status=color_status)
            self.all_tests_table.append(row)

            for bug_detail in case.bug_details:
                row_data = dict(bug_url=bug_detail.url,
                                bug_id=bug_detail.id, bug_summary=bug_detail.summary,
                                bug_status=bug_detail.status, priority=bug_detail.priority,
                                assignee=bug_detail.assignee, test_status=case.status,
                                bug_error=case.error_msg, test_case=case.test_case_name,
                                bug_count=len(case.bug_details), row_status=color_status
                                )
                self.all_tests_table.append(row_to_append % row_data)
                if i != 0:
                    self.all_tests_table.append("<tr>")

    def _create_failed_tests_table(self, class_name, suite_info):
        self._create_table(class_name, suite_info, 'failed', self.failed_tests_table)

    def _create_error_tests_table(self, class_name, suite_info):
        self._create_table(class_name, suite_info, 'error', self.error_tests_table)

    def _create_passed_with_bugid_tests_table(self, class_name, suite_info):
        self._create_table(class_name, suite_info, 'passed', self.passed_with_bugid_tests_table)

    def _create_table(self, class_name, suite_info, status, table_list):
        cases = filter(lambda info: str(info.status).lower() == status, suite_info.test_case_info)
        #cases_without_bug_id = filter(lambda c: len(c.bug_details) == 0, cases)
        row_span_length, with_out_bug_count = self._get_rowspan_length(cases, status)

        if status.lower() == 'passed':
            cases = self._get_passed_without_bug_id(cases)
            self.Total_passed_with_bug_id_count += row_span_length
            if row_span_length > 0:
                table_list.append(template.TEST_CLASS_ROW % dict(test_case_count=row_span_length, test_class=class_name))

        tests_len = len(cases)

        if status.lower() in ['failed', 'error']:
            self.Total_without_bug_id_count += with_out_bug_count

        if status == 'failed':
            self.Total_failed_count += tests_len
        elif status == 'error':
            self.Total_error_count += tests_len

        if len(cases) > 0 and status.lower() in ['failed', 'error']:
            table_list.append(template.TEST_CLASS_ROW % dict(test_case_count=row_span_length,
                                                             test_class=class_name))

        if with_out_bug_count > 0:
            self.tests_without_bugid_table.append(template.TEST_CLASS_ROW % dict(test_case_count=with_out_bug_count,
                                                                                 test_class=class_name))

        for i, case in enumerate(cases):
            color_status, row_to_append, test_case_col = self.get_color_status(case)
            error_msg = str(case.error_msg).replace('"', '`').replace('\'', '`').replace('\n', '<br>')
            row = test_case_col % dict(bug_error=error_msg, test_case=case.test_case_name,
                                       bug_count=len(case.bug_details), col_status=color_status)
            table_list.append(row)
            for bug_detail in case.bug_details:
                row = template.FAILED_TESTS_TABLE_BODY_TMPL % dict(bug_url=bug_detail.url, col_status=color_status,
                                                                   bug_id=bug_detail.id,
                                                                   bug_summary=bug_detail.summary,
                                                                   bug_status=bug_detail.status,
                                                                   priority=bug_detail.priority,
                                                                   assignee=bug_detail.assignee)
                table_list.append(row)
                if bug_detail.id.lower() == 'No Bug id'.lower():
                    row = template.WITH_OUT_BUGID_TESTS_TABLE_BODY % dict(bug_error=error_msg, row_status='danger',
                                                                          test_case=case.test_case_name)
                    self.tests_without_bugid_table.append(row)
                if i != 0:
                    table_list.append("<tr>")

                if bug_detail.id.lower() == 'No Bug id'.lower() and i != 0:
                    self.tests_without_bugid_table.append("<tr>")

    def _get_rowspan_length(self, cases, status):
        filtered_cases = 0
        with_out_bug_list = 0
        for case in cases:
            for bug_detail in case.bug_details:
                if bug_detail.id != '-':
                    filtered_cases += 1
                if bug_detail.id.lower() == 'No Bug id'.lower():
                    with_out_bug_list += 1
        return filtered_cases, with_out_bug_list

    def _get_passed_without_bug_id(self, cases):
        passed_without_bug = list()
        for case in cases:
            should_add = False
            for bug_detail in case.bug_details:
                if bug_detail.id != '-':
                    should_add = True
                    break
            if should_add:
                passed_without_bug.append(case)
        return passed_without_bug


    def _create_skipped_table(self, class_name, suite_info):
        skipped_cases = filter(lambda info: str(info.status).lower() == 'skipped', suite_info.test_case_info)
        tests_len = len(skipped_cases)
        self.Total_skip_count += tests_len
        if len(skipped_cases) > 0:
            self.skipped_tests_table.append(
                template.TEST_CLASS_ROW % dict(test_case_count=tests_len, test_class=class_name))
        for i, case in enumerate(skipped_cases):
            error_msg = str(case.error_msg).replace('"', '`').replace('\'', '`').replace('\n', '<br>')
            row = template.SKIPPED_TESTS_TABLE_BODY % dict(bug_error=error_msg, test_case=case.test_case_name,
                                                           row_status='warning')
            self.skipped_tests_table.append(row)
            if i != 0:
                self.skipped_tests_table.append("<tr>")

    def _create_summary_count_table(self, class_count):
        summary_count_table = list()
        summary_count_table.append(template.SUMMARY_COUNT_TABLE_HEADER)
        passed_count = self.Total_cases_count - (
        self.Total_error_count + self.Total_skip_count + self.Total_failed_count)
        row = template.SUMMARY_COUNT_TABLE_ROW_TMPL % dict(test_class_count=class_count,
                                                           test_case_count=self.Total_cases_count,
                                                           passed_count=passed_count,
                                                           failed_count=self.Total_failed_count,
                                                           error_count=self.Total_error_count,
                                                           skipped_count=self.Total_skip_count,
                                                           )
        summary_count_table.append(row)
        return summary_count_table
