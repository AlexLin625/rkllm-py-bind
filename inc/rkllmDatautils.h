#ifndef RKLLM_DATAUTILS_H
#define RKLLM_DATAUTILS_H

#include "rkllm.h"
#include <cstring>
#include <string>

class RKLLMDataUtils
{
public:
  static RKLLMInput textInput(const std::string prompt)
  {
    const char *inputCString = new char[prompt.length() + 1];
    std::strcpy(const_cast<char *>(inputCString), prompt.c_str());

    return {
        .input_type = RKLLM_INPUT_PROMPT,
        .prompt_input = inputCString,
    };
  }

  static RKLLMInput tokenInput(const int32_t *input_ids, size_t n_tokens)
  {
    return {
        .input_type = RKLLM_INPUT_TOKEN,
        .token_input =
            {
                .input_ids = const_cast<int32_t *>(input_ids),
                .n_tokens = n_tokens,
            },
    };
  }

  static RKLLMInput embedInput(const float *embed, size_t n_tokens)
  {
    return {
        .input_type = RKLLM_INPUT_EMBED,
        .embed_input =
            {
                .embed = const_cast<float *>(embed),
                .n_tokens = n_tokens,
            },
    };
  }
};

#endif
