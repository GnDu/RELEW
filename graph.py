from typing import List,Set,Tuple
from pydantic import BaseModel

class TripleGraph(BaseModel):
    """ This class models what a knowledge graph, G. 
    
    G is defined as $G = (V, E)$ where $V$ is the set of 
    entities. $E$ is the set of directed edges with no 
    self reference, $E = \{(v_i, v_j, r)\space\vert\space 
    v_i, v_j \in V, v_i \neq v_j, r \in R\}$

    This class also contains atomic operations for manipulating
    the graph, mainly adding and removing vertices and edges through 
    add_vertex, remove_vertex, add_edge, remove_edge.

    """
    vertices:Set[str]
    edges:List[Tuple[str,str, str]]

    def add_vertex(self, vertex_id:str):
        """Add a vertex, $v$ to the graph $G$.
        
        vertex_id / $v$ is a string that uniquely identify the vertex.
        Note, this function does not check for duplicates.

        Parameters
        ----------
        vertex_id:str
            the id, $v$ that uniquely identify the vertex
        """
        self.vertices.add(vertex_id)
    
    def remove_vertex(self, vertex_id:str):
        """Remove a vertex, $v$ from the graph $G$.
        
        vertex_id / $v$ is a string that uniquely identify the verte
        Note, this function does not check whether $v$ exists. It will
        raise an exception if it does not.


        Parameters
        ----------
        vertex_id:str
            the id, $v$ that uniquely identify the vertex

        Raises
        ------
        ValueError
            if vertex_id does not exist
        """

        self.vertices.remove(vertex_id)

    def add_edge(self, head:str, relation_label:str, tail:str):
        """
        Add edge, $(v_i, r, v_j)$ to the graph, $G$. 

        Parameters
        ----------
        head:str
            the vertex id that serves as the source, $v_i$

        relation_label:str
            the relation label, $r$ for the edge 

        tail:str
            the vertex id that serves as the sink, $v_j$

        """
        if head not in self.vertices:
            raise ValueError(f"{head} not added. Use add_vertex to add vertex first")
        
        if tail not in self.vertices:
            raise ValueError(f"{tail} not added. Use add_vertex to add vertex first")
        
        self.edges.append((head, relation_label, tail))

    def remove_edge(self, head:str, relation_label:str, tail:str):
        """
        Remove the edge, $(v_i, r, v_j)$ from the graph, $G$. 
        
        Note, this function does not check whether $(v_i, r, v_j)$ exists. It will
        raise an exception if it does not.

        Parameters
        ----------
        head:str
            the vertex id that serves as the source, $v_i$

        relation_label:str
            the relation label, $r$ for the edge 

        tail:str
            the vertex id that serves as the sink, $v_j$

        Raises
        ------
        ValueError
            if (head, relation_label, tail) / $(v_i, r, v_j)$ does not exist
        """
        self.edges.remove((head, relation_label, tail))

    def format_edges(self):
        return "[\n" + "\n".join([f"({e[0]}, {e[1]}, {e[2]})" for e in self.edges]) + "\n]"
