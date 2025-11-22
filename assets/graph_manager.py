from gui.graph_view import GraphView


class GraphManager():
    """GraphManager is a class that manages multiple graph views.
    
    Attributes:
        graphs (dict): A dictionary that stores graph views with their corresponding names.
    
    Methods:
        add_graph(name, graph_view):
            Adds a new graph view to the manager.
    
        get_widgets():
            Returns a list of plot widgets from all graph views.
    
        update_all(engine):
            Updates all graph views with the provided engine.
    """
    def __init__(self):
        
        self.graphs = {}
        
        self.add_graph("LJ_potential", GraphView("LJ potential",
                                                 "Potential Energy (kcal/mol)",
                                                 "step number"))

        self.add_graph("Total_forces", GraphView("Total forces"))

    def add_graph(self, name, graph_view):
        self.graphs[name] = graph_view

    def get_widgets(self):
        return [graph_view.plot for graph_view in self.graphs.values()]

    def update_all(self, engine):
        for key, view in self.graphs.items():
            view.update(engine, key)
