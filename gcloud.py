import subprocess
import toml

# 設定ファイルの読み込み
config = toml.load("config.toml")

# プロジェクトID
project_id = config['project']['project_id']

# プロジェクトの設定
subprocess.run(["gcloud", "config", "set", "project", project_id])

# サービスアカウントの作成
subprocess.run([
    "gcloud", "iam", "service-accounts", "create", config['service_account']['name'],
    "--description", config['service_account']['description'],
    "--display-name", config['service_account']['display_name']
])

# Dockerリポジトリの作成
subprocess.run([
    "gcloud", "artifacts", "repositories", "create", config['repository']['name'],
    "--repository-format=Docker",
    "--location", config['repository']['location'],
    "--description", config['repository']['description']
])

# 権限の付与
roles = [
    "roles/serviceusage.serviceUsageConsumer",
    "roles/run.admin",
    "roles/iam.serviceAccountUser",
    "roles/artifactregistry.writer"
]

for role in roles:
    subprocess.run([
        "gcloud", "projects", "add-iam-policy-binding", project_id,
        "--member", f"serviceAccount:{config['service_account']['name']}@{project_id}.iam.gserviceaccount.com",
        "--role", role
    ])

# Workload Identity Poolの作成
subprocess.run([
    "gcloud", "iam", "workload-identity-pools", "create", config['workload_identity_pool']['name'],
    "--location=global",
    "--display-name", config['workload_identity_pool']['display_name']
])

# Workload Identity Providerの作成
subprocess.run([
    "gcloud", "iam", "workload-identity-pools", "providers", "create-oidc", config['provider']['name'],
    "--workload-identity-pool", config['workload_identity_pool']['name'],
    "--issuer-uri", config['provider']['issuer_uri'],
    "--attribute-mapping=google.subject=assertion.sub,attribute.repository=assertion.repository,attribute.repository_owner=assertion.repository_owner",
    "--location=global",
    f"--attribute-condition=assertion.repository_owner=='{config['provider']['repository_owner']}'"
])

# Workload Identity Userの権限付与
subprocess.run([
    "gcloud", "iam", "service-accounts", "add-iam-policy-binding",
    f"{config['service_account']['name']}@{project_id}.iam.gserviceaccount.com",
    "--role", "roles/iam.workloadIdentityUser",
    "--member", f"principalSet://iam.googleapis.com/projects/{project_id}/locations/global/workloadIdentityPools/{config['workload_identity_pool']['name']}/attribute.repository/{config['provider']['repository_owner']}/google_run"
])
