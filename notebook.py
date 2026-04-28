# /// script
# requires-python = ">=3.13"
# dependencies = [
#     "ipython==9.12.0",
#     "marimo>=0.22.4",
#     "numpy==2.4.4",
#     "pandas==3.0.2",
# ]
# ///

import marimo

__generated_with = "0.23.0"
app = marimo.App(
    width="medium",
    css_file="/usr/local/_marimo/custom.css",
    auto_download=["html"],
)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Libraries
    """)
    return

@app.cell
def _():
    import marimo as mo
    import math

    import pandas as pd
    import numpy as np

    from svg import SVG, Rect, Circle, Line, Text

    return (
        Circle,
        Line,
        Rect,
        SVG,
        Text,
        math,
        mo,
        np,
        pd,
    )

@app.cell
def _(pd):
    data_soil = pd.read_csv("oumalik_soil_data.csv", sep=";")
    return (data_soil,)


@app.cell
def _(pd):
    data_rest = pd.read_csv("oumalik_environmental_data.csv", sep=";")
    return (data_rest,)


@app.cell
def _(data_soil):
    soil_columns = data_soil[['community','pH','sand','silt','clay']]
    return (soil_columns,)


@app.cell
def _(np, soil_columns):
    soil_columns[['sand','silt','clay']] = soil_columns[['sand','silt','clay']].replace(-9999, np.nan)
    return


@app.cell
def _(soil_columns):
    silt_dict = dict(zip(soil_columns['community'], soil_columns['silt']))
    clay_dict = dict(zip(soil_columns['community'], soil_columns['clay']))
    sand_dict = dict(zip(soil_columns['community'], soil_columns['sand']))
    ph_dict = dict(zip(soil_columns['community'], soil_columns['pH']))
    return clay_dict, ph_dict, sand_dict, silt_dict


@app.cell
def _(data_rest, np):
    rest_columns = data_rest[['community', 'cover_total', 'thaw_depth ', 'site_moisture ', 'disturbance_score']].replace(-9999, np.nan)
    return (rest_columns,)


@app.cell
def _(rest_columns):
    rest_mean = rest_columns.groupby('community').mean().reset_index()
    return (rest_mean,)


@app.cell
def _(rest_mean):
    cover_total_dict = dict(zip(rest_mean['community'], 
                                rest_mean['cover_total']))
    thaw_depth_dict = dict(zip(rest_mean['community'], 
                               rest_mean['thaw_depth ']))
    site_moisture_dict = dict(zip(rest_mean['community'], 
                                  rest_mean['site_moisture ']))
    disturbance_score_dict = dict(zip(rest_mean['community'],
                                      rest_mean['disturbance_score']))
    return disturbance_score_dict, site_moisture_dict, thaw_depth_dict


@app.cell
def _(mo):
    community_selector = mo.ui.dropdown(
        options=[str(i) for i in range(2, 37)], 
        value="2", 
        label="Choose community 1"
    )

    community_selector_2 = mo.ui.dropdown(
        options=[str(i) for i in range(2, 37)], 
        value="3",
        label="Choose community 2"
    )

    mo.hstack([community_selector, community_selector_2], gap=2)
    return community_selector, community_selector_2


@app.cell
def _(
    Circle,
    Line,
    Rect,
    SVG,
    Text,
    clay_dict,
    community_selector,
    community_selector_2,
    disturbance_score_dict,
    math,
    mo,
    pd,
    ph_dict,
    sand_dict,
    silt_dict,
    site_moisture_dict,
    thaw_depth_dict,
):
    selected_comm_1 = int(community_selector.value)

    if community_selector_2.value is not None and not pd.isna(community_selector_2.value):
        selected_comm_2 = int(community_selector_2.value)
    else:
        selected_comm_2 = None

    data_dicts = {
        'silt': silt_dict,
        'clay': clay_dict,
        'sand': sand_dict,
        'moist': site_moisture_dict,
        'thaw': thaw_depth_dict,
        'dist': disturbance_score_dict,
        'ph': ph_dict
    }

    def get_comm_data(comm_id, dicts):
        if comm_id is None: return None
        return {k: d.get(comm_id, 0) for k, d in dicts.items()}

    data_1 = get_comm_data(selected_comm_1, data_dicts)
    data_2 = get_comm_data(selected_comm_2, data_dicts)

    _elements = []

    soil_start_y = 340
    skala = 2.5

    # pH COLOR PALETTE
    def get_ph_color(ph):
        if pd.isna(ph):
            return "white"
        ph_min = 4.0
        ph_max = 8.1
        norm = (ph - ph_min) / (ph_max - ph_min)
        norm = max(0, min(1, norm))
        if norm < 0.5:
            local_norm = norm * 2
            r = int(243 - (local_norm * 243))
            g = int(255 - (local_norm * 131))
            b = int(130 + (local_norm * 16))
        else:
            local_norm = (norm - 0.5) * 2
            r = int(0 + (local_norm * 30))
            g = int(124 - (local_norm * 59))
            b = int(146 - (local_norm * 50))
        return f"rgb({r}, {g}, {b})"

    # STARTING POINT
    def draw_complete_plant(elements_list, data, base_x, start_y, plot_scale):
        if data is None: return

        def fmt(val):
            return "?" if pd.isna(val) else str(round(val, 1) if isinstance(val, float) else val)

        tooltip_text = (
            f"<title>"
            f"pH: {fmt(data['ph'])}&#10;"
            f"Moisture: {fmt(data['moist'])}&#10;"
            f"Thaw Depth: {fmt(data['thaw'])}&#10;"
            f"Disturbance: {fmt(data['dist'])}&#10;"
            f"Silt: {fmt(data['silt'])}&#10;"
            f"Clay: {fmt(data['clay'])}&#10;"
            f"Sand: {fmt(data['sand'])}"
            f"</title>"
        )
        elements_list.append(f"<g>{tooltip_text}")

        local_current_y = start_y
        soil_width = 120
        soil_x = base_x - (soil_width / 2)
        total_soil_height = 100 * plot_scale
        moist_width = 20
        moist_x = base_x - (moist_width / 2)
        promien_srodka = 22
        promien_platka = 10

        # SILT, CLAY, SAND
        v_silt = data['silt'] if not pd.isna(data['silt']) else 0
        v_clay = data['clay'] if not pd.isna(data['clay']) else 0
        v_sand = data['sand'] if not pd.isna(data['sand']) else 0
        suma_gleby = v_silt + v_clay + v_sand

        if suma_gleby > 0:
            for val, cls in [(v_silt, 'silt'), (v_clay, 'clay'), (v_sand, 'sand')]:
                if val > 0:
                    h = (val / suma_gleby) * total_soil_height
                    elements_list.append(Rect(x=soil_x, y=local_current_y, width=soil_width, height=h, class_=cls))
                    local_current_y += h
        else:
            h = total_soil_height / 3
            for _ in range(3):
                elements_list.append(Rect(x=soil_x, y=local_current_y, width=soil_width, height=h, 
                                          stroke="gray", stroke_width="1", stroke_dasharray="5,5", fill="white"))
                local_current_y += h

        # MOIST
        if not pd.isna(data['moist']):
            moist_h = max((data['moist'] - 1) * 25, 10)
            y_start_moist = start_y - moist_h
            elements_list.append(Rect(x=moist_x, y=y_start_moist, width=moist_width, 
                                      height=moist_h, stroke="black", stroke_width="2", class_='moist'))

            for i in range(1, int(data['moist']) + 1):
                line_y = start_y - (i * 25)
                if line_y > y_start_moist:
                    elements_list.append(Line(x1=moist_x, y1=line_y, x2=moist_x + moist_width, 
                                              y2=line_y, stroke="black", stroke_width="2"))
        else:
            moist_h = 5 * 20
            y_start_moist = start_y - moist_h
            elements_list.append(Rect(x=moist_x, y=y_start_moist, width=moist_width, 
                                      height=moist_h, stroke="gray", stroke_width="2", stroke_dasharray="5,5", fill="white"))

        # FLOWER pH
        srodek_y = y_start_moist - promien_srodka

        ph_fill_color = get_ph_color(data['ph'])
        stroke_style = "5,5" if pd.isna(data['ph']) else "0"
        elements_list.append(
            Circle(cx=base_x, cy=srodek_y, r=promien_srodka, 
                   fill=ph_fill_color, stroke="black", 
                   stroke_width="2", stroke_dasharray=stroke_style, class_='ph')
        )

        # GRADIENT
        if pd.isna(data['ph']):
            ph_fill_grad = "white"
            stroke_style_grad = "5,5"
        else:
            ph_fill_grad = "url(#phGradient)" 
            stroke_style_grad = "0"

        elements_list.append(
            Circle(cx=base_x, cy=srodek_y, r=promien_srodka, 
                   fill=ph_fill_grad, stroke_dasharray=stroke_style_grad,
                   stroke_width="2", class_='ph')
        )

        # DISTURBANCE SCORE
        if not pd.isna(data['dist']):
            dist_val = int(data['dist'])
            ilosc_kolek = max(0, 12 - dist_val)
            odleglosc_od_srodka = promien_srodka + promien_platka
            for i in range(ilosc_kolek):
                kat_radiany = math.radians(i * 30)
                px = base_x + odleglosc_od_srodka * math.sin(kat_radiany)
                py = srodek_y - odleglosc_od_srodka * math.cos(kat_radiany)
                elements_list.append(Circle(cx=px, cy=py, r=promien_platka, stroke="black", stroke_width="2", class_='disturbance'))

        # THAW DEPTH
        if not pd.isna(data['thaw']) and data['thaw'] > 0:
            thaw_len = data['thaw'] * 3.15
            end_y = start_y + thaw_len
            elements_list.append(Line(x1=moist_x, y1=start_y, x2=moist_x - 15, y2=end_y, stroke="black", stroke_width="2"))
            elements_list.append(Line(x1=base_x, y1=start_y, x2=base_x, y2=end_y * 0.95, stroke="black", stroke_width="2"))
            elements_list.append(Line(x1=moist_x + moist_width, y1=start_y, x2=moist_x + moist_width + 15, y2=end_y, stroke="black", stroke_width="2"))

        elements_list.append("</g>")

    draw_complete_plant(_elements, data_1, base_x=100, start_y=soil_start_y, plot_scale=skala)
    draw_complete_plant(_elements, data_2, base_x=400, start_y=soil_start_y, plot_scale=skala)

    legend_y = 650 
    legend_x = 100
    rect_w = 40 

    _elements.append(Text(text="pH Scale", x=legend_x, y=legend_y - 10, font_size="14px", font_weight="bold", fill="black"))

    palette_rgb = [
        (243, 255, 130), (171, 235, 136), (103, 210, 148), (23,  183, 156),
        (0,   154, 156), (0,   124, 146), (0,   94,  125), (31,  66,   96)
    ]
    ph_labels = ["4.0", "4.6", "5.2", "5.8", "6.3", "6.9", "7.5", "8.1"]

    for i, color in enumerate(palette_rgb):
        c_str = f"rgb({color[0]}, {color[1]}, {color[2]})"
        cur_x = legend_x + (i * rect_w)

        _elements.append(Rect(x=cur_x, y=legend_y, width=rect_w, height=20, fill=c_str, stroke="black", stroke_width="1"))
        _elements.append(Text(text=ph_labels[i], x=cur_x + 8, y=legend_y + 35, font_size="12px", fill="black"))


    comp_svg_width = 500 
    comp_svg_height = 700

    _svg = SVG(width=comp_svg_width, height=comp_svg_height, class_="notebook", elements=_elements)
    mo.Html(_svg.as_str())
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <style>
        svg.notebook {
            border: 1px solid
        }

        rect.silt {
            fill: #A5907E;
        }
        rect.clay {
            fill: #AC8076;
        }
        rect.sand {
            fill: #cbbd93;
        }

        rect.moist {
            fill: #858F79;
        }

        circle.disturbance {
            fill: #F5EFF8;
        }

    </style>
    """)
    return
