from __future__ import annotations

from typing import List, Optional
from pydantic import ValidationError


from swarms.agents.utils.Agent import AgentOutputParser
from swarms.agents.utils.human_input import HumanInputRun
from swarms.agents.prompts.prompt_generator import FINISH_NAME
from swarms.agents.models.base import AbstractModel
from swarms.agents.prompts.agent_output_parser import AgentOutputParser
from swarms.agents.prompts.agent_prompt_auto import PromptConstructor, MessageFormatter
from swarms.agents.prompts.agent_prompt import AIMessage, HumanMessage, SystemMessage


from langchain.chains.llm import LLMChain
from langchain.memory import ChatMessageHistory
from langchain.schema import (BaseChatMessageHistory, Document)

from langchain.tools.base import BaseTool
from langchain.vectorstores.base import VectorStoreRetriever

class Agent:
    """Base Agent class"""

    def __init__(
        self,
        ai_name: str,
        chain: LLMChain,
        memory: VectorStoreRetriever,
        output_parser: AgentOutputParser,
        tools: List[BaseTool],
        feedback_tool: Optional[HumanInputRun] = None,
        chat_history_memory: Optional[BaseChatMessageHistory] = None,
    ):
        self.ai_name = ai_name
        self.chain = chain
        self.memory = memory
        self.next_action_count = 0
        self.output_parser = output_parser
        self.tools = tools
        self.feedback_tool = feedback_tool
        self.chat_history_memory = chat_history_memory or ChatMessageHistory()

    @classmethod
    def from_llm_and_tools(
        cls,
        ai_name: str,
        ai_role: str,
        memory: VectorStoreRetriever,
        tools: List[BaseTool],
        llm: AbstractModel,
        human_in_the_loop: bool = False,
        output_parser: Optional[AgentOutputParser] = None,
        chat_history_memory: Optional[BaseChatMessageHistory] = None,
    ) -> Agent:
        prompt_constructor = PromptConstructor(ai_name=ai_name,
                                               ai_role=ai_role,
                                               tools=tools)
        message_formatter = MessageFormatter()
        human_feedback_tool = HumanInputRun() if human_in_the_loop else None
        chain = LLMChain(llm=llm, prompt_constructor=prompt_constructor, message_formatter=message_formatter)
        return cls(
            ai_name,
            memory,
            chain,
            output_parser or AgentOutputParser(),
            tools,
            feedback_tool=human_feedback_tool,
            chat_history_memory=chat_history_memory,
        )

    def run(self, goals: List[str]) -> str:
        user_input = (
            "Determine which next command to use, "
            "and respond using the format specified above:"
        )
        # Interaction Loop
        loop_count = 0
        while True:
            # Discontinue if continuous limit is reached
            loop_count += 1

            # Send message to AI, get response
            assistant_reply = self.chain.run(
                goals=goals,
                messages=self.chat_history_memory.messages,
                memory=self.memory,
                user_input=user_input,
            )

            # Print Assistant thoughts
            print(assistant_reply)
            self.chat_history_memory.add_message(HumanMessage(content=user_input))
            self.chat_history_memory.add_message(AIMessage(content=assistant_reply))

            # Get command name and arguments
            action = self.output_parser.parse(assistant_reply)
            tools = {t.name: t for t in self.tools}
            if action.name == FINISH_NAME:
                return action.args["response"]
            if action.name in tools:
                tool = tools[action.name]
                try:
                    observation = tool.run(action.args)
                except ValidationError as e:
                    observation = (
                        f"Validation Error in args: {str(e)}, args: {action.args}"
                    )
                except Exception as e:
                    observation = (
                        f"Error: {str(e)}, {type(e).__name__}, args: {action.args}"
                    )
                result = f"Command {tool.name} returned: {observation}"
            elif action.name == "ERROR":
                result = f"Error: {action.args}. "
            else:
                result = (
                    f"Unknown command '{action.name}'. "
                    f"Please refer to the 'COMMANDS' list for available "
                    f"commands and only respond in the specified JSON format."
                )

            memory_to_add = (
                f"Assistant Reply: {assistant_reply} " f"\nResult: {result} "
            )
            if self.feedback_tool is not None:
                feedback = f"\n{self.feedback_tool.run('Input: ')}"
                if feedback in {"q", "stop"}:
                    print("EXITING")
                    return "EXITING"
                memory_to_add += feedback

            self.memory.add_documents([Document(page_content=memory_to_add)])
            self.chat_history_memory.add_message(SystemMessage(content=result))
