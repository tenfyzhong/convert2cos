# convert2cos
convert video and then push to tencent cos. 

# install
```sh
pip install -r requirements.txt
```

# Usage
```
Usage: convert2cos.py [OPTIONS]

Options:
  -c TEXT         configuration
  -i TEXT         input file
  -o TEXT         remote output file
  --stdout TEXT   default stdout
  --stderr TEXT   default stderr
  --rm / --no-rm  remove output file
  --help          Show this message and exit.
```
It will convert the input file to `basename output` and the upload the file to
cos. 

# configuration
example: 
```yaml
cos:
  appid: # cos appid
  secret_id: # cos secret_id
  secret_key: # cos secret_key
  region: # cos region, sh 表示华东园区, gz 表示华南园区, tj 表示华北园区
  bucket: # bucket name

# input or output options
ffmpeg:
  output:
    options:
      - '-vcodec'
      - 'libx264'
      - '-preset'
      - 'fast'
      - '-crf'
      - '32'
      - '-r'
      - '18'
      - '-y'
      - '-acodec'
      - 'libmp3lame'
```

