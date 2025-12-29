# DataDev Quest Challenge 2025_11

![image](https://github.com/le-luu/DataDevQuest_2025_03/blob/main/img/logo.svg)

### Challenged By: 
 Cristian Saavedra Desmoineaux

### Objective
- Familiarize with the Tableau MCP
- Set up the Claude Desktop
- Build a terminal chat in Python
- Ask AI to get the insights from Tableau Cloud

### Solution Video
[![DDQ_2025_11](https://img.youtube.com/vi/fAPS79ITRjA/0.jpg)](https://www.youtube.com/watch?v=fAPS79ITRjA)

### Beginner Challenge
Link to the Beginner Challenge: https://datadevquest.com/ddq2025-11-tableau-mcp-with-claude-desktop-beginner/

**Challenge:**
- Explore prompts that use different tools listed in the Tableau MCP docs
- Identify which tools were used from the prompts

**Output**

![image](https://github.com/le-luu/DataDevQuest_2025_11/blob/main/img/ddq_2025_11_beginner_config_claude.png)

In Claude Desktop, go to Settings > Developers to configure the MCP Servers with the information above. Need to edit the directory to your index.js in the build folder, your server, site name, PAT name, PAT secret value. 

![image](https://github.com/le-luu/DataDevQuest_2025_11/blob/main/img/ddq_2025_11_beginner_output.png)

After restarting Claude Desktop, type the prompts to get the insights from Tableau Cloud with the specified site you set.

### Intermediate Challenge
Link to the Intermediate Challenge: https://datadevquest.com/ddq2025-11-tableau-mcp-terminal-chat-with-python-and-chatgpt-intermediate/

**Challenge:**
- Explore prompts that use different tools listed in the Tableau MCP docs
- Identify which tools were used from the prompts

**Output**

![image](https://github.com/le-luu/DataDevQuest_2025_11/blob/main/img/ddq_2025_11_intermediate_langfuse_openai.png)

Same as the Beginner challenge, in the Intermediate challenge, we also need to configure the mcpServers information for the directory to index.js, your server, site name, PAT name, PAT secret values. Also, need to add the API keys from Langfuse, OpenAI API.

![image](https://github.com/le-luu/DataDevQuest_2025_11/blob/main/img/ddq_2025_11_intermediate_output.png)

In the Terminal, after running the Python script, type the prompt to get the insights from Tableau Cloud with the specified site name.

### Instructions

- Follow the steps from the DataDevQuest page, watch the video solution for step-by-step.

**Beginner Challenge**

- Install Node.js version 22.7.5 or later
- Clone the tableau mcp page from github: https://github.com/tableau/tableau-mcp
- Install Claude Desktop
- Edit the mcpServer info in the config.stdio.json file
- Connect to Tableau MCP with configuration in Claude's setting
- Type Prompts in the chat box
  
**Intermediate Challenge**

- Need to install Python 3.12 or later
- Install Node.js version 22.7.5 or later
- Clone the tableau mcp page from github: https://github.com/tableau/tableau-mcp
- Create a folder inside the tableau-mcp folder called tableau-mcp-int
- Create .env file with all keys from Langfuse and OpenAI API inside the tableau-mcp-int folder
- Copy and paste the Python script file terminal_chat.py into the tableau-mcp-int folder
- Install virtual environment
```
python -m venv .venv
```
- Activate the virtual environment
```
.venv\Scripts\activate
```
- Upgrade pip and install packages
```
pip install mcp langchain langgraph langchain-openai langchain-mcp-adapters langfuse python-dotenv
```
- Run the Python script
```
python terminal_chat.py
```
- Then, type the prompts to get insights
