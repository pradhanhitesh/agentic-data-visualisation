# Agentic Data Visualization

Transform your raw datasets into meaningful visual stories with the power of AI agents. Agentic Data Visualization is an intelligent platform designed to automatically analyze, profile, and visualize data, uncovering hidden patterns with zero friction.

![Agentic Data Visualization](https://img.shields.io/badge/Status-Active-brightgreen)
![Python](https://img.shields.io/badge/Backend-Python%203.14-blue)
![Vue](https://img.shields.io/badge/Frontend-Vue.js%203-4fc08d)
![Polars](https://img.shields.io/badge/Data-Polars-ff69b4)

## Key Features

- **Automated Data Profiling**: Instantly understand the structure, types, and quality of your dataset.
- **AI-Driven Insights**: Advanced agents analyze your data to provide deep, textual analytical insights in Markdown format.
- **Dynamic Plot Generation**: Automatically creates professional-grade visualizations (scatter plots, histograms, etc.) tailored to your data.
- **PDF Report Export**: Export your entire analysis, including all insights and charts, into a beautifully formatted PDF report.
- **Local Persistence**: Your session history is stored locally in your browser, giving you full control and privacy.
- **Zero Friction**: No accounts or sign-ups required. Just upload and visualize.

## Technology Stack

### Backend
- **Core**: [Python 3.14+](https://www.python.org/)
- **API Framework**: [Flask](https://flask.palletsprojects.com/)
- **Data Engine**: [Polars](https://pola.rs/) (High-performance DataFrame library)
- **Rate Limiting**: [Flask-Limiter](https://flask-limiter.readthedocs.io/)
- **Report Generation**: [ReportLab](https://www.reportlab.com/)

### Frontend
- **Framework**: [Vue.js 3](https://vuejs.org/) (Composition API)
- **Routing**: [Vue Router](https://router.vuejs.org/)
- **Styling**: Modern CSS with Glassmorphism and Responsive Design
- **Icons**: [Bootstrap Icons](https://icons.getbootstrap.com/)
- **Notifications**: [Vue-Toastification](https://vue-toastification.maronato.dev/)

## Usage

1. **Upload**: Drag and drop or click to upload your `.csv` or `.xlsx` file.
2. **Analyze**: Wait a few seconds for the agents to profile your data and generate plans.
3. **Visualize**: Explore the generated insights and plots on the results page.
4. **Export**: Click the download button to get a comprehensive PDF report of your analysis.
5. **History**: Use the sidebar to quickly access your previous analyses.


## Future updates

- **Multi-Agent Reasoning**: Collaborative agent swarms for deep analytical reasoning.
- **Interactive Visualizations**: Integration of Plotly/D3 for interactive 3D and dynamic charts.
- **Statistical Testing**: Automated hypothesis testing and statistical validation (t-tests, ANOVA, etc.).
- **Expanded File Support**: Native support for SQL databases, JSON, and Parquet.
- **Enhanced Rate Limits**: Implementation of tiered access or higher hourly limits.

## Limitations

- **Rate Limit**: To ensure fair usage, the system allows **5 uploads per hour**.
- **File Types**: Currently supports `.csv` and `.xlsx` files only.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

---

Created with ❤️ by [Hitesh Pradhan](https://github.com/pradhanhitesh)
