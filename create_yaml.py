import yaml
import toml

# config.tomlの読み込み
config = toml.load('config.toml')

# config.tomlから値を取得
region = config['project']['region']
project_id = config['project']['project_id']
repo = config['project']['repo']
image = config['project']['image']

# YAMLの内容を辞書で定義
data = {
    'on': {
        'push': {
            'branches': ['main']
        }
    },
    'jobs': {
        'deploy': {
            'runs-on': 'ubuntu-latest',
            'permissions': {
                'id-token': 'write',
                'contents': 'read'
            },
            'steps': [
                {
                    'name': 'Checkout code',
                    'uses': 'actions/checkout@v4'
                },
                {
                    'name': 'Authenticate to Google Cloud',
                    'uses': 'google-github-actions/auth@v2',
                    'with': {
                        'workload_identity_provider': '${{ secrets.GCP_WORKLOAD_IDENTITY_PROVIDER }}',
                        'service_account': '${{ secrets.SERVICE_ACCOUNT_EMAIL }}'
                    }
                },
                {
                    'name': 'Set up Cloud SDK',
                    'uses': 'google-github-actions/setup-gcloud@v2'
                },
                {
                    'name': 'Configure Docker to use gcloud credentials',
                    'run': f'gcloud auth configure-docker {region}-docker.pkg.dev'
                },
                {
                    'name': 'Build and push Docker image',
                    'env': {
                        'REGION': region,
                        'PROJECT_ID': project_id,
                        'REPO': repo,
                        'IMAGE': image
                    },
                    'run': f'''docker build -t {region}-docker.pkg.dev/{project_id}/{repo}/{image}:latest .
                               docker push {region}-docker.pkg.dev/{project_id}/{repo}/{image}:latest'''
                },
                {
                    'name': 'Deploy to Cloud Run',
                    'run': f'''gcloud run deploy {image} \
                               --image {region}-docker.pkg.dev/{project_id}/{repo}/{image}:latest \
                               --region {region} \
                               --allow-unauthenticated'''
                }
            ]
        }
    }
}

# YAMLファイルに出力
with open("cloud_run_deploy.yml", "w") as file:
    yaml.dump(data, file, default_flow_style=False)

print("YAMLファイルが生成されました: cloud_run_deploy.yml")
