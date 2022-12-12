# URL Shortner

Fast and simple URL shortner written in Python. See [ADR](adr/) folder for design decisions.

## TODO

- [x] Dockerize
- [ ] Tests
- [x] litestream.io for backups


# S3 bucket
You need to have AWS `AccessKeyId` and `SecretAccessKey` that have read and write access 
to an S3 bucket. The SQLite database will be backed up to this bucket constantly, and
restored from the bucket on startup.
The easiest way to create both the bucket and the user is to use [s3-credentials](https://github.com/simonw/s3-credentials).
```bash
% pip install s3-credentials
% s3-credentials create shortme-bucket-for-database --create-bucket
```
The assumption that you have AWS credentials set up on your machine.