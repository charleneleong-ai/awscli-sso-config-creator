# awscli-sso-config-creator
Adapted from [this script](https://github.com/stormlrd/aws-sso-cli-config-creator/blob/master/create_config.py).

This script will **scrape** your roles from AWS SSO and create a AWS CLI v2 config file for you.

## Requirements 
- [Python 3.7.5](https://docs.python-guide.org/starting/install3/osx/) or above
- [AWS CLI v2](https://docs.aws.amazon.com/cli/latest/userguide/install-cliv2.html)


### Create virtualenv
```bash
$ python -m venv .venv
$ source .venv/bin/activate
```

### Install dependencies

```bash
$ pip install -r requirements.txt
```

For further development - 
```bash
$ pip install -r requirements-dev.txt
```


## Usage:
1. Clone this repository
2. Copy and paste the AWS SSO primary profile credentials from the `sample_sso_config` profile to your `~/.aws/config` file
3. Login to AWS SSO `aws sso login --profile primary`
4. Execute the script `python create_sso_config.py`
5. Transfer contents of newly generated `sso_config` into your `~/.aws/config` file


## Dependencies

The script relies on a couple of things:

1. That you have `aws cli v2` installed, `python3` installed and `boto3` library installed for python.
2. That you have configured your primary SSO profile `[profile primary]` in `~/.aws/config` file
3. That you have already logged into AWS SSO using `aws sso login --profile primary`.



## Further reading

Boto3 SDK for SSO: https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sso.html

AWS CLI v2 SSO configuration: https://docs.amazonaws.cn/en_us/cli/latest/userguide/cli-configure-sso.html

AWS CLI V2 announcement post: https://aws.amazon.com/blogs/developer/aws-cli-v2-is-now-generally-available/