#include "rkllm.h"
#include "rkllmWrapperBase.h"

#include <iostream>

class TestWrapper : public RKLLMWrapperBase
{
public:
  TestWrapper(RKLLMParam params) : RKLLMWrapperBase(params)
  {
  }

  void onInferToken(const char *token) override
  {
    std::cout << "Token: " << token << std::endl;
  }

  void onInferError() override
  {
    std::cout << "Error during inference" << std::endl;
  }

  void onInferFinished() override
  {
    std::cout << "Inference finished" << std::endl;
  }
};

int main(int argc, char *argv[])
{
  auto config = rkllm_createDefaultParam();
  config.model_path = "/home/pi/rkllm/llm-model-zoo/DeepSeek-R1-Distill-Qwen-7B_W8A8_RK3588.rkllm";
  config.max_new_tokens = 256;
  config.max_context_len = 1024;

  auto llm = TestWrapper(config);
  llm.init();

  return 0;
}