# Before running tests

- Install python, I recommend to use [pyenv](https://github.com/pyenv/pyenv) for that

- Install required packages listed in `requirements.txt` files

      pip install -r part_1/requirements.txt -r part_2/requirements.txt

# Executing part 1

  By default, part 1 tests run with Chrome browser 

        pytest -vvl part_1

  It is possible to also run them with Firefox and Safari
  using options: `--firefox`, `--chrome`, `--safari`

        pytest -vvl part_1 --firefox
 
  To run a particular test you can use option `-k`
 
        pytest -vvl part_1 -k

  for more information see [pytest documentation](https://docs.pytest.org/en/7.1.x/how-to/usage.html#specifying-which-tests-to-run) on how to specify which tests to run

# Executing part 2

  Open `part_2/configuration.yaml` file and fill missing configuration values.

    user_info:
      id: '<user_id should be a string>'
      first_name: <first name>
      last_name: <last name>
      email: <email>
    client_id: <your app client id>
    client_secret: <your app client secret>

  Run the tests

    pytest -vvl part_2

