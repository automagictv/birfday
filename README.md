# birfday

Get reminders to send friends/family birthday texts.

## Setup

This uses `pipenv` to manage the virtual env and all dependencies. If you don't have pipenv install it [here](https://pypi.org/project/pipenv/) then:

```
git clone https://github.com/automagictv/birfday.git
cd birfday
pipenv install --ignore-pipfile
```

For this to work, we need Birthday data in our database. If this is the first time you're running this application, start by seeding the data. Instructions on how to do this are below.

### Adding Birthdays

You'll need a csv containing the following fields with a `,` delimiter:

```
first_name
last_name
month
day
note [OPTIONAL]
dt_updated [OPTIONAL]
```

For example:

```
first_name,last_name,month,day
Test,Birthday,5,15
Test,Birthday1,10,23
```

Once you have this file you can run the app in SEED mode:

```
pipenv run birfday/runner.py --mode SEED --file "/path/to/file.csv"
```

## Running the App

To execute in RUN mode:

```
pipenv run birfday/runner.py
```

You can run this on the cron by doing something like this:

```
# Run at 12:05 AM every day
5 0 * * * cd /path/to/birfday && pipenv run birfday/runner.py >> /path/to/cronlog.txt 2>&1
```

## Config

This uses the `config.py` file to set certain constants

## Testing

This package uses [pytest](https://docs.pytest.org/en/stable/). So to run the tests, execute the following:

```
pipenv run python -m pytest
```

Or to test an individual module, run:

```
pipenv run python -m pytest tests/[test_module].py
```
