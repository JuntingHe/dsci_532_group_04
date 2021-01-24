
# Reflection

## Implemented/ Changes made based on feedback:

- The layout of the app is slightly changed compared to the proposal to make it more esthetic.
- Removed drop-down menu for continent and countries (global control)
  - Implemented local filter instead
- Removed the size component from the scatter plot due to overwhelming information
- Combined the trend by the continent plot and trend by status plot into a single chart
  - Added a radio button options for changing the color axis (toggle between continent and status)
- Changed the granularity of the world map from continent to country

## Not yet implemented:

- Toggle collapse menu
- Interactive map

## Known issues (intend to fix this in the later milestone):

- Some countries are not showing up on the map (probably due to the countries' name mismatch between the dataset and the metadata of the map)
- Scaling of the dashboard
  - When the browser size is being reduced, the charts overlap each other. We will try to address this issue if time permits

Our dashboard does well in enabling a user to perform multi-dimensional analysis to understand the factors affecting life expectancy. However, if we are given a new column in our dataset, our dashboard may need additional enhancement. We will make improvements based on TA feedbacks and solve previous known issues. Also, we will try implementing new features including an interactive map using Plotly and creating a toggle collapse menu. 
