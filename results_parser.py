'''
@author : breddy
'''
import json
import os
import re
import requests
import unicodedata
import xml.etree.ElementTree as ET
from apitestlib.tools.html_report_generator.settings import Settings


class _TestSuiteInfo:

    def __init__(self, suit_name, test_case_info, total_count, passed_count, failed_count, error_count, skip_count,
                 bugs, suite_bug_count):
        self.suit_name = suit_name
        self.test_case_info = test_case_info
        self.total_count = total_count
        self.passed_count = passed_count
        self.failed_count = failed_count
        self.error_count = error_count
        self.skipped_count = skip_count
        self.bugs = bugs
        self.suite_bug_count = suite_bug_count

    def __str__(self):
        return "suite_name:%s\ttest_case_info: %s\ttotal_count: %s\tpassed_count: %s\tfailed_count: " \
              "%s\terror_count: %s\tskipped_count: %s" %(self.suit_name, self.test_case_info, self.total_count,
                                                         self.passed_count, self.failed_count, self.error_count,
                                                         self.skipped_count)


class _TestCaseInfo(object):

    def __init__(self, test_case_name, status, bug_details=None, error_msg=None):
        self.test_case_name = test_case_name
        self.status = status
        self.bug_details = bug_details
        self.error_msg = error_msg

    def __str__(self):
        return "test_case_name: %s\tstatus: %s\tbug_details: %s\terror_msg: %s" % (self.test_case_name, self.status,
                                                                                   self.bug_details, self.error_msg)


class _BugDetails(object):

    def __init__(self, id, status='-', summary='-', url="javascript:void(0);", priority='-', assignee='-'):
        self.id = id
        self.status = status
        self.summary = summary
        self.url = url
        self.priority = priority
        self.assignee = assignee

    def __str__(self):
        return "id: %s\tstatus: %s\tsummary: %s\t url: %s\tpriority: %s\tassignee: %s" % (self.id, self.status,
                                                                                          self.summary, self.url,
                                                                                          self.priority, self.assigne)


class TestResultsParser(object):

    def __init__(self):
        self.bug_detail_map = dict()

    def get_xmls(self, xml_report_location):
        for f in os.listdir(xml_report_location):
            if f.endswith(".xml") and f != 'pom.xml':
                yield xml_report_location+'/'+f

    def get_test_results(self, test_result_xmls):
        test_results_info = dict()
        for result in test_result_xmls:
            tree = ET.parse(result)
            test_suite = tree.getroot()
            suite_name = test_suite.get('name').split('-')[0]
            test_info_list, bug_list, suite_bug_count = self.get_test_info_from_test_suite(test_suite)
            total_count = len(test_info_list)
            failed_count = len(filter(lambda x: x.status == 'Failed', test_info_list))
            error_count = len(filter(lambda x: x.status == 'Error', test_info_list))
            passed_count = len(filter(lambda x: x.status == 'Passed', test_info_list))
            skipped_count = len(filter(lambda x: x.status == 'Skipped', test_info_list))
            test_suite_info = _TestSuiteInfo(suite_name, test_info_list, total_count, passed_count, failed_count,
                                             error_count, skipped_count, bug_list, suite_bug_count)
            test_results_info[suite_name] = test_suite_info
        return test_results_info

    def get_test_info_from_test_suite(self, test_suite):
        test_cases = test_suite.findall('testcase')
        test_info_list = list()
        bug_list = list()
        testsuite_bug_count = 0
        for test_case in test_cases:
            test_case_name = test_case.get('name')
            status = self.get_test_case_status(test_case)
            bug_details = self.get_bug_id_from_test_name(test_case_name, status) #if status in ['Failed', 'Error'] else '-'
            error_msg = self.get_error_message(test_case)
            test_info_obj = _TestCaseInfo(test_case_name, status, bug_details, error_msg.replace('"', '\''))
            test_info_list.append(test_info_obj)
            testsuite_bug_count += len(bug_details)
            for d in bug_details:
                if d.id != '-':
                    bug_list.append(d.id)
        return test_info_list, set(bug_list), testsuite_bug_count

    def check_for_number(self, str):
        try:
            int(str)
            return True
        except ValueError:
            return False

    def get_bug_id_from_test_name(self, test_name, status):
        bug_details_list = list()
        desc_list = test_name.split("_")
        jira_list = len(filter(lambda x: ((re.split('(\d+)', x)[0]).upper()) in Settings.JIRA_PROJECTS, desc_list)) > 0
        if jira_list:
            for i, test in enumerate(desc_list):
                if self.check_for_number(test):
                    continue
                else:
                    bug_id = re.split('(\d+)', test)
                    bug_project = bug_id[0]
                    bug_no = None
                    if len(bug_id) == 1 and bug_project.upper() in Settings.JIRA_PROJECTS:
                        if i != len(desc_list)-1 and self.check_for_number(desc_list[i + 1]):
                            bug_no = desc_list[i + 1]
                        else:
                            continue
                    elif len(bug_id) == 1 and bug_project.upper() not in Settings.JIRA_PROJECTS:
                        continue
                    elif bug_project.upper() in Settings.JIRA_PROJECTS:
                        bug_no = bug_id[1]

                    if bug_no:
                        bug_details_list.append(self.get_bug_details(bug_project + '-' + bug_no))
        if len(bug_details_list) == 0 and str(status).lower() in ['failed', 'error']:
            bug_details_list.append(_BugDetails('No Bug id'))

        elif len(bug_details_list) == 0 and str(status).lower() in ['passed', 'skipped']:
            bug_details_list.append(_BugDetails('-'))
        return bug_details_list

    def get_test_case_status(self, test_case):
        failure_type = None

        for error in test_case.findall('error'):
            failure_type = error.get('type')

        if failure_type:
            if str(failure_type).lower() == 'AssertionError'.lower():
                return 'Failed'
            else:
                return 'Error'

        for skip in test_case.findall('skipped'):
            failure_type = skip.get('type')

        if failure_type:
            if str(failure_type).lower() == 'skip'.lower():
                return 'Skipped'
        return 'Passed'

    def get_error_message(self, test_case):

        for error in test_case.findall('error'):
            return self.ignore_ascii(error.text)

        for error in test_case.findall('skipped'):
            return self.ignore_ascii(error.get("message"))

        return 'Passed'

    def ignore_ascii(self, message):
        if isinstance(message, unicode):
            return unicodedata.normalize('NFKD', message).encode('ascii', 'ignore')
        else:
            return message

    def get_bug_details(self, bug_id):
        try:
            if bug_id in self.bug_detail_map:
                return self.bug_detail_map[bug_id]
            else:
                url = Settings.QA_JIRA_API_URI + (Settings.QA_JIRA_API_PATH % dict(bug_id=bug_id))
                response = requests.get(url)
                bug_details = json.loads(response.text)
                summary = str(bug_details["summary"]).replace('"', '`').replace('\'', '`').replace('\n', '<br>')
                bug_detail = _BugDetails(bug_details["issue_id"], bug_details["status"], summary,
                                         bug_details["url"], bug_details["priority"], bug_details["assignee"])
                self.bug_detail_map[bug_id] = bug_detail
                return bug_detail
        except Exception:
            return _BugDetails(bug_id)
