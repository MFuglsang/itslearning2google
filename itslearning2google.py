import itslearning
import config
import os
import logs
import os.path
import google

def main():
    logs.write_log('***** Starting script *****', '')

    configuration = os.path.dirname(os.path.abspath(__file__)) + '/configuration.xml'
    suspendweekmode = -1

    students =  config.read_config(configuration)

    for i in range(len(students)):
        planfile = itslearning.construct_planfile(students[i]['student_id'],suspendweekmode)

        if os.path.isfile(planfile) == True:
            message =  'Plan exists in '+str(planfile)+', skipping...'
            logs.write_log(message, 'Skip')
        else:
            status = itslearning.request_plan(students[i]['student_id'], students[i]['student_name'], students[i]['site_path'], 'morfug', 'FM050881fi', suspendweekmode)
            if status == 'OK':
                logs.write_log('Plan retrieved to ' + str(planfile), 'Ok')
            else:
                logs.write_log(status, 'Error')


        result = google.insert(planfile, students[i]['calendar_id'], students[i]['student_id'])
        if result == '0':
            logs.write_log('Plan inserted to calendar', 'Success')
        else:
            logs.write_log(result, 'Error')

    logs.write_log('***** Script finished *****', '')

if __name__ == '__main__':
    main()