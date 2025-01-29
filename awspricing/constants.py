from typing import Dict  # noqa


class Enum(object):
    """Very simple string enumeration implementation.

    Basic usage: `Colors = Enum('red', 'blue', 'green')  # Colors.RED == 'red'`

    You may also use kwargs to override accessor names.
    ```
    Years = Enum(one_year='1yr')  # Years.ONE_YEAR == '1yr'
    ```
    """
    def __init__(self, *args, **kwargs):  # type: (*str, **str) -> None
        self._values = {}  # type: Dict[str, str]
        for arg in args:
            self._values[arg.upper()] = arg
        for kwarg in kwargs:
            value = kwargs[kwarg]
            self._values[kwarg.upper()] = value

    def __getattr__(self, attr):
        if attr not in self._values:
            raise AttributeError("Enum value '{}' doesn't exist.".format(attr))
        return self._values[attr]

    def values(self):
        return self._values.values()


# noqa - Taken from: http://docs.aws.amazon.com/AWSEC2/latest/UserGuide/using-regions-availability-zones.html
REGION_SHORTS = {
    'af-south-1': 'Africa (Cape Town)',
    'ap-east-1': 'Asia Pacific (Hong Kong)',
    'ap-northeast-1': 'Asia Pacific (Tokyo)',
    'ap-northeast-2': 'Asia Pacific (Seoul)',
    'ap-northeast-3': 'Asia Pacific (Osaka-Local)',
    'ap-south-1': 'Asia Pacific (Mumbai)',
    'ap-south-2': 'Asia Pacific (Hyderabad)',
    'ap-southeast-1': 'Asia Pacific (Singapore)',
    'ap-southeast-2': 'Asia Pacific (Sydney)',
    'ap-southeast-3': 'Asia Pacific (Jakarta)',
    'ap-southeast-4': 'Asia Pacific (Melbourne)',
    'ap-southeast-5': 'Asia Pacific (Malaysia)',
    'ap-southeast-7': 'Asia Pacific (Thailand)',
    'ca-central-1': 'Canada (Central)',
    'cn-north-1': 'China (Beijing)',
    'cn-northwest-1': 'China (Ningxia)',
    'eu-central-1': 'EU (Frankfurt)',
    'eu-central-2': 'Europe (Zurich)',
    'eu-north-1': 'EU (Stockholm)',
    'eu-south-1': 'Europe (Milan)',
    'eu-south-2': 'Europe (Spain)',
    'eu-west-1': 'EU (Ireland)',
    'eu-west-2': 'EU (London)',
    'eu-west-3': 'EU (Paris)',
    'il-central-1': 'Israel (Tel Aviv)',
    'me-south-1': 'Middle East (Bahrain)',
    'me-central-1': 'Middle East (UAE)',
    'mx-central-1': 'Mexico (Central)',
    'sa-east-1': 'South America (Sao Paulo)',  # intentionally no unicode,
    'us-east-1': 'US East (N. Virginia)',
    'us-east-2': 'US East (Ohio)',
    'us-gov-east-1': 'AWS GovCloud (US-East)'
    'us-gov-west-1': 'AWS GovCloud (US)',
    'us-west-1': 'US West (N. California)',
    'us-west-2': 'US West (Oregon)',
}


EC2_LEASE_CONTRACT_LENGTH = Enum(one_year='1yr', three_year='3yr')
EC2_OFFERING_CLASS = Enum('standard', 'convertible')
EC2_PURCHASE_OPTION = Enum(
    no_upfront='No Upfront',
    partial_upfront='Partial Upfront',
    all_upfront='All Upfront'
)

RDS_LEASE_CONTRACT_LENGTH = Enum(one_year='1yr', three_year='3yr')
RDS_OFFERING_CLASS = Enum('standard')
RDS_PURCHASE_OPTION = Enum(
    no_upfront='No Upfront',
    partial_upfront='Partial Upfront',
    all_upfront='All Upfront'
)
