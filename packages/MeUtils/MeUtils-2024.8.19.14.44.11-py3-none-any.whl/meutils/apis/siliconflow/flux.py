#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : flux
# @Time         : 2024/8/5 09:52
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  : 


from meutils.pipe import *
from meutils.config_utils.lark_utils import get_spreadsheet_values, get_next_token_for_polling
from meutils.schemas.openai_types import ImageRequest, ImagesResponse
from meutils.apis.translator import deeplx
from meutils.schemas.translator_types import DeeplxRequest
from meutils.decorators.retry import retrying
from meutils.notice.feishu import send_message as _send_message

BASE_URL = "https://fluxpro.art"
FEISHU_URL = "https://xchatllm.feishu.cn/sheets/Bmjtst2f6hfMqFttbhLcdfRJnNf?sheet=tAFUNF"

# https://cloud.siliconflow.cn/api/redirect/model?modelName=black-forest-labs/FLUX.1-schnell&modelSubType=text-to-image


send_message = partial(
    _send_message,
    title=__name__,
    url="https://open.feishu.cn/open-apis/bot/v2/hook/dc1eda96-348e-4cb5-9c7c-2d87d584ca18"
)

ASPECT_RATIOS = {
    "1:1": "1024x1024",

    '2:3': "",
    '3:2': "",

    "4:3": "1280x960",
    "3:4": "960x1280",

    "5:4": "1280x960",
    "4:5": "960x1280",

    "16:9": "1366x768",
    "9:16": "768x1366",

    "21:9": "1344x576",
}


@retrying(max_retries=3, title=__name__, predicate=lambda x: x is True)
async def create_image(request: ImageRequest):
    token = await get_next_token_for_polling(feishu_url=FEISHU_URL)

    prompt = (await deeplx.translate(DeeplxRequest(text=request.prompt, target_lang="EN"))).get("data")

    payload = {
        "prompt": prompt,
        "negative_prompt": request.negative_prompt,
        "aspect_ratio": request.size if request.size in ASPECT_RATIOS else "1:1",

        "guidance": request.guidance_scale,
        "steps": request.num_inference_steps,
        "nsfw_level": request.nsfw_level  # 0 1 2 3
    }

    headers = {
        'Cookie': token,
    }
    async with httpx.AsyncClient(base_url=BASE_URL, headers=headers, timeout=100) as client:
        response = await client.post("/api/prompts/flux", json=payload)

        logger.debug(response.status_code)

        if response.status_code in {429, 403}:  # 触发重试
            logger.debug(f"{response.status_code} {token}")
            send_message(f"{response.status_code} {token}")
            return True

        if response.is_success:
            data = response.json().get('assets', [])
            data = [{"url": f"{BASE_URL}{i.get('src')}", "revised_prompt": prompt} for i in data]
            return ImagesResponse.construct(data=data)

        response.raise_for_status()


# {
#     "id": "clzianobv017nq200g3fd2zb1",
#     "prompt": "borttiful scenery nature glass bottle landscape, , purple galaxy seed",
#     "negative_prompt": "",
#     "aspect_ratio": "1:1",
#     "assets": [
#         {
#             "src": "/api/view/clzianobv017nq200g3fd2zb1/0.webp"
#         }
#     ],
#     "model": "FLUX.1 [pro]",
#     "created_at": "2024-08-06T10:45:19.723Z",
#     "is_nsfw": true
# }


if __name__ == '__main__':
    arun(create_image(ImageRequest(prompt="画条狗")))
