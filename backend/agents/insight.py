# Load environment variables from a .env file.
import os
from dotenv import load_dotenv
load_dotenv(os.path.join(os.path.dirname(__file__), "..", "credentials.env"))

# Define structured output models using Pydantic
from pydantic import BaseModel, RootModel

# Langchain imports that we will use to interact with OpenAI
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from langchain_classic.agents import create_openai_tools_agent, AgentExecutor

# Define the structure of the output
from pydantic import BaseModel, RootModel

# Import analyses
from logics.analyses import analyses
from typing import List, Literal

class VisualizationPlan(BaseModel):
    """
    Output:
        analysis_type (Literal): Type of analysis that can be done with the data
        tools (List[str]): List of best chart types for the given analysis
        vars (List[str]): List of features required for the visualization
    """
    analysis_type: Literal["distribution", "comparison", "relationship", "composition"]
    tools: List[str]
    vars: List[str]

class InsightSummary(BaseModel):
    """
    Output:
        insight (str): Insights on the data in markdown format
        plans (List[VisualizationPlan]): List of useful features only from the data to visualize the data
    """
    insight: str
    plans: List[VisualizationPlan]

class InsightSummaryList(RootModel[list[InsightSummary]]):
    """
    Output:
        List[InsightSummary]
    """
    pass

class InsightAgent:
    """
    Args:
        data_profile (dict): Dictionary containing the data profile
        model (str): Model to be used for the generation of the insights
    
    Output:
        InsightSummaryList: List of InsightSummary objects
    """
    def __init__(self, data_profile: dict, model: str = 'gpt-5.4-nano-2026-03-17'):
        self.data_profile = data_profile
        self.model = model

    def generate(self):
        # Define llm
        llm = ChatOpenAI(model=self.model)

        # Tell llm how to format the response using the Pydantic schema
        parser = PydanticOutputParser(pydantic_object=InsightSummaryList)

        # The main part here. This is our prompt and the instructions we give to llm
        prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    """
                    You are a Data Insight Summary expert.
                    1. Analyze the Dict content given by user to provide:
                        - insight: Insights on the data in markdown format
                        - plans: Name of the useful features only from the data to visualize the data       
                    2. Generate **insight**:
                        - Write clear, structured insights in **valid markdown**
                        - Focus on:
                            - Data quality (missingness, imbalance)
                            - Distributions (numeric + categorical)
                            - Notable patterns (skew, dominance, spread)
                        - Keep it concise but informative (no fluff)
                        - Use following headings in the markdown file
                            - Data Quality
                            - Numerical Features
                            - Categorical Features
                            - Insights Summary
                    3. Generate **plans**:
                        - For each plan, return:
                            - analysis_type: One of ["distribution", "comparison", "relationship", "composition"]
                            - tools: A list containing EXACTLY ONE best chart type for the given analysis
                                Rules:
                                - Select ONLY ONE most appropriate chart
                                - Do NOT return multiple tools
                                - Prefer:
                                - histogram for numeric distribution
                                - bar for categorical distribution
                                - scatter for relationship
                                - boxplot for comparison (numeric vs categorical)
                            - vars: List of feature names from the input required for the visualization
                    4. Markdown file structure:
                        - Use the provided headings.
                        - Bold and use backticks to hightlight the feature names. For example: **`feature`**.
                    5. Here is the analyses types for the visualization: {analyses}
                    6. Do not include extra text beyond the formatted output and the save confirmation message.
                    7. Return the output as a list of 1 entries in this format: {format_instructions}
                    """,
                ),
                ("human", "{query}"),
                ("placeholder", "{agent_scratchpad}"),  
            ]
        ).partial(format_instructions=parser.get_format_instructions())

        # Create the agent with tool-calling abilities and structured reasoning
        # TODO: Add tool calling abilities
        agent = create_openai_tools_agent(
            llm=llm,
            tools=[],
            prompt=prompt,
        )

        # Wrap the agent in an executor for running it with inputs
        agent_executor = AgentExecutor(agent=agent, tools=[])

        # Run the agent with the query
        raw_response = agent_executor.invoke({"query": self.data_profile, "analyses": analyses})

        # Parse the structured output using the Pydantic schema
        try:
            structured_response = parser.parse(raw_response.get('output'))
            return structured_response
        except Exception as e:
            raise ValueError("Error parsing response", e, "Raw Response - ", raw_response)