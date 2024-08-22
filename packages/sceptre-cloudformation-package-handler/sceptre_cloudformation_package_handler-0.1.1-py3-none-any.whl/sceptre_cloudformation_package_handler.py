import os
import subprocess
import tempfile

from sceptre.template_handlers import TemplateHandler
from sceptre.template_handlers.file import File


class PackagedTemplate(TemplateHandler):

    def __init__(self, *args, **kwargs):
        super(PackagedTemplate, self).__init__(*args, **kwargs)
        self.file_handler = File(*args, **kwargs)

    def schema(self):
        return {
            'type': 'object',
            'properties': {
                'path': {'type': 'string'},
                'artifact_bucket_name': {'type': 'string'},
                'artifact_bucket_prefix': {'type': 'string'},
            },
            'required': [
                'path',
                'artifact_bucket_name',
            ]
        }
    
    def handle(self):
        template_data = self.file_handler.handle()

        with tempfile.NamedTemporaryFile(dir=os.getcwd()) as template_file:
            with open(template_file.name, 'wb') as ofile:
                ofile.write(template_data.encode('utf-8'))

            environment_variables = (
                self.connection_manager.create_session_environment_variables()
            )

            package_command = ['aws', 'cloudformation', 'package']
            package_command.extend(['--template-file', template_file.name])
            package_command.extend(['--s3-bucket', self.arguments['artifact_bucket_name']])

            if 'artifact_bucket_prefix' in self.arguments:
                package_command.extend(['--s3-prefix', self.arguments['artifact_bucket_prefix']])

            result = subprocess.run(package_command, check=True, env=environment_variables, stdout=subprocess.PIPE)
            if result.returncode != 0:
                raise Exception('Unable to run cloudformation package, process returned exit code: {}'.format(result.returncode))

            return result.stdout
