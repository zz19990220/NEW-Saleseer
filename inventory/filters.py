import pandas as pd
from typing import Dict, List, Any, Optional


class ProductFilter:
    def __init__(self, csv_path: str = "products.csv"):
        """Initialize the ProductFilter with product data from CSV."""
        self.df = pd.read_csv(csv_path)
        
    def load_products(self) -> pd.DataFrame:
        """Load and return all products."""
        return self.df.copy()
    
    def filter_products(self, criteria: Dict[str, Any]) -> pd.DataFrame:
        """
        Filter products based on given criteria.
        
        Args:
            criteria: Dictionary containing filter criteria
                     - category: str
                     - color: str 
                     - price_max: float
                     - price_min: float
                     - rating_min: float
                     
        Returns:
            Filtered DataFrame
        """
        filtered_df = self.df.copy()
        
        # Filter by category
        if criteria.get('category'):
            category = criteria['category'].lower()
            filtered_df = filtered_df[filtered_df['category'].str.lower().str.contains(category, na=False)]
        
        # Filter by color
        if criteria.get('color'):
            color = criteria['color'].lower()
            filtered_df = filtered_df[filtered_df['color'].str.lower().str.contains(color, na=False)]
        
        # Filter by price range
        if criteria.get('price_max'):
            filtered_df = filtered_df[filtered_df['price'] <= criteria['price_max']]
            
        if criteria.get('price_min'):
            filtered_df = filtered_df[filtered_df['price'] >= criteria['price_min']]
        
        # Filter by minimum rating
        if criteria.get('rating_min'):
            filtered_df = filtered_df[filtered_df['rating'] >= criteria['rating_min']]
        
        # Sort by rating (highest first) and then by price (lowest first)
        filtered_df = filtered_df.sort_values(['rating', 'price'], ascending=[False, True])
        
        return filtered_df
    
    def get_product_stats(self) -> Dict[str, Any]:
        """Get basic statistics about the product inventory."""
        return {
            'total_products': len(self.df),
            'categories': self.df['category'].unique().tolist(),
            'colors': self.df['color'].unique().tolist(),
            'price_range': {
                'min': self.df['price'].min(),
                'max': self.df['price'].max(),
                'avg': self.df['price'].mean()
            },
            'avg_rating': self.df['rating'].mean()
        }


def generate_recommendation_explanation(filtered_products: pd.DataFrame, 
                                      original_criteria: Dict[str, Any]) -> str:
    """
    Generate a brief explanation for the recommendations.
    
    Args:
        filtered_products: DataFrame of filtered products
        original_criteria: The original search criteria
        
    Returns:
        Explanation string
    """
    if len(filtered_products) == 0:
        return "No products found matching your criteria. Try adjusting your search terms."
    
    explanation_parts = []
    
    # Mention the number of results
    count = len(filtered_products)
    explanation_parts.append(f"Found {count} item{'s' if count != 1 else ''}")
    
    # Mention criteria that were applied
    criteria_mentioned = []
    if original_criteria.get('category'):
        criteria_mentioned.append(f"in {original_criteria['category']}")
    if original_criteria.get('color'):
        criteria_mentioned.append(f"in {original_criteria['color']}")
    if original_criteria.get('price_max'):
        criteria_mentioned.append(f"under ${original_criteria['price_max']}")
    if original_criteria.get('rating_min'):
        criteria_mentioned.append(f"with rating ≥ {original_criteria['rating_min']}")
    
    if criteria_mentioned:
        explanation_parts.append(" ".join(criteria_mentioned))
    
    # Add quality note
    avg_rating = filtered_products['rating'].mean()
    if avg_rating >= 4.5:
        explanation_parts.append("• All items have excellent ratings")
    elif avg_rating >= 4.0:
        explanation_parts.append("• Items have good to excellent ratings")
    
    # Add price insight
    if len(filtered_products) > 1:
        price_range = f"${filtered_products['price'].min():.2f} - ${filtered_products['price'].max():.2f}"
        explanation_parts.append(f"• Price range: {price_range}")
    
    return ". ".join(explanation_parts) + "." 