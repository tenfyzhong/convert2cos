#!/usr/bin/env python
# -*- coding: utf-8 -*-
import click
import yaml
import ffmpy
import qcloud_cos
import os


@click.command()
@click.option('-c', default='./config.yml', help='configuration')
@click.option('-i', prompt=True, help='input file')
@click.option('-o', prompt=True, help='remote output file')
@click.option('--stdout', help='default stdout')
@click.option('--stderr', help='default stderr')
@click.option('--rm/--no-rm', default=False, help='remove output file')
def convert2cos(c, i, o, stdout, stderr, rm):
    local_output = os.path.split(o)[-1]
    config = parse_config(c)
    convert(config, i, local_output, stdout, stderr)
    ret = upload(o, local_output, config)
    if ret[u'code'] != 0:
        click.echo('upload failed', err=True)
    else:
        url = ret['data'][u'url']
        https_url = url[:4] + 's' + url[4:]
        source_url = ret[u'data'][u'source_url']
        https_source_url = source_url[:4] + 's' + source_url[4:]
        click.echo('http_url = ' + url)
        click.echo('https_url = ' + https_url)
        click.echo('source_url = ' + source_url)
        click.echo('https_source_url = ' + https_source_url)

    if rm:
        os.remove(local_output)


def parse_config(c):
    with open(c) as f:
        config = yaml.load(f)
    return config


def convert(config, i, local_output, stdout, stderr):
    out = None if not stdout else stdout
    err = None if not stderr else stderr
    input_options = None
    output_options = None
    try:
        input_options = config["ffmpeg"]["input"]["options"]
    except Exception:
        input_options = None
    try:
        output_options = config["ffmpeg"]["output"]["options"]
    except Exception:
        output_options = None
    ff = ffmpy.FFmpeg(
        inputs={i: input_options},
        outputs={local_output: output_options})
    ff.run(input_data=None, stdout=out, stderr=err)


def upload(o, local_output, config):
    remote_file = unicode(o) if o.startswith('/') else u'/' + unicode(o)
    cos = qcloud_cos.CosClient(
        config["cos"]["appid"],
        unicode(config["cos"]["secret_id"]),
        unicode(config["cos"]["secret_key"]),
        region=config["cos"]["region"])
    upload = qcloud_cos.UploadFileRequest(
        unicode(config["cos"]["bucket"]),
        remote_file,
        local_output)
    ret = cos.upload_file(upload)
    return ret


if __name__ == '__main__':
    convert2cos()
