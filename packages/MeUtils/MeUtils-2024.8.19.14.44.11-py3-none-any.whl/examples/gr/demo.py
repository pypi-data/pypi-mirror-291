#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : demo
# @Time         : 2024/8/7 09:06
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  : 

from meutils.pipe import *
import gradio as gr

from gradio_client import Client, file

client = Client("http://120.92.209.146:8887")
print(client.view_api(all_endpoints=True))


# client.predict(parameter_13, chat_with_minicpmv_26, decode_type, api_name="/respond")