---
lab:
  title: Develop your first AI agent with Claude
  description: Use the Claude Platform, the Claude SDK, and Claude Code in Visual Studio Code to create an agent.
  level: 200
  duration: 40 minutes
  islab: false
---

# Develop your first AI agent with Claude

This exercise should take approximately **40** minutes to complete.

> **Note**: Claude Platform, Claude Code, and the Claude models are subject to continual development. This reflects the fast-moving nature of artificial intelligence technology. Some elements of your user experience may differ from the descriptions in this exercise!

In this exercise, you'll build an agent that acts as an expert in the history of computing. You'll start by prototyping the agent's instructions and tools in the Claude Platform, then implement the agent in Python code with the Claude SDK, and finally use Claude Code to add a new feature to the app.

## Prototype an agent in the Claude Console

The Claude Console (part of the Claude Platform) is a web portal in which you can manage API access and experiment with Claude models and prompts.

> **Note**: Using the Claude API requires an Anthropic Console account with API credits. Usage in this exercise is light, but if your account has no credits, you'll be prompted to add some before you can submit prompts.

1. In a web browser, open the [Claude Console](https://platform.claude.com){:target="_blank"} at `https://platform.claude.com`, and sign in (or create an account). If prompted, create an organization and complete any setup steps - including adding credits to your account.

1. In the navigation menu, open the **playground** (also known as the *Prompt Console*) and ensure the **Form** tabe is selected.

    > **Tip**: If you can't find the playground, look in the navigation menu under **Build**.

### Chat with the model

At the heart of every AI agent, there's a large language model (LLM). In the playground you can chat with a Claude model to explore how it responds.

1. In the playground, select the model **Claude Haiku 5.5** (`claude-haiku-5-5`) in the model settings.
1. In the **User** message box, enter a prompt such as `Who was Ada Lovelace?`, and run it. Review the response.
1. Add a follow-up prompt, such as `Tell me more about her work with Charles Babbage.` and review the response.

    The Messages API is *stateless*, so chat applications send the whole conversation history with each request. That's how the context of the conversation is retained - in this case, "her" is interpreted as referring to Ada Lovelace.

1. Start a new conversation and enter a prompt such as `Tell me about the ELIZA chatbot.`; then continue with `How does ELIZA compare with modern LLMs?`.

### Specify instructions in a *system prompt*

To support specific use cases, you should use a *system prompt* to provide the model with instructions that guide its responses. You can use the system prompt to give the model a specific focus or role, and provide guidelines about format, style, and constraints about what the model should and should not include in its responses.

1. Start a new conversation (clearing the message history).
1. In the **System prompt** box, enter the following instructions:

    ```
    You are an expert in the history of computing and AI. You only answer questions about significant people and events in the development of computing, and about notable vintage computers. Do not engage in conversations on any topic that is unrelated to computing history.
    ```

1. Enter a user prompt related to computing history, such as `What was Alan Turing's contribution to the development of AI?`, and review the response.
1. Try asking an "off-topic" question, such as `What's the capital of Spain?`, and view the response.

### Add a web search tool

A model generally answers questions based on the data with which it was trained. While this is useful, that leaves out a lot of current information on the web, which might help the model give more relevant answers. You can use *tools* to give models access to external data sources and enable them to perform tasks. The *web search* tool enables Claude to search the web for up-to-date information. It's a *server-side* tool, which means that Anthropic runs the searches for you - you don't need to write any code to perform them.

1. In the playground, add the **Web search** tool.

    > **Note**: Web search must be enabled for your organization. If you're unable to use it, an organization admin can enable it in the Claude Console settings.

1. Enter the prompt `Find a vintage computer store near Seattle` (*or your local city!*) and review the response.

    The model should have searched the web for vintage computer stores near the specific city, and included references to the sources it used.

### View the code for your agent

You've now defined the main elements of your agent: a *model*, *instructions*, and a *tool*. Next you'll implement them in code.

1. In the playground, switch to the **Code** tab to view the Python code that's equivalent to your configuration. Note how it includes the model, the system prompt, and the web search tool definition. You'll write something very similar in the next section.

    > **Tip**: playground settings aren't an agent that gets deployed anywhere. They're a prototype - you're responsible for the code that runs the agent, using the Messages API.

### Create an API key

To call Claude from code, you need an API key.

1. In the Claude Console, in the navigation menu, open **API keys** (under **Settings**).
1. Create a new key named `computing-historian`, and copy its value. Store it somewhere safe temporarily - you won't be able to view it again after you close the dialog.

## Implement the agent with the Claude SDK

Now you'll write Python code that implements your agent using the Anthropic SDK, and use it in a simple web-based chat application.

### Configure a client application in Visual Studio Code

A partially completed client application for your agent has been provided. You'll complete this app and test it.

1. Start Visual Studio Code.

    > **Tip**: If you're new to Visual Studio Code, you can refer to the [documentation](https://code.visualstudio.com/Docs){:target="_blank"} at `https://code.visualstudio.com/Docs` for help.

1. Open the command palette (*Ctrl+Shift+P* or on the **View** menu, select **Command Palette**) and enter the `Git:clone` command to clone the `https://github.com/GraemeMalcolm/mslearn-agent-quickstart-claude` repo to a local folder (it doesn't matter which one).
1. After the clone operation is complete, open the folder when prompted.

    The folder may open in **Restricted mode**. If so, select the mode and trust the authors to allow full functionality.

1. In the Activity bar on the left edge, view the **Extensions** pane; and if it is not already installed, search for and install the **Python** extension.
1. In the **Command Palette**, use the command `python:select interpreter` to create a new **Venv** environment based on your Python 3.1x installation.

    > **Tip**: You can choose to install the workspace dependencies in the *requirements.txt* file as you create the environment. Don't worry if you accidentally skip this though; we'll do it in a later step anyway.

    Wait for the environment to be created. It may take a while, and some notifications may be displayed during the process.

1. In the Activity bar, switch back to the **Explorer** pane, and navigate to the folder containing the application code files at **/computer-history-client**. The application files include:
    - **.env** (the application configuration file)
    - **agent_client.py** (the code file for the Python code that implements your agent)
    - **app.py** (the main code file for a Python Flask-based web application)
    - **feature-spec.md** (a specification for a feature you'll add later)
    - **requirements.txt** (the Python package dependencies that need to be installed)
1. In the **Explorer** pane, right-click the **agent_client.py** file, and select **Open in integrated terminal**.

    > **Tip**: Opening the terminal in Visual Studio Code should automatically activate the Python environment after a few seconds. If you're using a PowerShell terminal, you may need to enable running scripts on your system (see [Set-ExecutionPolicy](https://learn.microsoft.com/powershell/module/microsoft.powershell.security/set-executionpolicy){:target="_blank"}). If for any reason the Python environment is not activated automatically, you can use [this query](https://www.bing.com/search?q=%22How%20do%20I%20activate%20a%20Python%20venv%22){:target="_blank"} to search for information on how to activate it in your environment.

1. Ensure that the terminal is open in the **/computer-history-client** folder with the prefix **(.venv)** to indicate that the Python environment you created is active.
1. Install the required Python packages by running the following command:

    ```
   pip install -r requirements.txt
    ```

1. In the **Explorer** pane, in the **/computer-history-client** folder, select the **.env** file to open it. Then replace *your_api_key* with the API key you created in the Claude Console.

    > **Important**: An API key is a secret. Never commit it to source control or share it. In this exercise it's stored in a local *.env* file that your code loads at runtime - don't commit your edited *.env* file if you push changes to a repo.

1. Save the updated **.env** file.

### Add code to implement the agent

Now you're ready to implement the code that will submit prompts to Claude and return the responses.

1. In the **Explorer** pane, in the **/computer-history-client** folder, select the **agent_client.py** file (<u>not</u> *app.py*) to open it.
1. Review the existing code. You will add code that uses the Anthropic SDK to implement your agent.

    > **Tip**: As you add code to the code file, be sure to maintain the correct indentation.

1. Find the comment **Import the Anthropic client library**, and add the following code to import the SDK:

    ```python
   # Import the Anthropic client library
   from anthropic import Anthropic
    ```

1. Find the comment **Define the agent's instructions (system prompt) and tools**, and add the following code to define the system prompt and web search tool - just like the ones you tested in the playground:

    ```python
   # Define the agent's instructions (system prompt) and tools
   SYSTEM_PROMPT = (
        "You are an expert in the history of computing and AI. "
        "You only answer questions about significant people and events in the development "
        "of computing, and about notable vintage computers. "
        "Do not engage in conversations on any topic that is unrelated to computing history."
   )

   TOOLS = [
        {"type": "web_search_20260209", "name": "web_search", "max_uses": 5}
   ]
    ```

    > **Note**: The `type` value identifies a specific version of the web search tool. If you see a different value in the code from the playground, use that instead. The `max_uses` setting limits the number of searches Claude can perform for a single prompt.

1. In the **AgentClient** class, in the ****init**** function, note that code has been provided to load the API key and model name from the environment configuration file. Then find the comment **Create the Anthropic client** and add the following code:

    ```python
   # Create the Anthropic client
   self.client = Anthropic()
    ```

    The client automatically reads the **ANTHROPIC_API_KEY** environment variable (which was loaded from your *.env* file).

1. In the **send_message** function, note that code to add the user's prompt to the conversation history has been provided. Then, in the **try** block, find the comment **Run the agent loop** and add the following code:

    ```python
   # Run the agent loop
   messages = list(self.conversation_history)
   for _ in range(self.max_turns):
        response = self.client.messages.create(
            model=self.model,
            max_tokens=16000,
            system=SYSTEM_PROMPT,
            tools=TOOLS,
            messages=messages
        )

        # If Claude paused while using a server-side tool, send its progress back so it can continue
        if response.stop_reason == "pause_turn":
            messages.append({"role": "assistant", "content": response.content})
            continue

        # Otherwise, Claude has finished
        break

   # The response contains multiple content blocks (for example, web searches and results);
   # the text blocks make up the answer
   assistant_message = "".join(
        block.text for block in response.content if block.type == "text"
   )

   if response.stop_reason == "refusal":
        assistant_message = "I'm unable to help with that request."
    ```

    This code is the *agent loop*. Each time through the loop, Claude decides whether it needs to use its tool. Because web search is a server-side tool, Anthropic runs the search and Claude incorporates the results - all within a single call. A long-running turn may end with a **pause_turn** stop reason; in that case the loop sends Claude's work back to continue where it left off. When Claude finishes, the loop ends and the answer is extracted from the response.

    > **Tip**: For tools that run in <u>your</u> code (*client-side* tools), the loop works the same way, except that the stop reason is **tool_use**; and your code runs the tool and sends the result back to Claude in a new message. The process repeats until Claude has everything it needs to answer.

1. Read through the rest of the code, using the comments to understand the technique of tracking user inputs and responses in a conversation history.
1. Save the updated **agent_client.py** file.

### Run the client application

Now you're ready to test the app.

1. In the terminal, enter the following command to run the application:

    ```powershell
   python app.py
    ```

1. When the Flask application starts, open your browser and navigate to the URL where it is running - for example, [http://127.0.0.1:5000](http://127.0.0.1:5000) (`http://127.0.0.1:5000`).

    > **Tip**: If the app displays an error that the agent client isn't initialized, check that your API key is correctly set in the *.env* file, and that you saved the file.

1. Enter a prompt, such as `What was ENIAC?` and view the response.
1. Follow up with a second prompt, such as `How does it compare with COLOSSUS?`
1. Try an off-topic prompt, like `What's a good recipe for pancakes?`, to verify that the agent follows its instructions.
1. Try more prompts, like `Find the latest news for vintage computer enthusiasts.`

    Your agent should use its knowledge and tools to provide useful information and insights into computing history related topics.

1. When you've finished testing the app, close the browser, and in Visual Studio Code, enter **CTRL+C** in the terminal pane, to stop the local web server.

## Use Claude Code to enhance the application

Claude Code is an agentic coding assistant that can read your codebase, plan changes, edit files, and run commands. It's available in Visual Studio Code as an extension. You'll use it to add a new feature to your app.

> **Note**: Claude Code requires a paid Claude subscription (such as Pro or Max), or an Anthropic Console account with API credits - which you already have.

### Install and sign in to Claude Code

1. In Visual Studio Code, in the **Extensions** pane, search for and install the **Claude Code for VS Code** extension published by Anthropic.
1. Open Claude Code by selecting the **Claude Code** (spark) icon at the top right of the editor window, or by using the command palette to run `Claude Code: Open in New Tab`.
1. When prompted, sign in. You can sign in with your Claude account, or with your Anthropic Console account (which uses your API credits).

    > **Tip**: If you're using Claude Code in a folder you haven't used before, you may be asked to trust it. Since you cloned this repo yourself, you can do so.

### Add image input to the app

1. In the **Explorer** pane, in the **/computer-history-client** folder, select **feature-spec.md** and read its contents.

    This file contains a specification for a new feature that enables users to upload an image and submit it to the agent along with a text-based prompt.

1. With the specification file still open, in the Claude Code panel, enter the following prompt:

    ```
   Use the feature spec to add an image identification feature to the computer history client app.
    ```

    > **Tip**: For larger changes, you can switch Claude Code to *plan mode* first, to review its approach before it makes any edits.

1. Review what Claude Code does. It will explore the code, then propose edits to files such as *agent_client.py*, *app.py*, and the files in the **/templates** and **/static** folders.

    The process may take a few minutes, and you may be prompted to approve edits or commands. Review each change shown before you accept it.

1. When Claude Code has finished, view the changes to **agent_client.py**. Look for how the image is added to the user's message alongside the text.

    The Messages API accepts a message with a list of *content blocks* - for example, an **image** block (containing base64-encoded image data and its media type) followed by a **text** block containing the prompt.

1. In the terminal, re-run the app (`python app.py`), and then open your browser and navigate to the URL where it is running.

    > **Tip**: Claude Code can also run the app and check for errors itself - if the app doesn't start, tell Claude Code what you see and ask it to fix the problem.

1. In the revised version of the app, upload one of the images from the **/test-images** folder (which is in the folder where you cloned the repo); and enter the prompt `What can you tell me about this?`
1. Review the response, which should provide information about the computer in the image you uploaded.
1. Try the other images in the *test-images* folder with prompts like `What about this?` or `Tell me about this.`
1. Test the error handling by trying to upload an unsupported file type, and then a text-only prompt to confirm that existing behavior still works.
1. If you're happy with the code that Claude Code has generated, you can keep the changes. If not, continue the conversation with Claude Code, specifying the changes you would like - or use its checkpoint/rewind feature to undo them.
1. When you've finished testing the app, close the browser, and in Visual Studio Code, enter **CTRL+C** in the terminal pane, to stop the local web server.

## Summary

In this exercise, you prototyped an AI agent in the Claude Console, implemented it in Python using the Claude SDK to run an agent loop with a web search tool, and then used Claude Code to add image input support to the application.

## Clean up

If you created an API key for this exercise, you can delete it in the **API keys** page of the Claude Console, so that it can't be used again.
