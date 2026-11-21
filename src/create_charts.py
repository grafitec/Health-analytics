import plotly.express as px
import pandas as pd
from pathlib import Path


def create_steps_chart(df: pd.DataFrame, points_data):
    """Create an interactive chart of daily steps."""

    # Gruppera på datum och säg till om det saknas steg i någon dag

    steps_row = points_data[points_data['activity'] == 'steps']
    steps_goal = steps_row['goal'][1]
    step_points = steps_row['point_at_100'][1]
    step_total = df['steps'].sum()
    step_goal_total = len(df[df['steps'].notna()]) * 10000
    step_procent = round((step_total / step_goal_total) * 100, 1)
    print('Steg i procent: ', step_procent)
    step_total_points = round((step_points * step_procent) / 100, 1)
    print('Steg poäng: ', step_total_points)


    chart_data = df.dropna(subset=["date", "steps"]).copy()
    chart_data = chart_data.sort_values("date")

    fig = px.line(
        chart_data,
        x="date",
        y="steps",
        width=340,
        height=230,
        markers=True,
    )
    fig.update_traces(
        line=dict(
            shape="spline",
            smoothing=0.5,
            width=3
        ),
        marker=dict(
            size=10
        )
    )
    fig.update_xaxes(showgrid=False)
    fig.update_yaxes(showgrid=False)
    fig.update_xaxes(title_text="")
    fig.update_yaxes(title_text="")
    fig.update_xaxes(tickformat="%b %-d")
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        template="plotly_white",
        font=dict(
            color="#174B70",
            family="Arial",
            size=18
        ),
    )

    fig.add_hline(
        y=steps_goal,
        line_dash="dash",
        annotation_text="10 000 steg",
    )
    fig.add_hline(
        y=0,
        line_dash="dash",
        annotation_text="0 steg",
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