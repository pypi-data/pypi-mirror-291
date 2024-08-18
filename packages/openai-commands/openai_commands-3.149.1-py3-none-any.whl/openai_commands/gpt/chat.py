"""
This Python script enables real-time conversation with OpenAI's ChatGPT model through the terminal.
Generated by ChatGPT, this script establishes a session where the user can interactively ask questions
or have a dialogue with the ChatGPT model. The user's input is sent to the ChatGPT API, and the model's
responses are displayed in the terminal, facilitating a conversational interface. Ensure you have the `openai`
Python package installed and an OpenAI API key set before running this script.

committed in its original form and then modified by Arash Abadpour - arash.abadpour@gmail.com.
"""

import os
from typing import List, Any, Tuple
from blueness import module
from openai import OpenAI
from abcli import file, path
from openai_commands import NAME, VERSION
from openai_commands import env
from openai_commands.logger import logger

NAME = module.name(__file__, NAME)

FULL_NAME = f"{NAME}-{VERSION}"

client = OpenAI(api_key=env.OPENAI_API_KEY)


def chat_with_openai(
    output_path: str = "",
    script_mode: bool = False,
    script: List[str] = [],
    model_name: str = env.OPENAI_GPT_DEFAULT_MODEL,
) -> Tuple[bool, List[Any]]:
    logger.info(
        "{} @ {}{}".format(
            FULL_NAME,
            model_name,
            f": 📜 {len(script)} line(s)." if script_mode else "",
        )
    )
    logger.info("ChatGPT: Hello! How can I assist you today?")

    conversation: List[Any] = []
    index = -1
    while True:
        index += 1

        if script_mode:
            if index >= len(script):
                logger.info("end of script.")
                break

            logger.info(
                "script: line #{}/{}: {}".format(
                    index + 1,
                    len(script),
                    script[index],
                )
            )

        user_input = script[index] if script_mode else input("(?:help) > ")

        if user_input in ["?", "help"]:
            logger.info("exit: exit.")
            logger.info("version: show version.")
            continue
        if user_input == "version":
            logger.info(FULL_NAME)
            continue
        if user_input == "exit":
            break

        response = client.chat.completions.create(
            model=model_name,
            messages=[{"role": "user", "content": user_input}],
            max_tokens=150,
        )

        answer = response.choices[0].message.content.strip()
        logger.info(f"ChatGPT: {answer}")

        conversation.append(
            {
                "user_input": user_input,
                "answer": answer,
            }
        )

    return (
        not (output_path)
        or file.save_yaml(
            os.path.join(
                output_path,
                f"{path.name(output_path)}.yaml",
            ),
            {
                "conversation": conversation,
                "created-by": FULL_NAME,
                "script_mode": script_mode,
            },
        ),
        conversation,
    )


def interact_with_openai(
    prompt: str,
    output_path: str = "",
    model_name: str = env.OPENAI_GPT_DEFAULT_MODEL,
) -> Tuple[bool, List[str]]:
    success, conversation = chat_with_openai(
        output_path=output_path,
        script_mode=True,
        script=[prompt],
        model_name=model_name,
    )

    if not conversation:
        return False, ""

    return success, conversation[0].get("answer", "").split("\n")


def list_models(log: bool = False) -> List[Any]:
    list_of_models = client.models.list().data

    if log:
        logger.info(f"{len(list_of_models)} model(s)")
        for index, model in enumerate(list_of_models):
            logger.info(f" #{index}: {model}")

    return list_of_models
