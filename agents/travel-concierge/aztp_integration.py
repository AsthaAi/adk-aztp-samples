import asyncio
import os
from aztp_client import Aztp  # Assuming you have the client installed
from google.adk.agents import Agent
# Assuming your prompt module is in the same directory or accessible
from travel_concierge import prompt
# from travel_concierge.sub_agents import (
#     inspiration_agent,
#     planning_agent,
#     booking_agent,
#     pre_trip_agent,
#     in_trip_agent,
#     post_trip_agent,
# )
# from travel_concierge.itinerary import _load_precreated_itinerary
from travel_concierge.agent import root_agent
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


async def main():
    # Initialize your AZTP client (configure as needed)
    API_KEY = os.getenv("AZTP_API_KEY")
    if not API_KEY:
        raise ValueError("AZTP_API_KEY environment variable is not set")

    client = Aztp(api_key=API_KEY)

    try:
        agent_identity = await client.secure_connect(
            root_agent,
            "travel-somit-agent",
            {
                "isGlobalIdentity": True
            }
        )
        print(
            f"Agent 'travel-somit-agent' identity created successfully: {agent_identity}")
        # You might want to store or communicate this identity
    except Exception as e:
        print(f"Error connecting with AZTP: {e}")


if __name__ == "__main__":
    asyncio.run(main())
