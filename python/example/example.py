import sys
import rkllm

def test_rkllm(model_path):
    llm_config = rkllm.rkllm_create_default_params()
    llm_config.model_path = model_path
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
    if len(sys.argv) != 2:
        print("Usage: python example.py <model_path>")
        sys.exit(1)

    model_path = sys.argv[1]
    test_rkllm(model_path)