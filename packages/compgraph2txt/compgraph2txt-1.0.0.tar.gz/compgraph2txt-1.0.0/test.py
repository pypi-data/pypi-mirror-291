from networkx import MultiDiGraph

from compgraph2txt import compgraph2txt

# graph = MultiDiGraph()
# graph.add_node("Camera", inputs=[], outputs=["Image"])
# graph.add_node(
#     "Foreground Detection", inputs=["Image"], outputs=["Foreground", "Background"]
# )
# graph.add_node("Blur", inputs=["Image"], outputs=["Blurred Image"])
# graph.add_node("Image Overlay", inputs=["Foreground", "Background"], outputs=["Image"])
# graph.add_node("Application", inputs=["Image"], outputs=[])

# graph.add_edge("Camera", "Foreground Detection", output="Image", input="Image")
# graph.add_edge("Foreground Detection", "Blur", output="Background", input="Image")
# graph.add_edge("Blur", "Image Overlay", output="Blurred Image", input="Background")
# graph.add_edge(
#     "Foreground Detection", "Image Overlay", output="Foreground", input="Foreground"
# )
# graph.add_edge("Image Overlay", "Application", output="Image", input="Image")

# print(compgraph2txt(graph))


graph = MultiDiGraph()
graph.add_node(
    "A", name="A", inputs=["a", "b", "c", "d"], outputs=["e", "f", "g", "h", "i"]
)
graph.add_node("Z", name="Z", inputs=["t", "u", "v", "w"], outputs=["x", "y", "z"])

# Add edges from external sources
graph.add_edge("ext1", "A", input="c")
graph.add_edge("ext1", "Z", input="v")
graph.add_edge("ext2", "A", input="a")
graph.add_edge("ext3", "Z", input="w")

# Add edges to external sinks
graph.add_edge("A", "ext", output="f")
graph.add_edge("A", "ext", output="i")
graph.add_edge("Z", "ext", output="x")
graph.add_edge("Z", "ext", output="z")
graph.add_edge("Z", "ext", output="x")
graph.add_edge("Z", "ext", output="z")

# Add edges between nodes
graph.add_edge("A", "Z", output="e", input="t")
graph.add_edge("A", "Z", output="g", input="u")

output = compgraph2txt(graph)
print(output)
