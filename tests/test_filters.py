import unittest
import pandas as pd
import sys
import os

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from inventory.filters import ProductFilter, generate_recommendation_explanation


class TestProductFilter(unittest.TestCase):
    
    def setUp(self):
        """Set up test data."""
        # Create a sample DataFrame for testing
        self.test_data = pd.DataFrame({
            'name': ['Red Dress', 'Blue Jeans', 'Black Jacket'],
            'category': ['dress', 'jeans', 'jacket'],
            'color': ['red', 'blue', 'black'],
            'price': [150.0, 89.99, 299.99],
            'rating': [4.5, 4.2, 4.8],
            'image_url': ['url1', 'url2', 'url3'],
            'description': ['desc1', 'desc2', 'desc3']
        })
        
        # Create a ProductFilter instance with test data
        self.filter = ProductFilter()
        self.filter.df = self.test_data
    
    def test_filter_by_category(self):
        """Test filtering by category."""
        criteria = {'category': 'dress'}
        result = self.filter.filter_products(criteria)
        self.assertEqual(len(result), 1)
        self.assertEqual(result.iloc[0]['name'], 'Red Dress')
    
    def test_filter_by_color(self):
        """Test filtering by color."""
        criteria = {'color': 'blue'}
        result = self.filter.filter_products(criteria)
        self.assertEqual(len(result), 1)
        self.assertEqual(result.iloc[0]['name'], 'Blue Jeans')
    
    def test_filter_by_price_max(self):
        """Test filtering by maximum price."""
        criteria = {'price_max': 200.0}
        result = self.filter.filter_products(criteria)
        self.assertEqual(len(result), 2)  # Red Dress and Blue Jeans
    
    def test_filter_by_price_min(self):
        """Test filtering by minimum price."""
        criteria = {'price_min': 100.0}
        result = self.filter.filter_products(criteria)
        self.assertEqual(len(result), 2)  # Red Dress and Black Jacket
    
    def test_filter_by_rating(self):
        """Test filtering by minimum rating."""
        criteria = {'rating_min': 4.5}
        result = self.filter.filter_products(criteria)
        self.assertEqual(len(result), 2)  # Red Dress and Black Jacket
    
    def test_combined_filters(self):
        """Test combining multiple filters."""
        criteria = {
            'price_max': 200.0,
            'rating_min': 4.3
        }
        result = self.filter.filter_products(criteria)
        self.assertEqual(len(result), 1)  # Only Red Dress
    
    def test_no_results(self):
        """Test case with no matching results."""
        criteria = {
            'category': 'shoes',
            'color': 'purple'
        }
        result = self.filter.filter_products(criteria)
        self.assertEqual(len(result), 0)
    
    def test_get_product_stats(self):
        """Test getting product statistics."""
        stats = self.filter.get_product_stats()
        self.assertEqual(stats['total_products'], 3)
        self.assertIn('dress', stats['categories'])
        self.assertIn('red', stats['colors'])
        self.assertEqual(stats['price_range']['min'], 89.99)
        self.assertEqual(stats['price_range']['max'], 299.99)


class TestRecommendationExplanation(unittest.TestCase):
    
    def setUp(self):
        """Set up test data."""
        self.test_products = pd.DataFrame({
            'name': ['Red Dress', 'Blue Jeans'],
            'price': [150.0, 89.99],
            'rating': [4.5, 4.2]
        })
    
    def test_explanation_with_results(self):
        """Test explanation generation with results."""
        criteria = {'category': 'dress', 'color': 'red', 'price_max': 200}
        explanation = generate_recommendation_explanation(self.test_products, criteria)
        
        self.assertIn('Found 2 items', explanation)
        self.assertIn('in dress', explanation)
        self.assertIn('in red', explanation)
        self.assertIn('under $200', explanation)
    
    def test_explanation_no_results(self):
        """Test explanation generation with no results."""
        empty_df = pd.DataFrame()
        criteria = {'category': 'shoes'}
        explanation = generate_recommendation_explanation(empty_df, criteria)
        
        self.assertIn('No products found', explanation)
    
    def test_explanation_single_result(self):
        """Test explanation generation with single result."""
        single_product = self.test_products.iloc[:1]
        criteria = {'category': 'dress'}
        explanation = generate_recommendation_explanation(single_product, criteria)
        
        self.assertIn('Found 1 item', explanation)
        self.assertNotIn('Found 1 items', explanation)  # Check singular form


if __name__ == '__main__':
    unittest.main() 