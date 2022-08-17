import os
from pathlib import Path
import streamlit as st
# import leafmap.foliumap as leafmap
import folium
from folium.plugins import BeautifyIcon, MarkerCluster, Fullscreen
# from streamlit_folium import folium_static#st_folium
import streamlit.components.v1 as components
import geopandas as gpd

def load_xy_to_cluster(shpname,icon_name='home',popup_cols=[],
                       include_latlon=True,min_width=100,max_width=200,):
    shp_df = gpd.read_file(shp_path)
    lon = shp_df.geometry.x.values
    lat = shp_df.geometry.y.values
    
    m_cluster = MarkerCluster(name="Poultry Houses",control=True)
    
    # Only works with v4, https://fontawesome.com/v4/icons/
    # in v5, there is 'turkey'
    for ilon,ilat in zip(lon,lat):
        
        html = ""
        if include_latlon: # add latitude and longitude
            html = html + "<b>" + 'GPS' + "</b>" + ": " + "{0:3.4f},{1:3.4f}".format(ilat,ilon) + "<br>"
        for p in popup_cols:
            html = html + "<b>" + p + "</b>" + ": " + str(row[p]) + "<br>"
        
        
        if len(html)>0:
            mark_popup = folium.Popup(html,min_width=min_width, max_width=max_width)
        else:
            mark_popup = None
        
        folium.Marker([ilat,ilon],
               popup=mark_popup,
               icon=BeautifyIcon(icon=icon_name,
                                 icon_shape='circle', 
                                 border_color='transparent', 
                                 inner_icon_style= 'color:black',
                                 # border_width=2,
                                 background_color='transparent')).add_to(m_cluster)
    return m_cluster

# if platform.system() == 'Windows':
#     main_path = Path(".")
# else:
main_path = Path(".")
    
shp_path = str(main_path.absolute().joinpath('data', 'bnr_chicken_house.geojson'))

# shp_path = r"data\bnr_chicken_house.geojson"
m_cluster = load_xy_to_cluster(shp_path)

ws_path = str(main_path.absolute().joinpath('data', 'bnr_ws_hu8.geojson'))
ws_style = lambda x:{'lineColor':'#F0F8FF',
            'weight': 3,
            'interactive':False,
            'stroke':True,
            'fillColor':'none',
    }


about_text = """
        This web [app](https://github.com/eventual_link_to_app/app.py) is maintained by the [Buffalo River Watershed Alliance](https://buffaloriveralliance.org/).
        You can follow the BRWA on social media:
             [Twitter](https://twitter.com/AllianceBuffalo) | [YouTube](https://www.youtube.com/channel/UCyNTnECDDGIAOUE6pYWGnTQ) | [Facebook](https://www.facebook.com/Buffalo-River-Watershed-Alliance-164944453665495/) | [GitHub](https://github.com/tbd).
    """

# https://github.com/giswqs/leafmap/blob/84fb926c556dd377baaf10d9a9c57d749fb5c9cb/leafmap/basemaps.py#L23
imaps = {
    "ROADMAP": {
        "url": "https://mt1.google.com/vt/lyrs=m&x={x}&y={y}&z={z}",
        "attribution": "Google",
        "name": "Google Maps",
    },
    "TERRAIN": {
        "url": "https://mt1.google.com/vt/lyrs=p&x={x}&y={y}&z={z}",
        "attribution": "Google",
        "name": "Google Terrain",
    },
    "HYBRID": {
        "url": "https://mt1.google.com/vt/lyrs=y&x={x}&y={y}&z={z}",
        "attribution": "Google",
        "name": "Google Satellite",
    },
}

def app():
    st.title("Feeding Operations in the Buffalo National River Watershed")

    st.markdown(
        """
    Text about feeding operations and water quality and the history of the BNR. This map includes operations within 1 mile of the watershed.

    """
    )

    c1, c2 = st.columns([3,1])
    
    with c1:
        m = folium.Map(location=(35.9658, -92.8103), zoom_start=10)
        
        # Add google maps as a basemap option
        
        for ikey in imaps:
            folium.TileLayer(imaps[ikey]['url'],attr=imaps[ikey]['attribution'],name=imaps[ikey]['name']).add_to(m)
        # m.add_basemap("HYBRID")
        # m.add_basemap("ROADMAP")
        
        # Add watershed outline
        # m.add_geojson(ws_path, layer_name='BNR Watershed', style=ws_style, fill_colors=['none'])
        folium.GeoJson(ws_path, name='BNR Watershed', style_function=ws_style).add_to(m)
    
        # Add chicken houses
        # m_ch = GeoJson(shp_path, name='Chicken Houses (2014)')
        
        # m_group = FeatureGroup(name='Chicken Clusters').add_to(m)
        m_cluster.add_to(m)
        # m_ch.add_to(m_group)
        
        m.add_child(folium.LayerControl())
        Fullscreen().add_to(m)
    
        # folium_static(m, height=700, width=1400)
        # folium_static(m,height=700,width=1000)
        
        fig = folium.Figure().add_child(m)
        components.html(
                        fig.render(), height=700 + 10
                        )
        
        # outfile = os.path.abspath('feedingtemp' + ".html")
        # m.save(outfile)
        # out_html = ""
        # with open(outfile) as f:
        #     lines = f.readlines()
        #     out_html = "".join(lines)
        # os.remove(outfile)
        
        # components.html(out_html,height=700,scrolling=False)

    with c2:
        # Eventually information on the (static) number of known feeding operations and
        # how many are estimated to be active in the ws. Markdown isn't working right
        st.markdown('''
                    # Poultry Operations \n
                    
                    **50ish** houses within the BNR watershed \n
                    **50ish** additional houses within 2 miles of the BNR watershed \n
                    **xyz** estimated active houses \n
                    ** xzy ft^2** roof area ~= **n chickens** and \n
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