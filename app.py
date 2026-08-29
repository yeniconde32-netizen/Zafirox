elif opcion == "🎵 Vídeos Musicales en Streaming":
    st.title("🎵 Vídeos Musicales en Streaming")
    st.write("Disfruta de tus videoclips musicales favoritos y una selección ampliada con más éxitos:")
    
    videos_musicales = {
        "Videoclip Pop & Hits Globales": "https://www.youtube.com/embed/9bZkp7q19f0",
        "Videoclip Dance & Party Electrónica": "https://www.youtube.com/embed/kJQP7kiw5Fk",
        "Videoclip Rock & Alternative Vibes": "https://www.youtube.com/embed/hTWKbfoikeg",
        "Videoclip Synthwave & Retro Beats": "https://www.youtube.com/embed/4xDzrJKXOOY",
        "Videoclip Rock Clásico Internacional (Hits Adicionales)": "https://www.youtube.com/embed/kDWgsQhbaqU",
        "Videoclip Pop Latino & Urbano (Variedad)": "https://www.youtube.com/embed/kJQP7kiw5Fk"
    }
    
    mus_elegida = st.selectbox("Elige un vídeo musical de la lista:", list(videos_musicales.keys()), key="select_musica_iframe")
    embed_mus_url = videos_musicales[mus_elegida]
    
    st.markdown(
        f"""
        <div style="position: relative; width: 100%; height: 315px; margin-bottom: 15px;">
            <iframe src="{embed_mus_url}?enablejsapi=1&autoplay=0&rel=0" title="Reproductor ZafiroX" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen style="width: 100%; height: 100%; border-radius: 10px;"></iframe>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    st.markdown("---")
    st.markdown("#### Publicidad Patrocinada:")
    st.components.v1.html(banner_anuncio_html, height=120)
    
    estado_vidmus_clave = f"{usuario}_vidmus_{mus_elegida}"
    
    if estado_vidmus_clave in st.session_state.videomusica_vista:
        st.button("🎥 Vídeo musical ya reclamado", disabled=True, key="btn_vidmus_disabled")
    else:
        if st.button("🎥 Reclamar Bonus de Vídeo Musical (+0.004 💎)", key="btn_vidmus_claim"):
            st.session_state.videomusica_vista[estado_vidmus_clave] = True
            actualizar_saldo(0.004)
            st.success("✅ ¡Bonus de vídeo musical acreditado!")
            time.sleep(0.8)
            st.rerun()
