#!/usr/bin/python
# coding=utf-8
import sys
import click
import http.client
import hashlib
import urllib
import random
import json
from rich.console import Console
from rich.table import Column, Table
console=Console()
@click.command()
@click.argument('sentence')
# 原文语种默认自动识别
@click.option('-f', default='auto', help='Language you want to translate.')
# 译文语种默认英语（可自行修改）
@click.option('-t', default='en', help='Language you want to translate to.')
# 注释中的appid和密钥可以在百度翻译开放平台获取
def main(sentence, f, t):
    q = sentence
    appid = ''  # 填写你的appid
    secretKey = ''  # 填写你的密钥

    httpClient = None
    myurl = '/api/trans/vip/translate'

    fromLang = f  # 原文语种
    toLang = t  # 译文语种
    salt = random.randint(32768, 65536)
    sign = appid + q + str(salt) + secretKey
    sign = hashlib.md5(sign.encode()).hexdigest()
    myurl = myurl + '?appid=' + appid + '&q=' + urllib.parse.quote(q) + '&from=' + fromLang + '&to=' + toLang + '&salt=' + str(
        salt) + '&sign=' + sign

    try:
        httpClient = http.client.HTTPConnection('api.fanyi.baidu.com')
        httpClient.request('GET', myurl)

        # response是HTTPResponse对象
        response = httpClient.getresponse()
        result_all = response.read().decode("utf-8")
        result = json.loads(result_all)
        table = Table(show_header=True, header_style="bold red")
        table.add_column("From", style="dim", width=5)
        table.add_column("To",width=5)
        table.add_column("Source", justify="right",width=25)
        table.add_column("Destination", justify="right",width=25)
        table.add_row(
                    result['from'],result['to'],result['trans_result'][0]['src'],result['trans_result'][0]['dst']
                )
        console.print(table)
    except Exception as e:
        print(e)
    finally:
        if httpClient:
            httpClient.close()


if __name__ == '__main__':
    main()
