import streamlit as st
import leafmap.foliumap as leafmap
from folium import Marker, Icon, GeoJson,Popup
from folium.plugins import MarkerCluster
from folium.plugins import BeautifyIcon
import geopandas as gpd

def load_xy_to_cluster(shpname,icon_name='home',popup_cols=[],
                       include_latlon=True,min_width=100,max_width=200,):
    shp_df = gpd.read_file(shp_path)
    lon = shp_df.geometry.x.values
    lat = shp_df.geometry.y.values
    
    m_cluster = MarkerCluster(name="Chicken Clusters",control=False)
    
    # Only works with v4, https://fontawesome.com/v4/icons/
    # in v5, there is 'turkey'
    for ilon,ilat in zip(lon,lat):
        
        html = ""
        if include_latlon: # add latitude and longitude
            html = html + "<b>" + 'GPS' + "</b>" + ": " + "{0:3.4f},{1:3.4f}".format(ilat,ilon) + "<br>"
        for p in popup_cols:
            html = html + "<b>" + p + "</b>" + ": " + str(row[p]) + "<br>"
        
        
        if len(html)>0:
            mark_popup = Popup(html,min_width=min_width, max_width=max_width)
        else:
            mark_popup = None
        
        Marker([ilat,ilon],
               popup=mark_popup,
               icon=BeautifyIcon(icon=icon_name,
                                 icon_shape='circle', 
                                 border_color='transparent', 
                                 inner_icon_style= 'color:black',
                                 # border_width=2,
                                 background_color='transparent')).add_to(m_cluster)
    return m_cluster

shp_path = r"data\bnr_chicken_house.geojson"
m_cluster = load_xy_to_cluster(shp_path)

ws_path = r"data\bnr_ws_hu8.geojson"
ws_style = {'lineColor':'#F0F8FF',
            'weight': 3,
            'interactive':False,
            'stroke':True,
    }


about_text = """
        This web [app](https://github.com/eventual_link_to_app/app.py) is maintained by the [Buffalo River Watershed Alliance](https://buffaloriveralliance.org/).
        You can follow the BRWA on social media:
             [Twitter](https://twitter.com/AllianceBuffalo) | [YouTube](https://www.youtube.com/channel/UCyNTnECDDGIAOUE6pYWGnTQ) | [Facebook](https://www.facebook.com/Buffalo-River-Watershed-Alliance-164944453665495/) | [GitHub](https://github.com/tbd).
    """

imaps = ['TERRAIN','HYBRID','ROADMAP']#leafmap.basemap_xyz_tiles()

def app():
    st.title("Feeding Operations in the Buffalo National River Watershed")

    st.markdown(
        """
    Text about feeding operations and water quality and the history of the BNR. This map includes operations within 1 mile of the watershed.

    """
    )

    c1, c2 = st.columns([3,1])
    
    with c1:
        m = leafmap.Map(center=(35.9658, -92.8103), zoom=10,locate_control=True)
        
        # Add google maps as a basemap option
        
        for ikey in imaps:
            m.add_basemap(ikey)
        # m.add_basemap("HYBRID")
        # m.add_basemap("ROADMAP")
        
        # Add watershed outline
        m.add_geojson(ws_path, layer_name='BNR Watershed', style=ws_style, fill_colors=['none'])
        
    
        # Add chicken houses
        # m_ch = GeoJson(shp_path, name='Chicken Houses (2014)')
        
        # m_group = FeatureGroup(name='Chicken Clusters').add_to(m)
        m_cluster.add_to(m)
        # m_ch.add_to(m_group)
        
        m.to_streamlit(height=700,bidirectional=False)

    with c2:
        # Eventually information on the (static) number of known feeding operations and
        # how many are estimated to be active in the ws. Markdown isn't working right
        st.markdown('''
                    # Poultry Operations \n
                    
                    **50ish** within the BNR watershed \n
                    **n** estimated active \n
                    **n ft^2** roof area ~= **n chickens** and \n
                    **xzy lb/yr solid waste** \n
                    ---
                    # Hog operations \n
                    
                    No known hog operations are currently active in the BNR watershed, 
                    but closed sites could have a lasting effect on the water quality.
                    ''',
                    unsafe_allow_html=True)
    
    with st.expander("Additional information"):
        st.markdown(about_text)
        st.write("""
                 The calculations were ...
                 """)