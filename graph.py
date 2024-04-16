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
    vertices:List[str]
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
        self.vertices.append(vertex_id)
    
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

    def add_edge(self, from_id:str, to_id:str, relation_label:str):
        """
        Add edge, $(v_i, v_j, r)$ to the graph, $G$. 

        Note, this function does not check for duplicates.

        Parameters
        ----------
        from_id:str
            the vertex id that serves as the source, $v_i$

        to_id:str
            the vertex id that serves as the sink, $v_j$

        relation_label:str
            the relation label, $r$ for the edge 
        """
        self.edges.append((from_id, to_id, relation_label))

    def remove_edge(self, from_id:str, to_id:str, relation_label:str):
        """
        Remove the edge, $(v_i, v_j, r)$ from the graph, $G$. 
        
        Note, this function does not check whether $(v_i, v_j, r)$ exists. It will
        raise an exception if it does not.

        Parameters
        ----------
        from_id:str
            the vertex id that serves as the source, $v_i$

        to_id:str
            the vertex id that serves as the sink, $v_j$

        relation_label:str
            the relation label, $r$ for the edge 

        Raises
        ------
        ValueError
            if (from_id, to_id, relation_label) / $(v_i, v_j, r)$ does not exist
        """
        self.edges.remove((from_id, to_id, relation_label))
