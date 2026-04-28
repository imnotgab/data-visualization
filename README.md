# Soil Analysis - Oumalik

This project focuses on visualizing environmental, soil, and vegetation data collected between 1983 and 1985 from 87 study plots near an abandoned test oil well in Oumalik, Alaska. The test site was constructed and abandoned around 1949–1950, causing significant anthropogenic disturbance to the tundra through heavy machinery and abandoned debris.

## Data Source
The original data used in this project (`.csv` files) was compiled based on documentation from the Oumalik region. 
The full report and methodology are available here: 
[Oumalik_Veg_plots.pdf](https://d3o6w55j8uz1ro.cloudfront.net/s3-d0f68fa49c8cba12794bb586349f2341/ornl-cumulus-prod-public.s3.us-west-2.amazonaws.com/above/Oumalik_Veg_plots/comp/Oumalik_Veg_plots.pdf?A-userid=None&Expires=1777395242&Signature=TH~8r6Y-kUQAiWZy1R2NaT1XDtFP1z7a3rcT0TX8-OhaVNwIRXc0SJ0H5amg9kshpinxtllJo-5nRBV6cj4uDhmgBu41L7rQGvznt72aHxLaFLu~~Sks3R38kYGpSXlA-if94jhAGRlvX6ekZXvCAYMAudggNdAMdj~PZ81f4F2IlHc2r06XhzRvRWV-MLXd4ehJFlsgzd~6dqpJJXxBX1Zl2TamD0ORqSHzBXB-iNWz530tKC1ieoUaYJlAhfZAkGmlFO321i31zX2OV2SvXPGuBSAN6H2v6Wiur2yV1xYgtzeB-sla6KdvnEOc7g2p6tZ7v9nKpzH9U5su2Ixxxg__&Key-Pair-Id=K2GHMOM2YD9MI1)

## The Dataset
The dataset consists of three main components:
* **Environmental Data:** Captures plant community types, geographical coordinates, physical site characteristics (e.g., thaw depth, microrelief), and various disturbance metrics evaluated on an ordinal scale.
* **Soil Data:** Details physical characteristics (sand, silt, clay percentages), moisture levels, and chemical composition (including pH, nitrogen, and phosphorus).
* **Species Data:** Provides the estimated percent land cover for various plant taxa using an ordinal cover-abundance scale.

## Target Persona
The assigned persona for this project is **XYZ**, a researcher studying Arctic tundra vegetation near Oumalik. 
* **Goal:** Understand why plant communities differ across sites that initially appear similar.
* **Needs:** Clear, interpretable visual evidence to compare communities, identify ecological patterns, and pinpoint environmental drivers (like soil pH or historical disturbance) without overly complex statistical details.

## Design Process
We started with the **diverge phase**, exploring a broad spectrum of design concepts independently using hand-drawn sketches. We utilized methods like modifying existing graphics and merging unrelated ideas. During in-person meetings, we discussed the core elements to include, critically evaluated our sketches, and discarded several concepts to select the most representative and intuitive ones. Finally, in the **converge phase**, we turned our combined ideas into clear designs, polished the details, and ensured the project met all its goals.

## Project Structure & Contributions
This project was developed as a collaborative effort by a three-person team. 
* **This Repository:** Contains my individual implementation and contribution to the project, focusing on the interactive plant-metaphor visualization.
* **Team Members:** The other two team members have hosted their respective parts of the project in their own separate repositories.

## The Visualization

### Intended vs. Actual Design
The main goal was to easily compare a few communities simultaneously, showing key data (pH, disturbance score, site moisture, thaw depth, and soil percentages) in a simple, aesthetically pleasing way. 

While the intended design considered including plant cover layers and soil minerals, the **actual design** resulted in a streamlined, interactive visual tool that compares two selected communities side-by-side using a plant metaphor.

### How to Read the Chart (Visual Encoding)
* **Petals (Disturbance Score):** The maximum score is 12 (represented by 12 petals). The color doesn't matter, only the count. A missing petal means the score goes up by one (e.g., seeing 5 petals means a disturbance score of 7).
* **Flower Center (pH Value):** The color indicates the pH value for a given community, mapped to a dedicated legend. It is designed to be both intuitive and counterintuitive to prompt closer inspection.
* **Stem (Site Moisture):** Values range from 1 to 10. Each block represents one point; the higher the moisture value, the longer the stem.
* **Roots (Thaw Depth):** The length of the roots directly correlates to the thaw depth.
* **Soil Rectangle (Composition):** Shows the precise mix of silt, clay, and sand percentages (adding up to 100%).

### Interactive Features
* **Community Selection:** Use the dropdown menus at the top to choose which two communities to compare (Community 1 on the left, Community 2 on the right).
* **Hover Tooltip:** Moving your mouse over the flower reveals a small box with exact numerical values for all its components.
* **Bottom Legend:** Helps quickly translate the flower center's color into the exact pH value.
* **Missing Data:** If data for a specific part is unavailable, it is represented as an empty box with dashed lines and no fill color.

## Future Improvements
The current tool successfully establishes the core concept, but there is room for advanced programmatic features:
* **Multi-Community Comparison:** Adding functionality to compare three, four, or more plants side-by-side.
* **Cover Layers:** Encoding species data as small leaves on the stem or a layer of moss above the soil, scaling their size to the percentage of the cover layer.
* **Automated Sorting:** Implementing one-click sorting to arrange all generated plants automatically (e.g., from lowest to highest pH, or by root length).
