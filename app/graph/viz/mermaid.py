import os, pyperclip


def visualize(agent_graph):
    mermaid = agent_graph.get_graph().draw_mermaid()
    print(mermaid)
    print("Copied mermaid script to clipboard.. \nPaste it in the opened editor to visualize the graph.")
    pyperclip.copy(mermaid)
    os.system("start \"\" https://mermaid.live/edit")