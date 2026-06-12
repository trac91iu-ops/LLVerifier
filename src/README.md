## Source Code

### Prerequisites
+ Python3.8+
+ maude v3.2.2+
+ set environment variable $EDITOR
+ `cp lib/preludePatched.maude /usr/share/maude/prelude.maude`
+ `cp configs/config.yaml.sample configs/config.yaml` , then edit configs/config.yaml
+ `bash scripts/bootstrap.sh`
+ `source venv/bin/activate`

### Usage

#### Generation
`python src/main.py <path_to_protocol_text>`

#### Checking:
`maude output/XXX/checker.maude`

