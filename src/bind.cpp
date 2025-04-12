#include "rkllm.h"
#include "rkllmDatautils.h"
#include "rkllmWrapperBase.h"

#include <pybind11/functional.h>
#include <pybind11/pybind11.h>
#include <pybind11/pytypes.h>
#include <pybind11/stl.h>
#include <vector>

namespace py = pybind11;

// Python包装类，继承自RKLLMWrapperBase以实现回调函数
class PyRKLLMWrapper : public RKLLMWrapperBase
{
public:
  // 使用pybind11的trampoline类来处理虚函数
  using RKLLMWrapperBase::RKLLMWrapperBase; // 继承构造函数

  // 实现纯虚函数，通过Python回调函数进行调用
  void onInferError() override
  {
    PYBIND11_OVERLOAD_PURE(void,             // 返回类型
                           RKLLMWrapperBase, // 父类
                           onInferError,     // 函数名
                                             // 没有参数
    );
  }

  void onInferToken(const char *token) override
  {
    PYBIND11_OVERLOAD_PURE(void,             // 返回类型
                           RKLLMWrapperBase, // 父类
                           onInferToken,     // 函数名
                           token             // 参数
    );
  }

  void onInferFinished() override
  {
    PYBIND11_OVERLOAD_PURE(void,             // 返回类型
                           RKLLMWrapperBase, // 父类
                           onInferFinished,  // 函数名
                                             // 没有参数
    );
  }
};

PYBIND11_MODULE(rkllm, m)
{
  m.doc() = "RKLLM Python bindings"; // 模块文档

  py::class_<RKLLMParam>(m, "RKLLMParam")
      .def(py::init<>()) // Add constructor
      .def_property(
          "model_path", [](const RKLLMParam &self) { return std::string(self.model_path); },
          [](RKLLMParam &self, const std::string &value) {
            if (self.model_path != nullptr)
            {
              free((void *)self.model_path);
              self.model_path = nullptr;
            }

            self.model_path = new char[value.size() + 1];
            std::strcpy((char *)self.model_path, value.c_str());
          })
      .def_readwrite("max_context_len", &RKLLMParam::max_context_len)
      .def_readwrite("max_new_tokens", &RKLLMParam::max_new_tokens)
      .def_readwrite("top_k", &RKLLMParam::top_k)
      .def_readwrite("n_keep", &RKLLMParam::n_keep)
      .def_readwrite("top_p", &RKLLMParam::top_p)
      .def_readwrite("temperature", &RKLLMParam::temperature)
      .def_readwrite("repeat_penalty", &RKLLMParam::repeat_penalty)
      .def_readwrite("frequency_penalty", &RKLLMParam::frequency_penalty)
      .def_readwrite("presence_penalty", &RKLLMParam::presence_penalty)
      .def_readwrite("mirostat", &RKLLMParam::mirostat)
      .def_readwrite("mirostat_tau", &RKLLMParam::mirostat_tau)
      .def_readwrite("mirostat_eta", &RKLLMParam::mirostat_eta)
      .def_readwrite("skip_special_token", &RKLLMParam::skip_special_token)
      .def_readwrite("is_async", &RKLLMParam::is_async);

  // 初始化helper
  m.def("rkllm_create_default_params", rkllm_createDefaultParam);

  // 定义RKLLMWrapperBase类及其Python继承类
  py::class_<RKLLMWrapperBase, PyRKLLMWrapper>(m, "RKLLMWrapperBase")
      .def(py::init<const RKLLMParam &>())
      .def("init", &RKLLMWrapperBase::init)
      .def("abort", &RKLLMWrapperBase::abort)
      .def("infer", &RKLLMWrapperBase::infer)
      .def("enablePromptCache", &RKLLMWrapperBase::enablePromptCache)
      .def("disablePromptCache", &RKLLMWrapperBase::disablePromptCache)
      .def("setPromptTemplate", &RKLLMWrapperBase::setPromptTemplate)
      .def("onInferError", &RKLLMWrapperBase::onInferError)
      .def("onInferToken", &RKLLMWrapperBase::onInferToken)
      .def("onInferFinished", &RKLLMWrapperBase::onInferFinished);

  // 定义RKLLMDataUtils类
  py::class_<RKLLMDataUtils>(m, "RKLLMDataUtils")
      .def_static("text_input", RKLLMDataUtils::textInput)
      .def_static("token_input",
                  [](const std::vector<int32_t> &input_ids) {
                    return RKLLMDataUtils::tokenInput(input_ids.data(), input_ids.size());
                  })
      .def_static("embed_input", [](const std::vector<float> &embed) {
        return RKLLMDataUtils::embedInput(embed.data(), embed.size());
      });

  py::class_<RKLLMInput>(m, "RKLLMInput");
}
