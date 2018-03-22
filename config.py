import sys
import os
import xmltodict

def validate_student(config):
    error = ''
    error = validate_param('student_id', config)
    error = validate_param('student_name', config)
    error = validate_param('site_path', config)
    error = validate_param('username', config)
    error = validate_param('password', config)
    error = validate_param('calendar_id', config)
    if error == '':
        return 'Config ok'
    else:
        return error


def validate_param(param, config):
    error = ''
    try:
        x = config[param]
        if len(x) > 0:
            pass
        else:
            error = 'Blank ' + str(param)
    except:
        error = 'Missing ' + str(param)
    return error

def read_config(configfile):
    with open(configfile) as f:
        root = xmltodict.parse(f)
    students = []
    config_students = root['configuration']['students']
    for i in range (len(config_students)):
        students.append(config_students['student'])
    for i in range(len(students)):
        status = ''
        if validate_student(students[i]) == 'Config ok':
            status = ''
        else:
            print 'Config errors for student ' + str(students[i]['student_id'])
            status = 'Error'
    if status == '':
        return students
    else:
        return 'Error'








