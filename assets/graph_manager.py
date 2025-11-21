from gui.graph_controler import GraphControler


class GraphManager():

    def __init__(self):
        
        super().__init__()

        self.graphs = {}

        self.add_graph("LJ potential", GraphControler("LJ potential"))

    def add_graph(self, name, graph_controler):
        self.graphs[name] = graph_controler

    def get_widgets(self):
        return [ctrl.plot for ctrl in self.graphs.values()]

    def update_all(self, engine):
        for controler in self.graphs.values():
            controler.update(engine)
