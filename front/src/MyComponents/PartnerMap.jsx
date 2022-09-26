import React, {useEffect, useRef, useState} from 'react';
import {YMaps, Map, ObjectManager} from "react-yandex-maps";
import PartnerSearch from "./PartnerSearch";
import SwipeableEdgeDrawer from "./SwipeableEdgeDrawer";
import axios from "axios";
import {useNavigate} from "react-router-dom";


const PartnerMap = (props) => {
    // tg web app
    const tg = useRef(window.Telegram.WebApp)

    // back button
    const navigate = useRef(useNavigate());

    // ymaps
    const [map, setMap] = useState(null);
    const [ymaps, setYmaps] = useState(null);
    const [objectManager, setObjectManager] = useState(null);
    const mainRef = useRef(null)
    // Current placemarks on map
    let [currentFeatures, setCurrentFeatures] = useState({})
    let featureId = useRef(-1)

    // Current swipeable paper params
    let [drawerText, _setDrawerText] = useState('')
    const drawerTextRef = useRef(drawerText)
    const setDrawerText = (val) => {
        _setDrawerText(val)
        drawerTextRef.current = val
    }

    let [drawerSecondaryText, _setDrawerSecondaryText] = useState('')
    const drawerSecondaryTextRef = useRef(drawerSecondaryText)
    const setDrawerSecondaryText = (val) => {
        _setDrawerSecondaryText(val)
        drawerSecondaryTextRef.current = val
    }

    const [drawerOpen, setDrawerOpen] = React.useState(false);

    let [drawerHours, setDrawerHours] = useState('')

    const mainButtonCallback = () => {
        axios.post('https://api.1032649-cu51513.tmweb.ru/order', {
            place: `${drawerTextRef.current}`,
            address: `${drawerSecondaryTextRef.current}`,
        }).then((res) => tg.current.close()).catch((e) => tg.current.close())
    }
    const backButtonClick = () => navigate.current(-1)

    useEffect(() => {
        tg.current.ready()
        axios.defaults.headers.common['auth'] = tg.current.initData
        tg.current.MainButton.hide()
        tg.current.MainButton.color = "#ff9800"
        tg.current.MainButton.text = 'Привезу отсюда'
        tg.current.onEvent('mainButtonClicked', mainButtonCallback)
        tg.current.BackButton.show()
        tg.current.BackButton.onClick(backButtonClick)
        mainRef.current.scrollIntoView()
        return () => {
            tg.current.BackButton.offClick(backButtonClick)
            tg.current.offEvent('mainButtonClicked', mainButtonCallback)
            tg.current.MainButton.hide()
            tg.current.MainButton.color = tg.current.themeParams.button_color
        }
    }, [])


    useEffect(() => {

        if (map && ymaps && objectManager) {
            map.events.add('click', (e) => {
                console.log(e)
                if (featureId.current !== -1) {
                    objectManager.objects.setObjectOptions(featureId.current, {
                        preset: 'islands#blueDotIcon'
                    })
                    featureId.current = -1
                    setDrawerText('')
                    tg.current.MainButton.hide()
                }
            });
        }
    })

    useEffect(() => {
        if (objectManager !== null) {
            objectManager.objects.events.add('click', (e) => {
                // changing pm color && pining map to pm
                const objectId = e.get('objectId');
                if (featureId.current !== objectId) {
                    objectManager.objects.setObjectOptions(featureId.current, {
                        preset: 'islands#blueDotIcon'
                    })
                }
                objectManager.objects.setObjectOptions(objectId, {
                    preset: 'islands#lightBlueDotIcon'
                })
                const placemark = objectManager.objects.getById(objectId)
                map.panTo(placemark.geometry.coordinates)
                // setting current company name
                setDrawerText(placemark.properties.name ?? '-')
                setDrawerSecondaryText(placemark.properties.description ?? '-')
                setDrawerHours(placemark.properties.CompanyMetaData.Hours ? placemark.properties.CompanyMetaData.Hours.text : '-')
                setDrawerOpen(true)
                tg.current.MainButton.show()
                // setting current feature (pm)
                featureId.current = objectId
            })
        }
    }, [map, objectManager])

    return (
        <div ref={mainRef} style={{height: '100%', width: '100%'}}>
            <YMaps query={{ load: ['ObjectManager', 'Placemark'] }}>
                <Map defaultState={{
                    center: [54.965021, 82.937751],
                    zoom: 10,
                }}
                     width={'100%'} height={'100%'}
                     instanceRef={(ref) => setMap(ref)}
                     onLoad={(ref) => setYmaps(ref)}
                     defaultOptions={{yandexMapDisablePoiInteractivity: true}}
                >
                    <ObjectManager
                        options={{
                            clusterize: true,
                            gridSize: 32,
                        }}
                        objects={{
                            openBalloonOnClick: true,
                            preset: 'islands#blueDotIcon',
                        }}
                        clusters={{
                            preset: 'islands#blueClusterIcons',
                        }}
                        // filter={object => object.id % 2 === 0}
                        modules={[
                            'objectManager.addon.objectsBalloon',
                            'objectManager.addon.objectsHint',
                        ]}
                        features={currentFeatures}
                        instanceRef={ref => setObjectManager(ref)}
                    />
                    {/*<Placemark geometry={[55.73003,37.730056]} options={{'color': 'rgb(155, 102, 102)'}} />*/}
                </Map>
            </YMaps>
            <PartnerSearch drawerText={drawerText} setDrawerText={setDrawerText} map={map} ymaps={ymaps} objectManager={objectManager} currentFeatures={currentFeatures} setCurrentFeatures={setCurrentFeatures} />
            <SwipeableEdgeDrawer open={drawerOpen} setOpen={setDrawerOpen} drawerHours={drawerHours} drawerText={drawerText} drawerSecondaryText={drawerSecondaryText} />
        </div>
    )
};

export default PartnerMap;