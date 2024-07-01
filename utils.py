from crewai import Agent, Task, Crew
import warnings
warnings.filterwarnings('ignore')

from crewai import Agent, Task, Crew
import google.generativeai as genai
from IPython.display import Markdown
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
load_dotenv()

llm = ChatGoogleGenerativeAI(model="gemini-pro", temperature=0.2)

support_agent = Agent(
    role="Senior Support Representative",
    goal="Be the most friendly and helpful support representative in your team",
    backstory=(
        "You work at Microsoft Autogen (https://microsoft.github.io/autogen/docs/FAQ) and "
        "are now working on providing support to {customer}, a super important customer for your company."
        "You need to make sure that you provide the best support!"
        "Make sure to provide full complete answers with practical coding (if needed), and make no assumptions."
    ),
    verbose=True,
    llm=llm
)

support_quality_assurance_agent = Agent(
    role="Support Quality Assurance Specialist",
    goal="Get recognition for providing the best support quality assurance in your team",
    backstory=(
        "You work at Microsoft Autogen (https://microsoft.github.io/autogen/docs/FAQ) and are now working with your team "
        "on a request from {customer} ensuring that the support representative is providing the best support possible."
        "You need to make sure that the support representative is providing full"
        "complete answers with code (if needed), and make no assumptions."
    ),
    verbose=True,
    llm=llm,
    allow_delegation = False
)

from crewai_tools import SerperDevTool, ScrapeWebsiteTool

docs_scrape_tool = ScrapeWebsiteTool(
    website_url="https://microsoft.github.io/autogen/docs/FAQ"
)

inquiry_resolution = Task(
    description=(
        "{customer} just reached out with a super important ask:\n"
        "{inquiry}\n\n"
        "{customer} is the one that reached out. "
        "Make sure to use everything you know to provide the best support possible."
        "You must strive to provide a complete and accurate response to the customer's inquiry."
    ),
    expected_output=(
        "A detailed, informative response to the customer's inquiry that addresses "
        "all aspects of their question."
        "The response should include codes and references to everything you used to find the answer, "
        "including external data or solutions. "
        "Ensure the answer is complete, leaving no questions unanswered, and maintain a helpful and friendly tone throughout. "
        "If you write any code make it look like python code, it shouldn't look like normal texts, use markdown if needed."
    ),
    tools=[docs_scrape_tool],
    agent=support_agent,
    llm=llm
)

quality_assurance_review = Task(
    description=(
        "Review the response drafted by the Senior Support Representative for {customer}'s inquiry. "
        "Ensure that the answer is comprehensive, accurate, and adheres to the high-quality standards expected for customer support."
        "Verify that all parts of the customer's inquiry have been addressed thoroughly, with a helpful and friendly tone."
        "Check for references and sources used to find the information, ensuring the response is well-supported and leaves no questions unanswered."
    ),
    expected_output=(
        "A final, detailed, and informative response with code snippets (if there any) ready to be sent to the customer."
        "This response should fully address the customer's inquiry, incorporating all relevant feedback and improvements."
        "If you write any code make it look like python code, it shouldn't look like normal texts, use markdown if needed."
        "Don't be too formal, we are a chill and cool company but maintain a professional and friendly tone throughout."
    ),
    agent=support_quality_assurance_agent,
    llm=llm
)

crew = Crew(
    agents=[support_agent, support_quality_assurance_agent],
    tasks=[inquiry_resolution, quality_assurance_review],
    verbose=2,
    memory=False
)

def generate_response(customer, inquiry):
    inputs = {
        "customer": customer,
        "inquiry": inquiry
    }
    result = crew.kickoff(inputs=inputs)
    return result

def execute(customer, quiry):
    result = generate_response(customer, quiry)
    # result = Markdown(result)
    return result