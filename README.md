**Actions:**
[![sam-validation](https://github.com/e1ifas/cloudinary-remote-files-sync-s3/actions/workflows/sam-validation.yaml/badge.svg)](https://github.com/e1ifas/cloudinary-remote-files-sync-s3/actions/workflows/sam-validation.yaml)
[![yamlfmt](https://github.com/e1ifas/cloudinary-remote-files-sync-s3/actions/workflows/yamlfmt.yaml/badge.svg)](https://github.com/e1ifas/cloudinary-remote-files-sync-s3/actions/workflows/yamlfmt.yaml)
[![YAPF](https://github.com/e1ifas/cloudinary-remote-files-sync-s3/actions/workflows/yapf.yaml/badge.svg)](https://github.com/e1ifas/cloudinary-remote-files-sync-s3/actions/workflows/yapf.yaml)

**Code Style:**
[![YAML](https://img.shields.io/badge/YAML-yamlfmt-1f425f.svg)](https://github.com/google/yamlfmt)
[![Python](https://img.shields.io/badge/Python-YAPF--Google-red.svg)](https://github.com/google/yapf)

# cloudinary-remote-files-sync-s3

# How to use

## Create CFn stack of Github Oidc IAM Role for GitHub Actions

- This role is required to run GitHub Actions `sam-validation.yaml`.
- Set value to `OIDCProviderArn` if you already have configured GithubOidc, otherwise CFn tries to create it and fail!

```bash
# Just an example. Edit for your own environment.
aws cloudformation create-stack \
  --stack-name github-oidc-iam-role-cloudinary-remote-files-sync-s3 \
  --template-body file://path/to/GitHubOIDC.yaml \
  --parameters ParameterKey=GitHubOrg,ParameterValue=e1ifas ParameterKey=RepositoryName,ParameterValue=cloudinary-remote-files-sync-s3 \
  --capabilities CAPABILITY_IAM
```

Then, you can get outputs of by the command below:

```bash
# Just an example. Edit for your own environment.
aws cloudformation describe-stacks \
  --stack-name github-oidc-iam-role-cloudinary-remote-files-sync-s3 \
  | jq -r '.Stacks[] | .Outputs[]'
```

## Register parameters to GitHub secrets

You need to register parameters below to GitHub secrets. 

- `AWS_REGION`
  - Set to your own region.
- `AWS_ROLE_TO_ASSUME`
  - Set a value output as `RoleArn` avobe.

