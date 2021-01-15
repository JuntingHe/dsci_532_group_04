### Section 3: Usage scenarios

Angie is a manager of a newly formed special division in United Nations, responsible for tracking Life expectancy across the world, advising policy makers responsible for taking decisions about administrative and financial aides and creating public awareness about Life expectancy in developing countries and factors affecting it. Angie and most of her team members are very passionate about quality of life around the world and dedicated good part of their life to help people living in questionable conditions

As part of the first milestone, Angie and her wants to have a dashboard for tracking average life expectancy which can be used by her team, the policy makers in UN and general public to understand how it has changed over the time and the factors affecting it. Based on this dashboard, Angie's team will report how Life expectancy has changed over time in every corner of the world and whether the steps taken by UN in last 15 years are yielding results.

Angie's team reached out the the data scientists of MDS DSCI 532 group 4 to build the initial version of the dashboard using publicly available data from last 15 years.

Following are the functional and technical requirements, based on initial requirement analysis:
- Functional requirements:
    - The users should be able to filter the dashboard based on year, multiple continents and countries
    - The key indicators are - Average life expectancy of a selected year and percentage change over 5 years:
        - Worldwide
        - For each continents
    - Other indicators are - Average life expectancy of a selected year and percentage change over 5 years for developed and developing countries
    - The team had mentioned about highlighting a target value for each indicators and may add it as an enhancement later.
    - The users should be able to see trend by year based on continent, country and status
    - The dashboard should enable users to perform multi-dimensional analysis to understand factors affecting Life expectancy
- Technical requirements:
    - There dashboard should have three global filters:
        - year
        - continent (multi-select)
        - country (multi-select)
    - The indicators should be presented at the top of the dashboard
    - The dashboard should have a line chart for Average Life expectancy vs year by continent
    - The dashboard should have a line chart for Average Life expectancy vs year by status
    - The dashboard should have a line chart for Average Life expectancy vs year with a separate combo box to select one country. Based on the country selected the graph will show life expectancy trend for the selected country, its continent and the entire world. This is required to understand how a particular country is doing in comparison to its continent and world
    - The dashboard should have a scatter-plot for each country with Life expectancy as fixed y-axis and the users will be able to change the dimension in x-axis, color and size. This is required to perform multi-dimensional analysis to understand factors affecting life expectancy
