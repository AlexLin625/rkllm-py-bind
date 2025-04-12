import sys
import rkllm
import asyncio


def test_rkllm(model_path):
    llm_config = rkllm.rkllm_create_default_params()
    llm_config.model_path = model_path
    llm_config.max_context_len = 1024
    llm_config.max_new_tokens = 512

    # 使用同步API时，必须继承这几个钩子.
    class LLM(rkllm.RKLLM):
        def onInferError(self):
            print("Infer error")

        def onInferToken(self, token):
            print(token, end="")

        def onInferFinished(self):
            print("-----\n\nInfer finished")

    llm = LLM(llm_config)
    llm.init()

    # 你可以使用str直接传入
    llm.infer("你是谁?")

    # 或者使用 `rkllm.RKLLMDataUtils` 转换
    converted_prompt = rkllm.RKLLMDataUtils.text_input("你来自哪里?")
    llm.infer(converted_prompt)


# 你也可以使用异步API
async def test_rkllm_async(model_path):
    llm_config = rkllm.rkllm_create_default_params()
    llm_config.model_path = model_path
    llm_config.max_context_len = 1024
    llm_config.max_new_tokens = 512

    asyncLLM = rkllm.RKLLMAsync(llm_config)
    asyncLLM.init()

    res_future = asyncLLM.inferAsync("你要到那里去?")
    res_future.add_done_callback(lambda res: print(res.result(), end=""))

    print("This method returns!")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python example.py <model_path>")
        sys.exit(1)

    model_path = sys.argv[1]
    test_rkllm(model_path)
    asyncio.run(test_rkllm_async(model_path))
