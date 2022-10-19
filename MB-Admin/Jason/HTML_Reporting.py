'''
    HTML Reporting for Selenium using Python

    To use:
        - instantiate a TestSuiteReporter object
            > reporter = TestSuiteReporter("Test Name", "output/file/path", "tester's name")
        - append a test case to the reporter object
            > reporter.addTestCase("testcasereferencename", "Test Case ID Code", "Test Case Decription")
        - report a test step (refer to the declared name of the test)
            > reporter["testcasereferencename"].reportStep(
                "description",
                "expected behavior",
                "actual behavior",
                teststatus, # boolean
                dataString, # String describing any data used (optional)
                screenshotCallback, # function to invoke with the other imagePath parameter (optional)
                imagePath, # file path to save screenshot to with the callback function (optional)
                imageEmbed, # whether or not to embed the screenshot as an image in the report (not a link), or not (optional)
            )
        - report a non-tested event (refer to the declared name of the test) 
            > reporter["testcasereferencename"].reportEvent(
                "description",
                warning, # boolean, defaults to False -- False = "DONE", True = "WARNING" (optional)
                dataString, # String describing any data used (optional)
                screenshotCallback, # function to invoke with the other imagePath parameter (optional)
                imagePath, # file path to save screenshot to with the callback function (optional)
                imageEmbed, # whether or not to embed the screenshot as an image in the report (not a link), or not (optional)
            )
'''


from dataclasses import dataclass
from datetime import datetime
from os import mkdir, path
from shutil import copy
from typing import Callable
from typing import Union


@dataclass
class _TestEvent:
    eventDescription: str
    warning: bool = False   # WARNING = true, DONE = false
    dataString: str = ''
    imagePath: str = ''
    imageEmbed: bool = False

    def __post_init__(self):
        self.statusColor = "yellow" if self.warning else "antiquewhite"
        self.statusString = "WARNING" if self.warning else "DONE"


@dataclass
class _TestStep:
    stepDescription: str
    expectedBehavior: str
    actualBehavior: str
    testStatus: bool   # PASS = true, FAIL = false
    dataString: str = ''
    imagePath: str = ''
    imageEmbed: bool = False
    
    def __post_init__(self):
        self.statusColor = "green" if self.testStatus else "red"
        self.statusString = "PASS" if self.testStatus else "FAIL"


@dataclass
class TestCase:
    testCaseID: str
    testCaseDescription: str
    testerName: str
    screenshotPath: Union[str, None] = None

    def __post_init__(self):
        '''Sets up other object values after dataclass initiation'''
        self.steps = []
        self.testStatus = 1
        if self.screenshotPath in [None, '']:
            self.screenshotPath = self.testCaseID.replace(" ", "").replace("\\", "_").replace("/", "_")
        if not path.exists(self.screenshotPath):
            mkdir(self.screenshotPath)
    
    def reportEvent(
        self,
        eventDescription: str,
        warning: bool = False,
        dataString: str = '',
        screenshotCallback: Union[Callable, None] = None,
        imagePath: str = '',
        imageEmbed: bool = False
    ):
        '''Registers a new test case event'''
        if screenshotCallback is not None:
            outPath = self._screenshot(screenshotCallback, imagePath, eventDescription)
        else:
            outPath = ''
        self.steps.append(
            _TestEvent(
                eventDescription,
                warning,
                dataString,
                outPath,
                imageEmbed
            )
        )
        
        if warning and not self.testStatus:
            self.testStatus = 2
    
    def reportStep(
        self,
        stepDescription: str,
        expectedBehavior: str,
        actualBehavior: str,
        testStatus: bool,
        dataString: str = '',
        screenshotCallback: Union[Callable, None] = None,
        imagePath: str = '',
        imageEmbed: bool = False
    ):
        '''Registers a new test case step'''
        if screenshotCallback is not None:
            outPath = self._screenshot(screenshotCallback, imagePath, stepDescription)
        else:
            outPath = ''
        self.steps.append(
            _TestStep(
                stepDescription,
                expectedBehavior,
                actualBehavior,
                testStatus,
                dataString,
                outPath, 
                imageEmbed
            )
        )

        if self.testStatus == 1:
            if not testStatus:
                self.testStatus = 0
        
    def _screenshot(self, callback, imagePath, description):
        '''Utility function that generalizes the screenshotting functionality'''
        if imagePath == '':
            pathSuffix = description.replace("/", "_").replace("\\", "_") + ".png"
        else:
            pathSuffix = imagePath
        outPath = path.join(self.screenshotPath, pathSuffix)
        if outPath[-4:] != ".png":
            outPath = outPath + ".png"
        callback(outPath)
        return outPath

    def statusColor(self):
        '''Returns the HTML color keyword for the appropriate test case status'''
        if self.testStatus == 0:
            return "red"
        elif self.testStatus == 1:
            return "green"
        else:
            return "yellow"

    def statusString(self):
        '''Returns the keyword for the appropriate test status'''
        if self.testStatus == 0:
            return "FAIL"
        elif self.testStatus == 1:
            return "PASS"
        else:
            return "WARNING"


class TestSuiteReporter:

    def __init__(
        self,
        testName: str, 
        outputPath: Union[str, None] = None,
        testerName: str = 'Doug Walter'
    ):
        self.testName = testName
        self.outputPath = outputPath
        if self.outputPath is None:
            self.outputPath = ' '.join(self.testName, str(datetime.now()))
        if not path.exists(self.outputPath):
            mkdir(self.outputPath)
        #self.screenshot_path = path.join(outputPath, '.screenshots')
        self.screenshot_path = '.screenshots'
        if not path.exists(self.screenshot_path):
            mkdir(self.screenshot_path)
        self.testerName = testerName
        self._testCases = {}

    def __del__(self):
        '''Deconstructor that writes report when cleaned up'''
        self.saveReport(self.outputPath)
    
    def __getitem__(self, key):
        '''Pass-through reference to the test cases dictionary'''
        return self._testCases[key]

    def addTestCase(
        self,
        testName: str,
        testCaseID: str,
        testCaseDescription: str,
        screenshotPath: str = ''
    ):
        '''Adds a new named test case to this suite'''
        if screenshotPath == '':
            screenshotPath = testName.replace(" ", "").replace("/", "_").replace("\\", "_")
        outPath = path.join(self.screenshot_path, screenshotPath)
        self._testCases[testName] = TestCase(
            testCaseID,
            testCaseDescription,
            self.testerName,
            outPath
        )

    def saveReport(self, outPath):
        '''Writes the report for this test suite'''
        with open(path.join(outPath, self.testName + '.html'), mode='a', encoding='UTF-8') as outfile:

            # open html and body
            outfile.write('<html><body>')

            # write test report header
            outfile.write(f'<h3>{self.testName} - run {datetime.now()} by {self.testerName}</h3>')

            # iterate over test cases
            for case in sorted(self._testCases.values(), key=lambda a: a.testCaseID):

                # write test case description
                tableStyleString = 'style="width: 1000px;margin: 0;padding: 0;table-layout: fixed;border-collapse: collapse;font: 11px/1.4 Trebuchet MS;"'
                tableHeaderStyleString = 'style="margin: 0;padding: 0;"'
                outfile.write(f'<table {tableStyleString}><thead {tableHeaderStyleString}><tr {tableHeaderStyleString}>')
                for text, width in zip(["TCID", "Description", "Status"], [100, 700, 200]):
                    outfile.write(f'<th style="width: {width}px;margin: 0;padding: 6px;background: #333;color: white;font-weight: bold;border: 1px solid #ccc;text-align: auto;">{text}</th>')
                outfile.write(f'</tr></thead><tbody><tr>')
                for text, width in zip([case.testCaseID, case.testCaseDescription], [100, 700]):
                    outfile.write(f'<th style="width: {width}px;margin: 0;padding: 6px;background: white;color: black;font-weight: bold;border: 1px solid #ccc;text-align: auto;">{text}</th>')
                outfile.write(f'<th style="width: 200px;margin: 0;padding: 6px;background: {case.statusColor()};color: black;font-weight: bold;border: 1px solid #ccc;text-align: auto;">{case.statusString()}</th>')
                outfile.write(f'</tr></tbody></table>')

                # write steps header
                outfile.write(f'<details><summary>Step Details</summary><table {tableStyleString}><thead {tableHeaderStyleString}><tr {tableHeaderStyleString}>')
                for text, width in zip(["Step #", "Description", "Expected Behavior", "Actual Behavior", "Status", "Test Data", "Screenshot"], [50, 200, 300, 300, 50, 250, 400]):
                    outfile.write(f'<th style="width: {width}px;margin: 0;padding: 6px;background: #333;color: white;font-weight: bold;border: 1px solid #ccc;text-align: auto;">{text}</th>')
                outfile.write('</tr></thead>')

                # write test steps
                outfile.write(f'<tbody {tableHeaderStyleString}>')
                for i, step in enumerate(case.steps, start=1):
                    outfile.write(f'<tr><th style="width: 50px;margin: 0;padding: 6px;background: white;color: black;font-weight: bold;border: 1px solid #ccc;text-align: auto;">{i}</th>')
                    if isinstance(step, _TestStep):
                        outfile.write(f'<th style="width: 200px;margin: 0;padding: 6px;background: white;color: black;font-weight: bold;border: 1px solid #ccc;text-align: auto;">{step.stepDescription}</th>')
                        outfile.write(f'<th style="width: 300px;margin: 0;padding: 6px;background: white;color: black;font-weight: bold;border: 1px solid #ccc;text-align: auto;">{step.expectedBehavior}</th>')
                        outfile.write(f'<th style="width: 300px;margin: 0;padding: 6px;background: white;color: black;font-weight: bold;border: 1px solid #ccc;text-align: auto;">{step.actualBehavior}</th>')
                    else:
                        outfile.write(f'<th style="width: 300px;margin: 0;padding: 6px;background: white;color: black;font-weight: bold;border: 1px solid #ccc;text-align: auto;">{step.eventDescription}</th>')
                        outfile.write(f'<th style="width: 200px;margin: 0;padding: 6px;background: white;color: black;font-weight: bold;border: 1px solid #ccc;text-align: auto;"></th>')
                        outfile.write(f'<th style="width: 300px;margin: 0;padding: 6px;background: white;color: black;font-weight: bold;border: 1px solid #ccc;text-align: auto;"></th>')
                    outfile.write(f'<th style="width: 50px;margin: 0;padding: 6px;background: {step.statusColor};color: black;font-weight: bold;border: 1px solid #ccc;text-align: auto;">{step.statusString}</th>')
                    outfile.write(f'<th style="width: 250px;margin: 0;padding: 6px;background: white;color: black;font-weight: bold;border: 1px solid #ccc;text-align: auto;">{step.dataString}</th>')
                    if step.imagePath == '':
                        outfile.write(f'<th style="width: 400px;margin: 0;padding: 6px;background: white;color: black;font-weight: bold;border: 1px solid #ccc;text-align: auto;">N/A</th>')
                    else:
                        if step.imageEmbed:
                            outfile.write(f'<th style="width: 400px;margin: 0;padding: 6px;background: white;color: black;font-weight: bold;border: 1px solid #ccc;text-align: auto;"><image src="{step.imagePath}"></image></th>')
                        else:
                            outfile.write(f'<th style="width: 400px;margin: 0;padding: 6px;background: white;color: black;font-weight: bold;border: 1px solid #ccc;text-align: auto;"><a href="{step.imagePath}" target="_blank">Link</a></th>')
                    outfile.write('</tr>')
                outfile.write('</tbody>')

                # close step description
                outfile.write('</table></details><br><br>')

            # close html and body
            outfile.write('</body></html>')
