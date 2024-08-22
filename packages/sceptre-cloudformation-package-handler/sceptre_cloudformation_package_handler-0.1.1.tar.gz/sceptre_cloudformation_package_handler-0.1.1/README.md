# Sceptre CloudFormation package handler

Provides support for packaging template file with cloudformation package command.
This handler internally uses the `file` handler to load template files.

## Usage
In your config file, specify the template as follows:

```yaml
template:
  type: cloudformation_package
  path: my-template.yaml
  artifact_bucket_name: my-artifacts-bucket
  artifact_bucket_prefix: my-artifacts-prefix
```

## Options

The following options are supported:

| Option | Description                    |
|--------|--------------------------------|
| path | Path to the template file.     |
| artifact_bucket_name | Bucket to upload artifacts to. |
| artifact_bucket_prefix | *Optional* Prefix to upload artifacts to. |
