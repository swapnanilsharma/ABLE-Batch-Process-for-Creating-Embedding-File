#!/usr/bin/env python
# (C) Copyright 2019-2020, PwC
#
# @brief common python file for exceptions
#
#****************************************************************************

#****************************************************************************
# Imports
#****************************************************************************

from framework import commonLog


class DependencyException(Exception):
    """
    Exception to throw when there is an error in a dependency
    """
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return "[DEP ERROR] %s\n" % self.message


class DoesNotExistException(Exception):
    """
    Exception to throw when an object does not exist
    """
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return "[DNE ERROR] %s\n" % self.message


class PermissionDeniedException(Exception):
    """
    Exception to throw when access to a file or directory is denied
    """
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return "[PERMISSION DENIED] %s\n" % self.message


class OperationNotPermittedException(Exception):
    """
    Exception to throw when an operation is not permitted
    """
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return "[OPERATION NOT PERMITTED] %s\n" % self.message


class LogicException(Exception):
    """
    Exception to throw when something unexpected is passed to a function.
    """
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return "[LOGIC ERROR] %s\n" % self.message


class SetupException(Exception):
    """
    Exception to throw when there is an error setting up the test
    """
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return "[SETUP ERROR] %s" % self.message


class SkipException(Exception):
    """
    Exception to throw when the test is to be skipped

    Put the reason for the skip in the exception string.
    E.g. Blocked by Bug 50329
    """
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return "[TEST SKIPPED] %s" % self.message


class TestException(Exception):
    """
    Exception to throw when there is an error in the test
    """
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return "[TEST ERROR] %s\n" % self.message


class RemoteCommandException(Exception):
    """
    Exception to throw when a remote command receives a non zero exit code
    """
    def __init__(self, message, std_out=None, std_err=None, exit_code=None):
        self.message = message
        self.std_out = std_out
        self.std_err = std_err
        self.exit_code = exit_code

    def __str__(self):
        return ("[REMOTE COMMAND ERROR] The following command received the non-zero exit code: %s\n%s\n"
                % (self.exit_code, self.message))


class UnimplementedException(Exception):
    """
    Exception to throw when a test component is unimplemented
    """
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return "[UNIMPLEMENTED ERROR] %s\n" % self.message


class WarningException(Exception):
    """
    Exception to throw when there is a warning in a test
    """
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return "[WARNING] %s\n" % self.message


class RunException(Exception):
    """
    Exception to throw when there is an error running a command
    """
    def __init__(self, message, std_out=None, std_err=None, exit_code=None):
        self.message = message
        self.std_out = std_out
        self.std_err = std_err
        self.exit_code = exit_code

    def __str__(self):
        return ("[COMMAND ERROR] The following command received the non-zero exit code: %s\n%s\n"
                % (self.exit_code, self.message))


class ConfigControllerException(Exception):
    """
    Exception to throw when there is an error in run in setup or cleanup
    as executed by the config Object in the config controller.
    """
    def __init__(self, exception_list):
        self.exception_list = exception_list
        for exception, trace in self.exception_list:
            commonLog.log("%s\n%s" % (exception, trace), commonLog.LOG_LEVEL_ALWAYS)

    def __str__(self):
        return "[CONFIG CONTROLLER ERROR]\n"


class TestCaseException(Exception):
    """
    Exception to throw for specific test case failures
    """
    def __init__(self, test_case_list):
        self.test_cases = test_case_list

    def __str__(self):
        return "[TEST CASE ERROR] %s\n" % str(self.test_cases)

class MandatoryParameterError(Exception):
    """
    Exception to throw for missing mandatory parameter
    """
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return "[MISSING MANDATORY PARAMETER] %s\n" % str(self.message)
