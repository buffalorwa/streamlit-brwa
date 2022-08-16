import streamlit as st
import leafmap.foliumap as leafmap

ws_path = r"data\bnr_ws_hu8.geojson"
ws_style = {'lineColor':'#F0F8FF',
            'weight': 3,
            'interactive':False,
            'stroke':True,
    }


def app():
    st.title("BNR Explorer")

    st.markdown(
        """
    Welcome to the Buffalo National River (BNR) Geospatial Explorer! Learn more about the water, rocks, and places in and around the BNR watershed.
    
    To learn more about protecting and supporting the health of the BNR, visit the [Buffalo River Watershed Alliance](https://buffaloriveralliance.org/)! 

    """
    )

    m = leafmap.Map(center=(35.9658, -92.8103), zoom=10,locate_control=True)
    
    # Add google maps as a basemap option
    m.add_basemap("ROADMAP")
    
    # Add watershed outline
    m.add_geojson(ws_path, layer_name='BNR Watershed', style=ws_style, fill_colors=['none'])
    
    m.to_streamlit(height=700)
