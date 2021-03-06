
import subprocess
import os

scan_log_messages = {
    "safesql_start_message": "\nINFO: Running [safesql]...",
    "safesql_success_message": "You're safe from SQL injection! Yay \o/",
    "safe_sql_no_issues": "INFO: NO ISSUES DETECTED during [safesql] scan for GO project at: {0}",
    "safe_sql_issues_detected": "\nISSUES DETECTED during [safesql] scan for GO project at: {0}",
    "safe_sql_run_error": "ERROR: [safesql] exit with an error code {0} and following message \n{1}",
    "gas_start_message": "\nINFO: Running [GoASTScanner]...",
    ## "gas_success_message": "*****Write******", ## Redundant
    "gas_sql_no_issues": "INFO: NO ISSUES DETECTED during [GoASTScanner] scan for GO project at : {0}",
    "gas_sql_run_error": "ERROR: [GoASTScanner] exit with an error code {0} and following message \n{1}",
    "gas_sql_issues_detected": "INFO: ISSUES DETECTED during [GoASTScanner] scan for GO project at : {0}"
}

class ScannerWraps:


    def rungas(self, path_to_code_to_scan, curr_gopath):
        '''
        ScannerWraps The method [rungas] will run the GoASTScanner on the GO files in the path supplied
        :param path_to_code_to_scan:
        :return:
        '''
        print(scan_log_messages["gas_start_message"])
        ## Check if path_to_code_scan exists
        ## before trying chdir
        wd = os.path.join(curr_gopath,"src/",path_to_code_to_scan)
        if not ScannerWraps.checkforvaliddirectory(wd.strip()):
            return False
        os.chdir(wd)

        resultsfile = "RESULT_GoAST_SCAN.json"  # The file where GoAST Scan results will be written to

        try:
            gas_run = subprocess.Popen(["gas", "-fmt=json", "-out="+ resultsfile, "./..."],
                                       cwd= os.getcwd(),
                                       stdout=subprocess.PIPE,
                                       stderr=subprocess.STDOUT)
            print("INFO: Processing the results...")

            gas_return_code = gas_run.wait()
            gas_result = gas_run.stdout.read().decode("utf-8")
            if gas_return_code>=0:
                print(("INFO: Scan results written to: {0}/{1}".format(wd, resultsfile)))
            else:
                print(scan_log_messages["gas_sql_run_error"].format(gas_return_code, gas_result))
            return True
        except Exception as err:
            print(str(err))
            return False



    def runsafesql(self, path_to_code_to_scan, curr_gopath):

        '''
        The method [runsafesql] will be used to run safesql on the code files in path_to_code_to_scan
        :param path_to_code_to_scan:
        :return True/False:
        '''
        print(scan_log_messages["safesql_start_message"])
        try:
            wd = os.path.join(curr_gopath,"src/",path_to_code_to_scan)
            if not ScannerWraps.checkforvaliddirectory(wd.strip()):
                return False

            safesql_run = subprocess.Popen(["safesql", path_to_code_to_scan], stdout=subprocess.PIPE,
                                           stderr=subprocess.STDOUT)
            print("INFO: Processing the results...")
            safesql_return_code = safesql_run.wait()
            safesql_result = safesql_run.stdout.read().decode("utf-8")

            if safesql_return_code == 0:
                if safesql_result.strip() == scan_log_messages["safesql_success_message"]:
                    print(scan_log_messages["safe_sql_no_issues"].format(path_to_code_to_scan))
                else:
                    print(scan_log_messages["safe_sql_issues_detected"].format(path_to_code_to_scan))
            else:
                print(scan_log_messages["safe_sql_run_error"].format(safesql_return_code,safesql_result))
        except:
            raise


    def checkforvaliddirectory(path_to_code_to_scan):
        '''
        Check if the directory to scan provided exists or not
        :param path_to_code_to_scan:
        :return True/False:
        '''
        if not os.path.isdir(path_to_code_to_scan):
            print("\nERROR: The path to scan is not a valid directory: {0}".format(path_to_code_to_scan))
            return False
        return True
