import os
import re
import json
import requests
import tiktoken

from .base import BaseLLM

class gemini(BaseLLM):
    def __init__(
        self,
        api_key: str,
        engine: str = os.environ.get("GPT_ENGINE") or "gemini-1.5-pro-latest",
        api_url: str = "https://generativelanguage.googleapis.com/v1beta/models/{model}:{stream}?key={api_key}",
        system_prompt: str = "You are Gemini, a large language model trained by Google. Respond conversationally",
        temperature: float = 0.5,
        top_p: float = 0.7,
        timeout: float = 20,
        convo_id: str = "default",
    ):
        super().__init__(api_key, engine, system_prompt=system_prompt, timeout=timeout, temperature=temperature, top_p=top_p)
        self.system_prompt[convo_id] = system_prompt
        self.api_url = api_url
        self.conversation: dict[str, list[dict]] = {
            "default": [],
        }

    def add_to_conversation(
        self,
        message: str,
        role: str,
        convo_id: str = "default",
        pass_history: int = 9999,
        total_tokens: int = 0,
    ) -> None:
        """
        Add a message to the conversation
        """

        if convo_id not in self.conversation or pass_history <= 2:
            self.reset(convo_id=convo_id)
        # print("message", message)
        if isinstance(message, str):
            message = [{"text": message}]
        self.conversation[convo_id].append({"role": role, "parts": message})

        history_len = len(self.conversation[convo_id])
        history = pass_history
        if pass_history < 2:
            history = 2
        while history_len > history:
            self.conversation[convo_id].pop(1)
            history_len = history_len - 1

        if total_tokens:
            self.tokens_usage[convo_id] += total_tokens

    def reset(self, convo_id: str = "default", system_prompt: str = "You are Gemini, a large language model trained by Google. Respond conversationally") -> None:
        """
        Reset the conversation
        """
        self.conversation[convo_id] = list()
        self.system_prompt[convo_id] = system_prompt or self.system_prompt[convo_id]

    def __truncate_conversation(self, convo_id: str = "default") -> None:
        """
        Truncate the conversation
        """
        while True:
            if (
                self.get_token_count(convo_id) > self.truncate_limit
                and len(self.conversation[convo_id]) > 1
            ):
                # Don't remove the first message
                self.conversation[convo_id].pop(1)
            else:
                break

    def get_token_count(self, convo_id: str = "default") -> int:
        """
        Get token count
        """
        encoding = tiktoken.get_encoding("cl100k_base")

        num_tokens = 0
        for message in self.conversation[convo_id]:
            # every message follows <im_start>{role/name}\n{content}<im_end>\n
            num_tokens += 5
            for key, value in message.items():
                if value:
                    num_tokens += len(encoding.encode(value))
                if key == "name":  # if there's a name, the role is omitted
                    num_tokens += 5  # role is always required and always 1 token
        num_tokens += 5  # every reply is primed with <im_start>assistant
        return num_tokens

    async def ask_stream(
        self,
        prompt: str,
        role: str = "user",
        convo_id: str = "default",
        model: str = None,
        pass_history: int = 9999,
        model_max_tokens: int = 4096,
        **kwargs,
    ):
        if convo_id not in self.conversation or pass_history <= 2:
            self.reset(convo_id=convo_id, system_prompt=self.system_prompt[convo_id])
        self.add_to_conversation(prompt, role, convo_id=convo_id, pass_history=pass_history)
        # self.__truncate_conversation(convo_id=convo_id)
        # print(self.conversation[convo_id])

        headers = {
            "Content-Type": "application/json",
        }

        json_post = {
            "contents": self.conversation[convo_id] if pass_history else [{
                "role": "user",
                "content": prompt
            }],
            "systemInstruction": {"parts": [{"text": self.system_prompt[convo_id]}]},
            "safetySettings": [
                {
                    "category": "HARM_CATEGORY_HARASSMENT",
                    "threshold": "BLOCK_NONE"
                },
                {
                    "category": "HARM_CATEGORY_HATE_SPEECH",
                    "threshold": "BLOCK_NONE"
                },
                {
                    "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
                    "threshold": "BLOCK_NONE"
                },
                {
                    "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
                    "threshold": "BLOCK_NONE"
                }
            ],
        }
        replaced_text = json.loads(re.sub(r'/9j/([A-Za-z0-9+/=]+)', '/9j/***', json.dumps(json_post)))
        print(json.dumps(replaced_text, indent=4, ensure_ascii=False))

        url = self.api_url.format(model=model or self.engine, stream="streamGenerateContent", api_key=self.api_key)

        try:
            response = self.session.post(
                url,
                headers=headers,
                json=json_post,
                timeout=kwargs.get("timeout", self.timeout),
                stream=True,
            )
        except ConnectionError:
            print("连接错误，请检查服务器状态或网络连接。")
            return
        except requests.exceptions.ReadTimeout:
            print("请求超时，请检查网络连接或增加超时时间。{e}")
            return
        except Exception as e:
            print(f"发生了未预料的错误: {e}")
            return

        if response.status_code != 200:
            print(response.text)
            raise BaseException(f"{response.status_code} {response.reason} {response.text}")
        response_role: str = "model"
        full_response: str = ""
        try:
            for line in response.iter_lines():
                if not line:
                    continue
                line = line.decode("utf-8")
                if line and '\"text\": \"' in line:
                    content = line.split('\"text\": \"')[1][:-1]
                    content = "\n".join(content.split("\\n"))
                    full_response += content
                    yield content
        except requests.exceptions.ChunkedEncodingError as e:
            print("Chunked Encoding Error occurred:", e)
        except Exception as e:
            print("An error occurred:", e)

        self.add_to_conversation([{"text": full_response}], response_role, convo_id=convo_id, pass_history=pass_history)