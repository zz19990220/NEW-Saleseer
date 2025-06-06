import streamlit as st
import pandas as pd
import os
from llm.handler import LLMHandler
from inventory.filters import ProductFilter, generate_recommendation_explanation

# Page configuration
st.set_page_config(
    page_title="Saleseer AI Product Recommendations",
    page_icon="🛍️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .product-card {
        border: 1px solid #ddd;
        border-radius: 10px;
        padding: 15px;
        margin: 10px 0;
        background-color: #f9f9f9;
    }
    .product-image {
        width: 100%;
        height: 200px;
        object-fit: cover;
        border-radius: 8px;
    }
    .price-tag {
        font-size: 1.2em;
        font-weight: bold;
        color: #e74c3c;
    }
    .rating {
        color: #f39c12;
    }
    .search-summary {
        background-color: #e8f4fd;
        padding: 10px;
        border-radius: 5px;
        border-left: 4px solid #3498db;
        margin: 10px 0;
    }
    .recommendation-explanation {
        background-color: #e8f5e8;
        padding: 10px;
        border-radius: 5px;
        border-left: 4px solid #27ae60;
        margin: 15px 0;
    }
</style>
""", unsafe_allow_html=True)

def init_session_state():
    """Initialize session state variables."""
    if 'search_history' not in st.session_state:
        st.session_state.search_history = []
    if 'last_results' not in st.session_state:
        st.session_state.last_results = None

def display_product_card(product_row):
    """Display a single product in a card format."""
    with st.container():
        col1, col2 = st.columns([1, 2])
        
        with col1:
            st.image(product_row['image_url'], use_column_width=True)
        
        with col2:
            st.subheader(product_row['name'])
            st.markdown(f"**Category:** {product_row['category'].title()}")
            st.markdown(f"**Color:** {product_row['color'].title()}")
            st.markdown(f"<span class='price-tag'>${product_row['price']:.2f}</span>", unsafe_allow_html=True)
            
            # Rating with stars
            stars = "⭐" * int(product_row['rating'])
            st.markdown(f"<span class='rating'>{stars} ({product_row['rating']}/5)</span>", unsafe_allow_html=True)
            
            st.markdown(f"*{product_row['description']}*")
        
        st.markdown("---")

def main():
    # Initialize session state
    init_session_state()
    
    # Header
    st.title("🛍️ Saleseer AI Product Recommendations")
    st.markdown("### Find products using natural language!")
    st.markdown("*Try queries like: 'Show me red dresses under $200' or 'I want blue jeans'*")
    
    # Check if OpenRouter API key is set
    if not os.getenv('OPENROUTER_API_KEY'):
        st.error("⚠️ OpenRouter API key not found! Please set your OPENROUTER_API_KEY in the .env file.")
        st.info("1. Copy `.env.example` to `.env`\n2. Add your OpenRouter API key to the `.env` file")
        return
    
    # Initialize components
    try:
        llm_handler = LLMHandler()
        product_filter = ProductFilter()
    except Exception as e:
        st.error(f"Error initializing components: {e}")
        return
    
    # Sidebar with inventory stats
    with st.sidebar:
        st.header("📊 Inventory Overview")
        try:
            stats = product_filter.get_product_stats()
            st.metric("Total Products", stats['total_products'])
            st.metric("Average Rating", f"{stats['avg_rating']:.1f}/5")
            st.metric("Price Range", f"${stats['price_range']['min']:.0f} - ${stats['price_range']['max']:.0f}")
            
            st.subheader("Available Categories")
            for category in sorted(stats['categories']):
                st.write(f"• {category.title()}")
            
            st.subheader("Available Colors")
            for color in sorted(stats['colors']):
                st.write(f"• {color.title()}")
                
        except Exception as e:
            st.error(f"Error loading inventory stats: {e}")
    
    # Main search interface
    st.header("🔍 Search Products")
    
    # Search input
    user_query = st.text_input(
        "What are you looking for?",
        placeholder="e.g., Show me red dresses under $200",
        help="Describe what you're looking for in natural language"
    )
    
    # Search button
    if st.button("🔍 Search", type="primary") or user_query:
        if user_query.strip():
            with st.spinner("🤖 Understanding your request and finding products..."):
                try:
                    # Parse the query using LLM
                    criteria = llm_handler.parse_query(user_query)
                    
                    # Generate search summary
                    search_summary = llm_handler.generate_search_summary(criteria, user_query)
                    st.markdown(f"""
                    <div class='search-summary'>
                        <strong>🎯 {search_summary}</strong>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Filter products
                    filtered_products = product_filter.filter_products(criteria)
                    
                    # Store results in session state
                    st.session_state.last_results = {
                        'query': user_query,
                        'criteria': criteria,
                        'products': filtered_products
                    }
                    
                    # Add to search history
                    if user_query not in st.session_state.search_history:
                        st.session_state.search_history.insert(0, user_query)
                        if len(st.session_state.search_history) > 5:
                            st.session_state.search_history = st.session_state.search_history[:5]
                    
                except Exception as e:
                    st.error(f"Error processing your request: {e}")
                    return
    
    # Display results
    if st.session_state.last_results:
        results = st.session_state.last_results
        filtered_products = results['products']
        
        # Generate and display explanation
        explanation = generate_recommendation_explanation(filtered_products, results['criteria'])
        st.markdown(f"""
        <div class='recommendation-explanation'>
            <strong>💡 Recommendation Insight:</strong><br>
            {explanation}
        </div>
        """, unsafe_allow_html=True)
        
        # Display products
        if len(filtered_products) > 0:
            st.header(f"🎯 Found {len(filtered_products)} Product{'s' if len(filtered_products) != 1 else ''}")
            
            # Display products
            for idx, (_, product) in enumerate(filtered_products.iterrows()):
                display_product_card(product)
                
            # Show more details in expandable section
            with st.expander("📋 View Detailed Results Table"):
                st.dataframe(
                    filtered_products[['name', 'category', 'color', 'price', 'rating', 'description']],
                    use_container_width=True
                )
        else:
            st.warning("😔 No products found matching your criteria. Try adjusting your search terms.")
            
            # Suggest alternatives
            st.subheader("💡 Suggestions:")
            st.write("- Try broader search terms")
            st.write("- Check the available categories and colors in the sidebar")
            st.write("- Adjust your price range")
    
    # Search history
    if st.session_state.search_history:
        st.header("🕒 Recent Searches")
        for i, query in enumerate(st.session_state.search_history):
            if st.button(f"🔄 {query}", key=f"history_{i}"):
                st.experimental_rerun()

if __name__ == "__main__":
    main() 