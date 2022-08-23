import streamlit as st

# The next line sets the text to put in a browser window
st.set_page_config(page_title="Buffalo National River Geospatial Explorer", layout="wide",initial_sidebar_state="collapsed")

from streamlit_option_menu import option_menu # https://github.com/victoryhb/streamlit-option-menu
from apps import  feeding ,geology# ,home # import your app modules here



# Remove whitespace from the top of the page and sidebar
st.markdown("""
        <style>
               .css-18e3th9 {
                    padding-top: 0rem;
                    padding-bottom: 10rem;
                    padding-left: 5rem;
                    padding-right: 5rem;
                }
               .css-1d391kg {
                    padding-top: 3.5rem;
                    padding-right: 1rem;
                    padding-bottom: 3.5rem;
                    padding-left: 1rem;
                }
        </style>
        """, unsafe_allow_html=True)

# A dictionary of apps in the format of {"App title": "App icon"}
# More icons can be found here: https://icons.getbootstrap.com
# Apps are the individual pages on the site. Each is a .py file in the "apps" folder
# Updating this list will automatically update the menu options
apps = [
    #{"func": home.app, "title": "BNR Explorer", "icon": "house"},
    {"func": feeding.app, "title": "Feeding Operations", "icon": "piggy-bank"},
    #{"func": hydrology.app, "title": "Hydrology", "icon": "droplet"}, # map
    {"func": geology.app, "title": "Geology", "icon": "boxes"},
]

# The information that shows up in the "About" box. Use the [text to show](link) format to add website links
about_text = """
        This web [app](https://github.com/eventual_link_to_app/app.py) is maintained by the [Buffalo River Watershed Alliance](https://buffaloriveralliance.org/). You can follow us on social media:
             [Twitter](https://twitter.com/AllianceBuffalo) | [YouTube](https://www.youtube.com/channel/UCyNTnECDDGIAOUE6pYWGnTQ) | [Facebook](https://www.facebook.com/Buffalo-River-Watershed-Alliance-164944453665495/) | [GitHub](https://github.com/tbd).
    """

menu_name = "Buffalo River Explorer" #  Text to put above the menu of pages/apps

# ------------ No need to change anything from here on ------------
# -----------------------------------------------------------------

titles = [app["title"] for app in apps]
titles_lower = [title.lower() for title in titles]
icons = [app["icon"] for app in apps]

params = st.experimental_get_query_params()

if "page" in params:
    default_index = int(titles_lower.index(params["page"][0].lower()))
else:
    default_index = 0

with st.sidebar:
    selected = option_menu(
        menu_name,
        options=titles,
        icons=icons,
        menu_icon="cast",
        default_index=default_index,
    )
    
    # Define the information for the "About" box in the contents bar on the left
    st.sidebar.title("About") # title of the box
    st.sidebar.info(about_text)

for app in apps:
    if app["title"] == selected:
        app["func"]()
        break
