# File: prototype/visualization/knowledge_visualizer.py

import networkx as nx
import matplotlib.pyplot as plt
import json
from pathlib import Path
import numpy as np

class KnowledgeVisualizer:
    """Visualizes knowledge structure from EdNet analysis."""
    
    def __init__(self, structure_path: str):
        with open(structure_path) as f:
            self.structure = json.load(f)
            
    def create_knowledge_graph(self, output_path: Path) -> None:
        """Create knowledge graph visualization."""
        G = nx.DiGraph()
        
        # Add nodes (concepts)
        for concept, data in self.structure['concepts'].items():
            G.add_node(concept, 
                      difficulty=data['difficulty'],
                      attempts=data['total_attempts'])
        
        # Add edges (relationships)
        for rel_name, data in self.structure['relationships'].items():
            source, target = data['connects']
            G.add_edge(source, target, 
                      weight=data['strength'],
                      bidirectional=data['bidirectional'])
        
        # Set up the plot
        plt.figure(figsize=(12, 8))
        
        # Calculate node sizes based on attempts
        attempts = [G.nodes[n]['attempts'] for n in G.nodes()]
        node_sizes = [1000 * a/max(attempts) for a in attempts]
        
        # Calculate node colors based on difficulty
        difficulties = [G.nodes[n]['difficulty'] for n in G.nodes()]
        node_colors = plt.cm.RdYlGn_r(difficulties)
        
        # Calculate edge widths and colors based on relationship strength
        edge_weights = [G[u][v]['weight'] for u,v in G.edges()]
        edge_widths = [3 * w/max(edge_weights) for w in edge_weights]
        edge_colors = plt.cm.Blues([w for w in edge_weights])
        
        # Create layout
        pos = nx.spring_layout(G, k=1, iterations=50)
        
        # Draw the network
        nx.draw_networkx_nodes(G, pos, 
                             node_size=node_sizes,
                             node_color=node_colors)
        
        nx.draw_networkx_edges(G, pos,
                             width=edge_widths,
                             edge_color=edge_colors,
                             arrows=True,
                             arrowsize=20)
        
        # Add labels
        labels = {}
        for node in G.nodes():
            difficulty = G.nodes[node]['difficulty']
            attempts = G.nodes[node]['attempts']
            labels[node] = f"{node}\n(d:{difficulty:.2f})"
        
        nx.draw_networkx_labels(G, pos, labels, font_size=8)
        
        # Add legend
        plt.text(1.2, 0.95, 'Node Size: Number of Attempts', 
                transform=plt.gca().transAxes)
        plt.text(1.2, 0.90, 'Node Color: Difficulty', 
                transform=plt.gca().transAxes)
        plt.text(1.2, 0.85, 'Edge Width/Color: Relationship Strength', 
                transform=plt.gca().transAxes)
        
        # Add title
        plt.title('Knowledge Structure Analysis\nNode size: attempts, '
                 'Color: difficulty (red=hard), Edge: relationship strength')
        
        # Save plot
        plt.savefig(output_path / 'knowledge_structure.png', 
                   bbox_inches='tight', dpi=300)
        plt.close()
        
    def create_learning_progression(self, output_path: Path) -> None:
        """Create learning progression visualization."""
        plt.figure(figsize=(12, 6))
        
        concepts = list(self.structure['concepts'].keys())
        difficulties = [self.structure['concepts'][c]['difficulty'] 
                       for c in concepts]
        attempts = [self.structure['concepts'][c]['total_attempts'] 
                   for c in concepts]
        times = [self.structure['concepts'][c]['avg_time'] 
                for c in concepts]
        
        # Sort by difficulty
        sorted_indices = np.argsort(difficulties)
        concepts = [concepts[i] for i in sorted_indices]
        difficulties = [difficulties[i] for i in sorted_indices]
        attempts = [attempts[i] for i in sorted_indices]
        times = [times[i] for i in sorted_indices]
        
        # Create plot
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8))
        
        # Difficulty and attempts
        color1 = 'tab:red'
        color2 = 'tab:blue'
        
        ax1.bar(concepts, difficulties, color=color1, alpha=0.6)
        ax1.set_ylabel('Difficulty', color=color1)
        ax1.tick_params(axis='y', labelcolor=color1)
        
        ax3 = ax1.twinx()
        ax3.plot(concepts, attempts, 'o-', color=color2)
        ax3.set_ylabel('Number of Attempts', color=color2)
        ax3.tick_params(axis='y', labelcolor=color2)
        
        ax1.set_title('Concept Difficulty vs. Attempts')
        plt.setp(ax1.xaxis.get_majorticklabels(), rotation=45)
        
        # Average time
        ax2.bar(concepts, times, color='tab:green', alpha=0.6)
        ax2.set_ylabel('Average Time (seconds)')
        ax2.set_title('Average Time per Concept')
        plt.setp(ax2.xaxis.get_majorticklabels(), rotation=45)
        
        plt.tight_layout()
        plt.savefig(output_path / 'learning_progression.png')
        plt.close()
        
    def visualize_all(self, output_dir: str = 'results') -> None:
        """Generate all visualizations."""
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        
        self.create_knowledge_graph(output_path)
        self.create_learning_progression(output_path)