from src.graph import build_graph

def main():
    graph = build_graph()
    initial_state = {}
    final_state = graph.invoke(initial_state)
    print("Content generation completed. Outputs written to outputs/")

if __name__ == "__main__":
    main()
