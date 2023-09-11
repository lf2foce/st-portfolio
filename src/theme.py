from st_pages import Page, show_pages, add_page_title

show_pages(
            [
                Page("streamlit_app.py", "So sánh", "📊"),
                Page("pages/1_info.py", "Dự đoán", "🎯"),
                Page("pages/2_optimizer.py", "Tối ưu danh mục", "🎮"),
            ]
        )