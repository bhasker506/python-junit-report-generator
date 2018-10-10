'''
@author : breddy
@author : usharma
'''
HTML_HEAD_TMPL = """
<!DOCTYPE html>
<html lang="en">
  <head>
  	<title>%(report_title)s</title>
  	<meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css">
  	<script src="https://ajax.googleapis.com/ajax/libs/jquery/3.1.1/jquery.min.js"></script>
  	<script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/js/bootstrap.min.js"></script>
  	<style>
  		body {padding-top: 20px; overflow-x:hidden}
  		thead th {background-color: #708090; color: white;}
        .popover.fade.in { overflow-x:auto;}
        .panel-default > .panel-heading-custom{
          background-image: none;
          background-color: #0F70B1;
          color: #ffffff;}
	</style>
  </head>
  <body>

    <script>
		$(document).ready(function(){
		    $('[data-toggle="popover"]').popover();
		});

		model_error = function(err_msg){
		    var error_class = document.getElementsByClassName("error_msg")
		    error_class[0].innerHTML = err_msg
		}

    </script>

  	<div class="container-fluid">
  	        <div class="panel panel-default">
  	            <div class="panel-heading panel-heading-custom">
                  <h2 align="center">%(report_title)s</h2>
               </div>
               <div class="panel-body">
                  <table class="table">
                    <tbody>
                     %(build_details)s
                     </tbody>
                 </table>
               </div>
  	        </div>
  		    <ul class="nav nav-pills nav-justified" style="margin-top: 40px">
	  		<li class="active"><a data-toggle="pill" href="#tests_summary">Summary</a></li>
	  		<li><a data-toggle="pill" href="#all_tests">All Tests</a></li>
	  		<li><a data-toggle="pill" href="#failed_tests">Failed</a></li>
	  		<li><a data-toggle="pill" href="#error_tests">Error</a></li>
	  		<li><a data-toggle="pill" href="#skipped_tests">Skipped</a></li>
	  		<li><a data-toggle="pill" href="#with_out_bug">Without BugID</a></li>
	  		<li><a data-toggle="pill" href="#passed_with_bugid">Passed With BugId</a></li>
  		</ul>
"""

BUILD_DETAIL_TMPL = """<tr class="info"><td>%(key)s</td><td>%(value)s</td></tr>"""

SUMMARY_VIEW = """
  		<div class="tab-content" style="margin-top: 25px">
  			<div id="tests_summary" class="table-responsive tab-pane fade in active">
  			"""
SUMMARY_TABLE_HEADER_TMPL = """
		  		<table style="margin-top: 25px" class="table table-hover table-striped table-bordered">
		  			<thead>
						<tr>
							<th>Class Name</th>
							<th>Total</th>
							<th>Passed</th>
							<th>Failed</th>
							<th>Error</th>
							<th>Skipped</th>
							<th>Bug ID List</th>
						</tr>
	    			</thead>
	    			<tbody>
"""

SUMMARY_COUNT_TABLE_HEADER = """
		  		<table style="margin-top: 25px" class="table table-hover table-striped table-bordered">
		  			<thead>
						<tr>
							<th>Total Classes</th>
							<th>Total Cases</th>
							<th>Total Passed</th>
							<th>Total Failed</th>
							<th>Total Errors</th>
							<th>Total Skipped</th>
						</tr>
	    			</thead>
	    			<tbody>
"""

SUMMARY_COUNT_TABLE_ROW_TMPL="""
						<tr class="info">
							<td>%(test_class_count)s</td>
							<td>%(test_case_count)s</td>
							<td>%(passed_count)s</td>
							<td>%(failed_count)s</td>
							<td>%(error_count)s</td>
							<td>%(skipped_count)s</td>
						</tr>
"""

SUMMARY_TABLE_ROW_TMPL="""
						<tr class="%(tr_class)s">
							<td>%(test_class)s</td>
							<td>%(total)s</td>
							<td>%(passed)s</td>
							<td>%(failed)s</td>
							<td>%(error)s</td>
							<td>%(skipped)s</td>
							<td>%(bug_list)s</td>
						</tr>
"""

TABLE_FOOTER_TMPL = """</tbody></table>"""

FAILED_TESTS_TABLE_HEADER_TMPL = """
	  		<div id="%(id_refrence)s" class="table-responsive tab-pane fade">
		  		<table class="table table-bordered">
		  			<thead>
						<tr>
						    <th>Class Name</th>
							<th>TestCase Name</th>
							<th>Bug ID</th>
							<th>Bug Status</th>
							<th>Priority</th>
							<th>Assigned To</th>
						</tr>
	    			</thead>
	    			<tbody>
"""

BUGS_ROW = """<td style="border: solid thin; vertical-align: middle;" class="%(col_status)s" rowspan=%(bug_count)s>
				<a class="test_case" href="javascript:void(0);" onclick="model_error('%(bug_error)s')" data-toggle="modal" data-target="#err_modal">%(test_case)s</a>
			</td>
		    """

PASSED_TEST_CASE_COL = """<td style="border: solid thin; vertical-align: middle;" class="%(col_status)s" rowspan=%(bug_count)s>
				<a class="test_case" href="javascript:void(0);" data-toggle="popover" data-trigger="focus" data-placement="right" data-content="%(bug_error)s">%(test_case)s</a>
			</td>
		    """
FAILED_TESTS_TABLE_BODY_TMPL = """
							<td style="border: solid thin;" class="%(col_status)s">
								<a href="%(bug_url)s" data-toggle="popover" data-trigger="hover" data-placement="right" data-content="%(bug_summary)s">%(bug_id)s</a>
							</td>
							<td style="border: solid thin;" class="%(col_status)s">%(bug_status)s</td>
							<td style="border: solid thin;" class="%(col_status)s">%(priority)s</td>
							<td style="border: solid thin;" class="%(col_status)s">%(assignee)s</td>
						</tr>
"""

PASSED_TESTS_TABLE_BODY_TMPL = """
							<td style="border: solid thin;" class="success">
								<a href="%(bug_url)s" data-toggle="popover" data-trigger="hover" data-placement="right" data-content="%(bug_summary)s">%(bug_id)s</a>
							</td>
							<td style="border: solid thin;" class="success">%(bug_status)s</td>
							<td style="border: solid thin;" class="success">%(priority)s</td>
							<td style="border: solid thin;" class="success">%(assignee)s</td>
						</tr>
"""

TEST_CLASS_ROW = """<tr><td style="vertical-align: middle;" rowspan=%(test_case_count)s>%(test_class)s</td>"""

ALL_TESTS_TABLE_HEADER_TMPL = """
	  		<div id="all_tests" class="table-responsive tab-pane fade">
		  		<table class="table table-bordered">
		  			<thead>
						<tr>
							<th>Class Name</th>
							<th>TestCase Name</th>
							<th>Test Status</th>
							<th>Bug ID</th>
							<th>Bug Status</th>
							<th>Priority</th>
							<th>Assigned To</th>
						</tr>
	    			</thead>
	    			<tbody>
"""

ALL_PASSED_TESTS_TABLE_BODY_TMPL = """
							<td style="border: solid thin;" class="%(row_status)s">%(test_status)s</td>
							<td style="border: solid thin;" class="%(row_status)s">
								<a href="%(bug_url)s" data-toggle="popover" data-trigger="hover" data-placement="right" data-content="%(bug_summary)s">%(bug_id)s</a>
							</td>
							<td style="border: solid thin;" class="%(row_status)s">%(bug_status)s</td>
							<td style="border: solid thin;" class="%(row_status)s">%(priority)s</td>
							<td style="border: solid thin;" class="%(row_status)s">%(assignee)s</td>
						</tr>
"""

ALL_FAILED_TESTS_TABLE_BODY_TMPL = """
							<td style="border: solid thin;" class="%(row_status)s">%(test_status)s</td>
							<td style="border: solid thin;" class="%(row_status)s">
								<a href="%(bug_url)s" data-toggle="popover" data-trigger="hover" data-placement="right" data-content="%(bug_summary)s">%(bug_id)s</a>
							</td>
							<td style="border: solid thin;" class="%(row_status)s">%(bug_status)s</td>
							<td style="border: solid thin;" class="%(row_status)s">%(priority)s</td>
							<td style="border: solid thin;" class="%(row_status)s">%(assignee)s</td>
						</tr>
"""

SKIPPED_TESTS_TABLE_HEADER = """
	  		<div id="%(id_refrence)s" class="table-responsive tab-pane fade">
		  		<table class="table table-bordered">
		  			<thead>
						<tr>
							<th>Class Name</th>
							<th>TestCase Name</th>
						</tr>
	    			</thead>
	    			<tbody>
"""
SKIPPED_TESTS_TABLE_BODY = """
<td class="%(row_status)s">
    <a class="test_case" href="javascript:void(0);" data-toggle="popover" data-trigger="focus" data-placement="right" data-content="%(bug_error)s">%(test_case)s</a>
</td>
</tr>
"""

WITH_OUT_BUGID_TESTS_TABLE_BODY = """
<td class="%(row_status)s">
    <a class="test_case" href="javascript:void(0);" onclick="model_error('%(bug_error)s')" data-toggle="modal" data-target="#err_modal">%(test_case)s</a>
</td>
</tr>
"""


ERROR_POPUP = """
<div class="modal fade" id="err_modal" role="dialog">
    <div class="modal-dialog modal-lg">
      <div class="modal-content">
        <div class="modal-header">
          <button type="button" class="close" data-dismiss="modal">&times;</button>
          <h4 class="modal-title">Error Message</h4>
        </div>
        <div class="modal-body">
          <p class="error_msg"></p>
        </div>
      </div>
    </div>
  </div>
"""
NO_DATA_FOUND = """<div align="center"> No Data Found </div>"""
CLOSE_DIV = """</div>"""
HTML_END_TMPL = """</body></html>"""