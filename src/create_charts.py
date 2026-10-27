import plotly.express as px
import pandas as pd
from pathlib import Path


def create_steps_chart(df: pd.DataFrame):
    """Create an interactive chart of daily steps."""

    chart_data = df.dropna(subset=["date", "steps"]).copy()
    chart_data = chart_data.sort_values("date")

    fig = px.line(
        chart_data,
        x="date",
        y="steps",
        width=700,
        height=400,
        markers=True,
        title="Antal steg per dag",
        labels={
            "date": "Datum",
            "steps": "Antal steg",
        },
    )

    fig.add_hline(
        y=10000,
        line_dash="dash",
        annotation_text="10 000 steg",
    )
    fig.add_hline(
        y=0,
        line_dash="dash",
        annotation_text="0 steg",
    )

    fig.update_layout(
        template="plotly_white",
        xaxis_title="Datum",
        yaxis_title="Steg",
    )

    # Export as svg and html
    fig_path_svg = (Path(__file__).parent.parent
        / "reports"
        / "svg"
    )
    fig_path_html = (Path(__file__).parent.parent
        / "reports"
        / "html"
    )
    fig_path_svg.mkdir(parents=True, exist_ok=True)
    fig_path_html.mkdir(parents=True, exist_ok=True)
    fig_path_svg = (Path(fig_path_svg) / "steps_chart.svg")
    fig_path_html = (Path(fig_path_html) / "steps_chart.html")

    fig.write_image(
        fig_path_svg,
        format="svg",
        width=700,
        height=400,
    )

    fig.write_html(
        fig_path_html,
        include_plotlyjs=True
    )

    return fig