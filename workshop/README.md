## Challenging GitHub Copilot

Let's go through some challenging requests for GitHub Copilot and address them
as they happen.

> [!NOTE]
> This repo is intended to give an introduction to various **GitHub Copilot** features, such as **Copilot Chat** and **inline chat**. Hence the step-by-step guides below contain the general description of what needs to be done, and Copilot Chat or inline chat can support you in generating the necessary commands.
>
> Each step (where applicable) also contains a `Cheatsheet` which can be used to validate the Copilot suggestion(s) against the correct command.
>
> 💡 Play around with different prompts and see how it affects the accuracy of the GitHub Copilot suggestions. For example, when using inline chat, you can use an additional prompt to refine the response without having to rewrite the whole prompt.

## Workshop features

In this workshop, you will be working with data from a CSV file included in
this repository as well as a Python web application that loads the data into
a SQLite3 database and executes complex queries on it. Here are some features:

1. Load the web application and open up the browser
1. Identify the potential performance problem when loading initially
1. All dependencies and libraries are pre-installed


### 1. Explore the project using agents

Use the `@workspace` agent to explain what is going on with this project.

- Open GitHub Copilot Chat and prefix your prompt with `@workspace`
- Ask questions like how to run the project

### 2. Determine the performance problem

Launch your project and run the web application. Confirm there is a performance
problem when loading the main website.

- Try to run the project based on the suggestions of `@workspace` agent
- Navigate to the resulting URL and confirm the performance problem

> [!NOTE]
> Why this might not work? Dependencies might not be installed, or commands are
> not available or have different versions. Be more specific and open more
> files to help.

### 3. Explore the complex.sql query

The complex.sql file contains the query that is being executed in the
application. Open it up and use inline chat with `/explain` to find more about
certain parts.

- Ask questions about the `CROSS JOIN`
- Ask if any parts are unnecessary

> [!NOTE]
> Why this might not provide correct explanations? Because the business logic
> may want to have some of this components which aren't obvious to the LLM


### 4. Explore the web application

The web application is using Python, but the setup is unorthodox using Sqlite3
and executing a complex query on an endpoint.

- Open main.py and use `/explain` on the endpoint executing the request
- Open the test file and use Copilot Chat to understand more about these tests


### 5. Determine optimizations for the query

Now that the application and the complex query are clear, determine potential
fixes.

- Select the `CROSS JOIN` sections and use inline chat with /explain
- GitHub Copilot will probably suggest to avoid the `CROSS JOIN` with an
  explanation, suggest adding a test to validate this change
- Ask GitHub Copilot to add a Python test to validate the changes
- See how Copilot will probably not want to do this, keep trying different
  prompts

> [!NOTE]
> Why the fixes might not be ideal? Because the results might be specific to
> the application and business logic, which Copilot isn't aware of. The test
> part will push Copilot to use a SQL test rather than Python because this is
> not common, even when being specific. Try opening the test file and add tests
> directly instead.


### 6. Add more tests for full coverage

Before doing any changes to the SQL query, make sure that the API will still
respond as expected after modifications.

- Open the test file and continue adding the remaining cases
- Use GitHub Copilot autocompletion instead of chat
- Run the tests at the end with `pytest -v` in the terminal or using Visual
  Studio Code for verification
- Ensure all tests are passing and are covering all the cases for each column

> [!NOTE]
> It is easier for copilot to see a pattern and continue suggesting similar
> tests. Whenever Copilot provides non-ideal suggestions keep typing until it
> does.


### 7. Try to optimize the SELECT DISTINCT section

That part of the query is doing redundant work, but it is unclear what each
part is going. Use Copilot Chat to explain changes

- Ask _"how would you optimize this part of the query. Explain your reasoning"_
- Try to get a better understanding and ignore when Copilot insists on removing
  the CROSS JOINs
- Further insist on focusing only on the selection
- Ask why is it necessary to multiply by 1000


> [!TIP]
> It isn't necessary to multiply by 1000 and we can use NULLIF. Verify that
> Sqlite3 supports NULLIF. Optimization is an opinionated suggestion, it may
> not fully apply with the intent of the query.


### 8. Safely Replace the CROSS JOIN

The `CROSS JOIN` statements are indeed completely unnecessary. Ask Copilot how
to safely remove them or replace them.

- Open Chat and ask about the problem statements
- Use the suggestions to change them
- Run tests to verify speedups

> [!NOTE]
> Some of the removals might break the tests. It is imperative to have
> validation and not blindlty remove or change parts of the query. Use the
> tests to guide you for safe removal of redundant code.


### 9. Go through other possible optimizations

For example, ask why `CAST` is necessary in the first `SELECT` and how to
optimize it. Go through the suggestions and apply them.

- Perform selections for providing context, ask about optimizations and apply
  them
- After applying them, run the tests and ensure nothing breaks
- Continue throughout all sub-queries and apply optimizations ensuring tests
  are passing

> [!NOTE]
> The CAST is completely unnecessary and it can use other ways to accomplish
> this. It is also wasteful to have the SQL provide this when this could
> potentially be solved on the code side. Sometimes what you ask is not really
> what you may need. Come up with other alternatives or ask about other
> potential approaches to accomplish what you need.


### 10. Ask for a prompt that would recreate a high-performing query

Push the limits of GitHub Copilot by asking to generate a prompt that could
potentially create the query from scratch while being high-performing.

- Select the whole complex.sql query and open Chat
- Ask Copilot to create a prompt
- Copy the prompt, open a new chat session and paste the prompt
- Apply the results of the suggestion and run the tests to verify they still
  pass

> [!NOTE]
> Why this might not work? Because generic questions provide generic answers,
> and even if Copilot produces a good prompt, it still might miss core business
> logic that is essential for the product.
