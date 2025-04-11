import sys

sys.path.append("./build")
import rkllm

def test_rkllm():
    model = "/home/pi/rkllm/llm-model-zoo/DeepSeek-R1-Distill-Qwen-7B_W8A8_RK3588.rkllm"

    llm_config = rkllm.rkllm_create_default_params()
    llm_config.model_path = model
    llm_config.max_context_len = 1024
    llm_config.max_new_tokens = 512

    class LLM(rkllm.RKLLMWrapperBase):
        def __init__(self, config):
            super().__init__(config)

        def onInferError(self):
            print("Infer error")

        def onInferToken(self, token):
            print(token, end="")
        
        def onInferFinished(self):
            print("-----\n\nInfer finished")

    llm = LLM(llm_config)
    llm.init()

    llm.infer(rkllm.RKLLMDataUtils.text_input("你是谁?"))


if __name__ == "__main__":
    test_rkllm()