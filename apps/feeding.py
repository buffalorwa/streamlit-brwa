import os
from pathlib import Path
import streamlit as st
# import leafmap.foliumap as leafmap
import folium
from folium.plugins import BeautifyIcon, MarkerCluster, Fullscreen
# from streamlit_folium import folium_static#st_folium
import streamlit.components.v1 as components
import geopandas as gpd




popup_dict = {'source':"Data Source",'inside':"Miles from BNRW",
              'last_active':"Last year active",'gps':'GPS'}

@st.cache  
def popupHTML(row, popup_dict=popup_dict,col1width=50):
    '''Create custom HTML for popup.

    Parameters
    ----------
    row : TYPE
        DESCRIPTION.

    Returns
    -------
    html : TYPE
        DESCRIPTION.
        
    After: https://towardsdatascience.com/folium-map-how-to-create-a-table-style-pop-up-with-html-code-76903706b88a
           and https://github.com/Gromopo/GroMoPo

    '''
    html = """<!DOCTYPE html>
            <html>
            
            <table>
            <tbody>
            """
    
    for key, value in popup_dict.items():
        # Loop through entries for popup with specific formatting
        
        if row[key] is None:
            second_col_val= 'N/A'
        else:
            second_col_val = row[key]
        
        if 'link' in value: # format for clickable link
            html += """<tr>
                       <td><span style="text-align: left;width: {0}px; color: #293191; overflow-wrap: break-word;"><b>{1}</b></span></td>
                       <td><span style="text-align: right;overflow-wrap: break-word;>""".format(col1width,value) # Attribute name
                       
            # if second_col_val != 'N/A' and second_col_val is not None:
                
            links = second_col_val.split('|')
            links.insert(0,"") # for some reason need a dummy entry, as first entry doesn't show up as link, only as text.
            
                
            # link_html = """ """.join(["""<a href="{0}" target="_blank"> {0}</a><br>""".format(link) for link in links])
            link_html = """ """
            for i,link in enumerate(links):
                if i == 0:
                    link_html += """<a href="{0}" target="_blank">{0}</a>""".format(link)
                elif link == 'N/A':
                    link_html += """{}<br>""".format(link)
                else:
                    link_html += """<a href="{0}" target="_blank">{0}</a><br>""".format(link)
            
            html += link_html
            # else:
            #     html += """{0}<br>""".format(second_col_val)
                
            html += """</span></td></tr>"""
            # html += """</td></td></td></tr>"""


        else:
            html += """<tr>
                       <td style="text-align: left;"><span style="width: {0}px;color: #000000;overflow-wrap: break-word;"><b>{1}</b></span></td>
                       <td style="text-align: right; overflow-wrap: break-word;">{2}</td></tr>""".format(col1width,value,second_col_val)
                       
    
    html += """</tbody>
               </table>                    
               </html>"""
    
    return html

def load_xy_to_cluster(shp_df,icon_name='home',popup_cols=[],
                       include_latlon=True,min_width=100,max_width=200,):
    
    m_cluster = MarkerCluster(name="Poultry Houses",control=True)
    
    # Only works with v4, https://fontawesome.com/v4/icons/
    # in v5, there is 'turkey'
    # for ilon,ilat in zip(lon,lat):
    for irow,row_df in shp_df.iterrows():
        
        html = row_df['popup_html']
        # if include_latlon: # add latitude and longitude
        #     html = html + "<b>" + 'GPS' + "</b>" + ": " + "{0:3.4f},{1:3.4f}".format(row_df.geometry.y,row_df.geometry.x) + "<br>"
        # for p in popup_cols:
        #     html = html + "<b>" + p + "</b>" + ": " + str(row[p]) + "<br>"
        
        
        if len(html)>0:
            mark_popup = folium.Popup(html,min_width=min_width, max_width=max_width)
        else:
            mark_popup = None
        
        if row_df['active'] == 1:
            color = 'black'
        else:
            color = 'grey'
        
        
        folium.Marker([row_df.geometry.y,row_df.geometry.x],
               popup=mark_popup,
               icon=BeautifyIcon(icon=icon_name,
                                 icon_shape='circle', 
                                 border_color='transparent', 
                                 inner_icon_style= 'color:{};font-size:30px'.format(color),
                                 # border_width=2,
                                 background_color='transparent')).add_to(m_cluster)
    return m_cluster

# if platform.system() == 'Windows':
#     main_path = Path(".")
# else:
main_path = Path(".")
    
shp_path = str(main_path.absolute().joinpath('data', 'bnr_chicken_house+2mile.geojson'))
shp_df = gpd.read_file(shp_path)
shp_df.loc[shp_df['last_active'].isna(),'last_active'] = 2022
shp_df['last_active'] = gpd.pd.to_numeric(shp_df['last_active'],downcast="integer")
shp_df['gps'] = shp_df.apply(lambda row: "{0:3.4f},{1:3.4f}".format(row.geometry.xy[1][0],row.geometry.xy[0][0]),axis=1)


shp_df['popup_html'] = shp_df.apply(popupHTML,axis=1)


m_cluster = load_xy_to_cluster(shp_df)

ws_path = str(main_path.absolute().joinpath('data', 'bnr_ws_hu8.geojson'))
ws_style = lambda x:{'lineColor':'#F0F8FF',
            'weight': 3,
            'interactive':False,
            'stroke':True,
            'fillColor':'none',
    }


about_text = """
        This web [app](https://github.com/buffalorwa/streamlit-brwa) is maintained by the [Buffalo River Watershed Alliance](https://buffaloriveralliance.org/).
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
    ----- NOTE: application is still in development ----
    
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
                    
                    **70** houses within the BNR watershed \n
                    **65** additional houses within 2 miles of the BNR watershed \n
                    **98** estimated active houses <img src="https://raw.githubusercontent.com/FortAwesome/Font-Awesome/6.x/svgs/solid/house.svg" width="20" height="20"> within 2 miles of BNR watershed \n
                    ** xzy ft^2** roof area ~= **n chickens** and \n
                    **xzy lb/yr solid waste** \n
                    
                    **Black** houses are active, <span style="color:grey">**Grey**</span> inactive
                    
                    ---
                    # Hog operations \n
                    
                    No known hog operations are currently active in the BNR watershed, 
                    but closed sites could have a lasting effect on the water quality.
                    ''',
                    unsafe_allow_html=True)
    
    with st.expander("Additional information"):
        st.markdown(about_text)
        st.write("""
                 The calculations for the solid waste production were based on 
                 the methods developed for the WaterKeeper Alliance and EWG
                 ["Fields of Filth" interactive map](https://www.ewg.org/interactive-maps/2020-fields-of-filth/map/).
                 This methodology is further described  at https://www.ewg.org/research/exposing-fields-filth-north-carolina.
                 
                 
                 
                 
                 
                 # References \n
                 AHTD (Arkansas Highway and Transportation Department) Chicken Houses, August 29, 2006: https://gis.arkansas.gov/product/chicken-house-point/
                 
                 """)