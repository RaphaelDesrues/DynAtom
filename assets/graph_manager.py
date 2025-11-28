from gui.graph_view import GraphView


class GraphManager():
    """GraphManager is a class that manages multiple graph views for visualizing simulation data.
    
    Attributes:
        graphs (dict): A dictionary that stores graph views, where the key is the graph name and the value is the corresponding GraphView object.
    
    Methods:
        add_graph(name, graph_view):
            Adds a new graph view to the manager.
    
        get_widgets():
            Returns a list of plot widgets for all managed graph views.
    
        update_all(engine):
            Updates all graph views with data from the provided engine.
    """
    def __init__(self):
        
        self.graphs = {}
        
        self.add_graph("LJ_potential_total", GraphView("LJ potential",
                                                       "step number",
                                                       "Potential Energy (kcal/mol)",
                                                    ))
        
        self.add_graph("force_norm_total", GraphView("Total forces",
                                                     "Step number",
                                                     "Total forces",
                                                    ))


        self.add_graph("acc_norm_total", GraphView("Total acceleration",
                                                   "Step number"
                                                   "Total acceleration",
                                                   ))

    def add_graph(self, name, graph_view):
        self.graphs[name] = graph_view

    def get_widgets(self):
        return [graph_view.plot for graph_view in self.graphs.values()]

    def update_all(self, engine):
        for key, view in self.graphs.items():
            view.update(engine, key)
