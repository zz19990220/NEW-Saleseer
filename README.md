# 🛍️ AI Product Recommendation System

A simple AI-powered product recommendation website built with Python and Streamlit. Users can search for products using natural language queries, and the system uses OpenAI's GPT model to parse the intent and filter products accordingly.

## ✨ Features

- **Natural Language Search**: Query products using everyday language like "Show me red dresses under $200"
- **AI-Powered Parsing**: Uses OpenRouter API with GPT models to understand user intent and extract search criteria
- **Smart Filtering**: Filters products by category, color, price range, and ratings
- **Visual Product Display**: Clean, card-based product listings with images and details
- **Search History**: Keeps track of recent searches for easy access
- **Responsive Design**: Modern, mobile-friendly interface

## 🏗️ Project Structure

```
ai-product-recommendations/
├── app.py                 # Main Streamlit application
├── inventory/             # Inventory management
│   └── filters.py        # Product filtering logic
├── llm/                  # LLM integration
│   └── handler.py        # OpenAI API handler
├── tests/                # Unit tests
│   └── test_filters.py   # Filter functionality tests
├── products.csv          # Sample product inventory
├── requirements.txt      # Python dependencies
├── .env.example         # Environment variables template
└── README.md            # This file
```

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- OpenRouter API key ([Get one here](https://openrouter.ai/keys))

### Installation

1. **Clone or download the project**
   ```bash
   cd your_project_directory
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**
   ```bash
   cp .env.example .env
   ```
   Edit `.env` and add your OpenRouter API key:
   ```
   OPENROUTER_API_KEY=sk-or-v1-your_actual_api_key_here
   ```

4. **Run the application**
   ```bash
   streamlit run app.py
   ```

5. **Open your browser**
   The app will automatically open at `http://localhost:8501`

## 💡 Usage Examples

Try these natural language queries:

- "Show me red dresses under $200"
- "I want blue jeans"
- "Find black jackets with good ratings"
- "Something cheap for summer"
- "Purple evening wear"
- "Comfortable shoes under $150"

## 🎯 How It Works

1. **User Input**: User enters a natural language query
2. **AI Parsing**: OpenRouter API (using GPT models) parses the query to extract:
   - Product category (dress, jeans, shoes, etc.)
   - Color preference
   - Price range (min/max)
   - Rating requirements
3. **Filtering**: Products are filtered based on extracted criteria
4. **Display**: Matching products are shown with explanations

## 📊 Sample Data

The project includes a sample CSV file (`products.csv`) with 15 clothing items including:
- Dresses, jeans, jackets, shoes, and more
- Various colors and price ranges
- Customer ratings and descriptions
- Placeholder images for demonstration

### Adding Your Own Products

Simply edit `products.csv` with your own product data. Required columns:
- `name`: Product name
- `category`: Product category
- `color`: Primary color
- `price`: Price (numeric)
- `rating`: Customer rating (1-5)
- `image_url`: Product image URL
- `description`: Product description

## 🧪 Testing

Run the unit tests to ensure everything works correctly:

```bash
python -m pytest tests/test_filters.py -v
```

Or using unittest:
```bash
python tests/test_filters.py
```

## 🔧 Configuration

### Environment Variables

- `OPENROUTER_API_KEY`: Your OpenRouter API key (required)

### Customization

- **Product Data**: Modify `products.csv` to use your own inventory
- **LLM Model**: Change the model in `llm/handler.py` (default: gpt-3.5-turbo)
- **Filtering Logic**: Customize filtering rules in `inventory/filters.py`
- **UI Styling**: Modify CSS in `app.py` for custom appearance

## 📈 Features in Detail

### Natural Language Processing
- Handles various query formats and synonyms
- Extracts multiple criteria from single queries
- Fallback parsing when API is unavailable

### Smart Filtering
- Flexible category matching
- Color variations and partial matches
- Price range filtering
- Rating-based recommendations
- Results sorted by rating and price

### User Experience
- Clean, modern interface
- Product cards with images and details
- Search history for quick access
- Inventory overview in sidebar
- Helpful error messages and suggestions

## 🛠️ Development

### Adding New Features

1. **New Filter Criteria**: Add to `ProductFilter.filter_products()` in `inventory/filters.py`
2. **Enhanced AI Parsing**: Modify prompts in `llm/handler.py`
3. **UI Improvements**: Update styling and layout in `app.py`

### Dependencies

- `streamlit`: Web app framework
- `openai`: OpenAI API client
- `pandas`: Data manipulation
- `python-dotenv`: Environment variable management
- `openpyxl`: Excel file support

## ⚠️ Important Notes

- Requires active internet connection for OpenRouter API calls
- API calls incur costs based on OpenRouter pricing (often cheaper than OpenAI direct)
- Fallback parsing available when API is unavailable
- Sample images use placeholder service (replace with actual product images)

## 🤝 Contributing

Feel free to enhance this project by:
- Adding more sophisticated AI parsing
- Implementing additional filter criteria
- Improving the user interface
- Adding product recommendations based on user behavior
- Integrating with real e-commerce APIs

## 📝 License

This project is open source and available for educational and commercial use.

---

**Happy Shopping! 🛍️** 