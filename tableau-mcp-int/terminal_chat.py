import os, sys, json, asyncio
from pathlib import Path
from dotenv import load_dotenv
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from langchain_mcp_adapters.tools import load_mcp_tools
from langchain_openai import ChatOpenAI
from langchain.agents import create_agent
from langchain_core.messages import HumanMessage
from langgraph.checkpoint.memory import InMemorySaver
from langfuse.langchain import CallbackHandler as LangfuseCallbackHandler

CONFIG_FILE = "config.stdio.json"
    
async def format_agent_response(agent, messages, langfuse_handler):
    """Stream response from agent and return the final text"""
    response_text = ""
    async for chunk in agent.astream(
        {"messages": messages},
        config={
            "configurable": {"thread_id": "main_session"},
            "callbacks": [langfuse_handler],
        },
        stream_mode="values",
    ):
        if "messages" in chunk and chunk["messages"]:
            latest_message = chunk["messages"][-1]
            if hasattr(latest_message, "content"):
                response_text = latest_message.content

    print()
    return response_text

async def main():
    here = Path(__file__).parent
    dotenv_path = here / ".env"
    if dotenv_path.exists():
        load_dotenv(dotenv_path=dotenv_path, override=False)
        print(f"Loaded .env from: {dotenv_path}")
    else:
        print("No .env file found - using shell env vars only")

    cfg_path = here / CONFIG_FILE
    if not cfg_path.exists():
        print(f"Config file not found: {cfg_path}", file=sys.stderr)
        sys.exit(1)

    with open(cfg_path, "r", encoding="utf-8") as f:
        cfg = json.load(f)

    if "mcpServers" not in cfg or "tableau" not in cfg["mcpServers"]:
        print("Invalid config: missing mcpServers.tableau", file=sys.stderr)
        sys.exit(1)

    tableau = cfg["mcpServers"]["tableau"]
    cmd = tableau.get("command")
    args = tableau.get("args", [])
    env = tableau.get("env", {})

    if not cmd or not args:
        print("Missing command/args in config", file=sys.stderr)
        sys.exit(1)
    if not os.path.exists(args[0]):
        print(f"MCP server entry not found: {args[0]}", file=sys.stderr)
        sys.exit(1)

    print("Loaded configuration from config.stdio.json")
    print(f" Command: {cmd} {' '.join(args)}")
    print(f" Transport: {env.get('TRANSPORT', 'stdio')}\n")

    server_params = StdioServerParameters(
        command=cmd,
        args=args,
        env=env
    )

    langfuse_handler = LangfuseCallbackHandler()

    print("Starting Tableau MCP via stdio ...")
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            mcp_tools = await load_mcp_tools(session)
            openai_key = os.getenv("OPENAI_API_KEY")
            if not openai_key:
                print("Set OPENAI_API_KEY in your .env", file=sys.stderr)
                sys.exit(1)

            llm = ChatOpenAI(model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"), temperature=0)
            checkpointer = InMemorySaver()
            agent = create_agent(model=llm, tools=mcp_tools, checkpointer=checkpointer)

            print("Tableau MCP connected - (Ctrl+C, exit, bye to exit)\n")
            while True:
                try:
                    user = input("user_prompt> ").strip()
                    if not user:
                        continue
                    if user.lower() in {"exit", "quit", "bye"}:
                        print("Bye!")
                        break

                    messages = [HumanMessage(content=user)]
                    response_text = await format_agent_response(agent, messages, langfuse_handler)

                    print("Agent>" + response_text)
                    print("\n")

                except (KeyboardInterrupt, EOFError):
                    print("\nBye!")
                    break
                except Exception as e:
                    print(f"\nError: {e}", file=sys.stderr)

if __name__ == "__main__":
    asyncio.run(main())
