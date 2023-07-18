# Work Log 
## 7/18
- Created config.toml to allow default configurations for our app, mainly to force a certain theme on users
- Updated graphing methods to have a grid in the background, improves readability
- Wrapped all the styling configurations for the different plots into one method, reduces lines and improves coherency
- renamed streamlit_app.py => app.py to improve conciseness, fixed renaming bugs
- Added collapsing characteristic to pages

## 7/14 
- Wrapped line plot and frequency plot into one method 'roulette_plot' to create a uniform method for roulette strategies
- Redesigned aesthetics for line and frequency plot
- Fixed input boxes on forms, added greyed out suggestion texts and optional input fields
- Fixed tickmarks on graphs to show accurate values
- Fixed vertical line starting balance indicator on histogram
- Reorganized graphs into st.columns
- Created the box and whisker plot
- Created sliders for the forms to update in real time
- Reformatted pages of roulette strategies