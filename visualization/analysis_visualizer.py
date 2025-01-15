# File: analysis_visualizer.py

import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pandas as pd
from typing import List, Dict, Optional
import torch
from datetime import datetime
from pathlib import Path
import networkx as nx
from sklearn.manifold import TSNE
import logging

logger = logging.getLogger(__name__)

class AnalysisVisualizer:
    def __init__(self, output_dir: str = "results/visualizations"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.current_figures = {}
        
        # Set style
        plt.style.use('seaborn')
        sns.set_palette("husl")
    
    def visualize_learning_patterns(self, 
                                  pss_patterns: List[torch.Tensor],
                                  ednet_patterns: List[torch.Tensor],
                                  title: str = "Learning Pattern Comparison") -> None:
        """Visualize learning patterns using t-SNE."""
        logger.info("Generating learning pattern visualization...")
        
        # Convert patterns to numpy arrays
        pss_data = torch.stack(pss_patterns).numpy()
        ednet_data = torch.stack(ednet_patterns).numpy()
        
        # Apply t-SNE
        tsne = TSNE(n_components=2, random_state=42)
        combined_data = np.vstack([pss_data, ednet_data])
        embedded_data = tsne.fit_transform(combined_data)
        
        # Split back into PSS and EdNet
        pss_embedded = embedded_data[:len(pss_data)]
        ednet_embedded = embedded_data[len(pss_data):]
        
        # Create visualization
        plt.figure(figsize=(10, 8))
        plt.scatter(pss_embedded[:, 0], pss_embedded[:, 1], 
                   label='PSS', alpha=0.6)
        plt.scatter(ednet_embedded[:, 0], ednet_embedded[:, 1], 
                   label='EdNet', alpha=0.6)
        
        plt.title(title)
        plt.legend()
        self._save_figure("learning_patterns.png")
    
    def visualize_topic_relationships(self, 
                                    topic_similarities: Dict[str, Dict[str, float]]) -> None:
        """Visualize topic relationship graph."""
        logger.info("Generating topic relationship visualization...")
        
        G = nx.Graph()
        
        # Add edges with weights
        for topic1, similarities in topic_similarities.items():
            for topic2, weight in similarities.items():
                if weight > 0.3:  # Threshold for visualization
                    G.add_edge(topic1, topic2, weight=weight)
        
        # Create layout
        pos = nx.spring_layout(G)
        
        plt.figure(figsize=(12, 8))
        
        # Draw edges with varying thickness
        edges = G.edges()
        weights = [G[u][v]['weight'] * 5 for u, v in edges]
        nx.draw_networkx_edges(G, pos, width=weights, alpha=0.5)
        
        # Draw nodes
        nx.draw_networkx_nodes(G, pos, node_size=1000, 
                             node_color='lightblue', alpha=0.7)
        
        # Add labels
        nx.draw_networkx_labels(G, pos)
        
        plt.title("Topic Relationships")
        self._save_figure("topic_relationships.png")
    
    def visualize_learning_trajectories(self, 
                                      trajectories: Dict[str, List[float]]) -> None:
        """Visualize learning trajectories over time."""
        logger.info("Generating learning trajectory visualization...")
        
        plt.figure(figsize=(12, 6))
        
        for user_id, scores in trajectories.items():
            plt.plot(range(len(scores)), scores, label=f"User {user_id}", 
                    alpha=0.7, marker='o')
        
        plt.title("Learning Trajectories")
        plt.xlabel("Interaction Number")
        plt.ylabel("Performance Score")
        plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
        plt.tight_layout()
        
        self._save_figure("learning_trajectories.png")
    
    def visualize_engagement_patterns(self, 
                                    engagement_data: pd.DataFrame) -> None:
        """Visualize engagement patterns."""
        logger.info("Generating engagement pattern visualization...")
        
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
        
        # Response time distribution
        sns.boxplot(x='topic', y='response_time', data=engagement_data, ax=ax1)
        ax1.set_xticklabels(ax1.get_xticklabels(), rotation=45)
        ax1.set_title("Response Time by Topic")
        
        # Engagement over time
        sns.lineplot(data=engagement_data, x='timestamp', 
                    y='engagement_score', hue='user_id', ax=ax2, alpha=0.7)
        ax2.set_title("Engagement Over Time")
        
        plt.tight_layout()
        self._save_figure("engagement_patterns.png")
    
    def create_performance_heatmap(self, 
                                 performance_matrix: np.ndarray,
                                 labels: List[str]) -> None:
        """Create performance heatmap."""
        logger.info("Generating performance heatmap...")
        
        plt.figure(figsize=(10, 8))
        sns.heatmap(performance_matrix, annot=True, fmt='.2f', 
                   xticklabels=labels, yticklabels=labels,
                   cmap='YlOrRd')
        
        plt.title("Performance Correlation Heatmap")
        plt.tight_layout()
        