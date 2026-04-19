import json
from agents.retrieval_planner_agent import retrieval_planner_agent
from tests.schemas import RetrievalPlan

def test_retrieval_planner_outputs_valid_json():

    test_queries = [
        "snacks for tea",
        "cheap phones",
        "something for my kitchen",
        "gifts for kids",
    ]

    for q in test_queries:
        state = {"user_query": q}
        state = retrieval_planner_agent(state)

        plan = state["planner_output"]

        # Schema validation
        RetrievalPlan(**plan)

        #Security property
        assert plan["strategy"] in ["search", "category", "general"]