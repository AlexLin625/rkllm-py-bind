#ifndef RKLLM_WRAPPER_BASE_H
#define RKLLM_WRAPPER_BASE_H

#include "rkllm.h"
#include <string>

class RKLLMWrapperBase
{
public:
  /*
    用户填入的回调函数
  */
  virtual void onInferError() = 0;
  virtual void onInferToken(const char *token) = 0;
  virtual void onInferFinished() = 0;

  RKLLMWrapperBase(const RKLLMParam &params)
  {
    this->params = params;
  };

  ~RKLLMWrapperBase()
  {
    if (this->handle != nullptr)
    {
      if (isPromptCacheEnable)
      {
        rkllm_release_prompt_cache(this->handle);
        this->isPromptCacheEnable = false;
      }

      rkllm_destroy(this->handle);
      this->handle = nullptr;
    }
  };

  bool init()
  {
    const int ret = rkllm_init(&this->handle, &this->params, RKLLMWrapperBase::staticInferCallback);
    this->inferParam = this->getDefaultInferParams();

    return ret == 0;
  };

  bool abort()
  {
    if (this->handle)
      return rkllm_abort(this->handle) == 0;
    return false;
  }

  bool infer(RKLLMInput input)
  {
    if (this->handle == nullptr)
      return false;

    if (this->isPromptCacheEnable)
    {
      updatePromptCacheParams();
      this->inferParam.prompt_cache_params = &this->promptCacheParams;
    }
    else
    {
      this->inferParam.prompt_cache_params = nullptr;
    }

    this->inferParam.keep_history = this->keepHistory;

    int ret = rkllm_run(this->handle, &input, &this->inferParam, static_cast<void *>(this));
    return ret == 0;
  }

private:
  void updatePromptCacheParams()
  {
    if (!this->isPromptCacheEnable)
      return;

    this->promptCacheParams = {
        .save_prompt_cache = static_cast<int>(!this->isPromptCacheExist),
        .prompt_cache_path = this->cachePath.c_str(),
    };
  }

public:
  bool enablePromptCache(const std::string &cachePath, const RKLLMPromptCacheParam &params)
  {
    if (this->handle == nullptr)
      return false;

    this->cachePath = cachePath;
    this->isPromptCacheEnable = true;
    this->isPromptCacheExist = false;

    return true;
  }

  bool disablePromptCache()
  {
    if (this->handle)
    {
      rkllm_release_prompt_cache(this->handle);
      this->isPromptCacheEnable = false;
      return true;
    }
    return false;
  }

  bool setPromptTemplate(const std::string &systemPrompt, const std::string &userPromptPrefix,
                         const std::string &userPromptSuffix)
  {
    if (this->handle == nullptr)
      return false;

    this->systemPrompt = systemPrompt;
    this->userPromptPrefix = userPromptPrefix;
    this->userPromptSuffix = userPromptSuffix;

    int ret = rkllm_set_chat_template(this->handle, this->systemPrompt.c_str(), this->userPromptPrefix.c_str(),
                                      this->userPromptSuffix.c_str());
    return ret == 0;
  }

  void setKeepChatHistory(bool val)
  {
    this->keepHistory = val;
  }

private:
  // 内部使用的句柄
  LLMHandle handle = nullptr;

  // 模型推理和采样参数
  RKLLMParam params;

  /* *** 封装类设置 *** */
  // 推理模式
  bool isAsync = false;
  bool keepHistory = false;
  RKLLMInferParam inferParam;

  // 提示词模板
  std::string systemPrompt;
  std::string userPromptPrefix;
  std::string userPromptSuffix;

  // 是否使用 Prmpt Cache
  bool isPromptCacheEnable = false;
  bool isPromptCacheExist = false;
  std::string cachePath;
  RKLLMPromptCacheParam promptCacheParams;

  RKLLMInferParam getDefaultInferParams()
  {
    return {
        .mode = RKLLM_INFER_GENERATE,
        .lora_params = NULL,
        .prompt_cache_params = NULL,
        .keep_history = this->keepHistory,
    };
  }

  void inferCallback(RKLLMResult *result, void *userData, LLMCallState state)
  {
    switch (state)
    {
    case RKLLM_RUN_WAITING:
      return;

    case RKLLM_RUN_ERROR:
      if (this->isPromptCacheEnable)
      {
        this->isPromptCacheExist = false;
      }
      onInferError();
      return;

    case RKLLM_RUN_NORMAL:
      onInferToken(result->text);
      return;
    case RKLLM_RUN_FINISH:
      if (this->isPromptCacheEnable)
      {
        this->isPromptCacheExist = true;
      }
      onInferFinished();
      return;
    }
  }

  static void staticInferCallback(RKLLMResult *result, void *userData, LLMCallState state)
  {
    RKLLMWrapperBase *wrapper = static_cast<RKLLMWrapperBase *>(userData);
    wrapper->inferCallback(result, userData, state);
  }
};

#endif