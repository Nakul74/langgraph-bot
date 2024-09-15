from langgraph.graph import StateGraph
from src.graph import graph_utils


def get_graph_workflow():

    workflow = StateGraph(graph_utils.GraphState)

    # Define the nodes
    workflow.add_node("generate", graph_utils.generate)  # generatae
    workflow.add_node("check_hallucination", graph_utils.check_hallucination)  # check_hallucination
    workflow.add_node("push_to_slack", graph_utils.push_to_slack)  # push to slack

    workflow.set_entry_point("generate")
    workflow.add_edge("generate", "check_hallucination")
    workflow.add_edge("check_hallucination", "push_to_slack")
    workflow.set_finish_point("push_to_slack")

    app = workflow.compile()
    
    return app
    
