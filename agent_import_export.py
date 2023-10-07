import argparse
import subprocess

#  export GOOGLE_APPLICATION_CREDENTIALS=./gcloud.json 

def import_agent(agent_dir, project_id):
    # Run the gcloud command to import the agent
    cmd = [
        'gcloud',
        'alpha',
        'dialogflow',
        'agent',
        'import',
        '--project=' + project_id,
        '--source=' + agent_dir
    ]

    subprocess.run(cmd)


def export_agent(agent_dir, project_id):

    cmd = [
        'gcloud',
        'alpha',
        'dialogflow',
        'agent',
        'export',
        '--project=' + project_id,
        '--destination=' + agent_dir
    ]

    # Run the gcloud command to export the agent
    subprocess.run(cmd)

# Example usage:
# export_agent('your-agent-id', 'local-export-directory', 'your-project-id')

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Preform import and export tasks with Dialogflow agent")
    parser.add_argument("--import-zip", required=False, help="Path to the ZIP file containing the agent")
    parser.add_argument("--export-zip", required=False, help="Target Path to the ZIP file containing the agent")
    parser.add_argument("--project-id", required=True, help="Your Google Cloud project ID")

    args = parser.parse_args()

    import_file_dir = args.import_zip
    export_file_dir = args.export_zip
    project_id = args.project_id

    if export_file_dir:
        export_agent(export_file_dir, project_id )

    if import_file_dir:
        import_agent(import_file_dir, project_id)



# python3 agent_import_export.py --export-zip ./exports/exported_agent.zip --project-id nlpchatbot-utan 

#unzip ./exports/exported_agent.zip -d ./exports 

# ngrok http 8000

#zip imports/from_export.zip -r ./exports/*

# python3 agent_import_export.py --import-zip ./imports/from_export.zip --project-id nlpchatbot-utan 

# rm -rf ./exports/*  && rm -rf ./imports/*